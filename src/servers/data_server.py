#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 관리 MCP 서버 - 로컬 DB 및 보안 관리
"""

import os
import json
import sqlite3
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .base_server import BaseMCPServer

class DataServer(BaseMCPServer):
    """데이터 관리 MCP 서버"""
    
    def __init__(self):
        super().__init__("DataServer")
        self.db_path = "data/user_data/retirement_agent.db"
        self.backup_dir = "data/backups"
        self.encryption_key = None
        self._init_database()
        self._init_encryption()
    
    def _init_database(self):
        """데이터베이스 초기화"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 사용자 프로필 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                profile_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 경제 가정 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS economic_assumptions (
                user_id TEXT,
                scenario_type TEXT,
                assumptions_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, scenario_type),
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
            )
        ''')
        
        # 투자 포트폴리오 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investment_portfolios (
                user_id TEXT,
                portfolio_id TEXT,
                portfolio_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, portfolio_id),
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
            )
        ''')
        
        # 백업 기록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_records (
                backup_id TEXT PRIMARY KEY,
                user_id TEXT,
                backup_type TEXT,
                file_path TEXT,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_encryption(self):
        """암호화 키 초기화"""
        key_file = "data/user_data/encryption.key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # 새 키 생성
            self.encryption_key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
    
    def setup_tools(self):
        """데이터 관리 도구들 설정"""
        
        # 로컬 DB 관리
        self.register_tool(
            "manage_local_database",
            self.manage_local_database,
            "로컬 DB CRUD 작업"
        )
        
        self.register_tool(
            "encrypt_sensitive_data",
            self.encrypt_sensitive_data,
            "민감 데이터 암호화"
        )
        
        self.register_tool(
            "decrypt_sensitive_data",
            self.decrypt_sensitive_data,
            "암호화된 데이터 복호화"
        )
        
        self.register_tool(
            "backup_user_data",
            self.backup_user_data,
            "사용자 데이터 백업"
        )
        
        self.register_tool(
            "restore_user_data",
            self.restore_user_data,
            "사용자 데이터 복원"
        )
        
        self.register_tool(
            "list_backups",
            self.list_backups,
            "백업 목록 조회"
        )
        
        self.register_tool(
            "cleanup_old_backups",
            self.cleanup_old_backups,
            "오래된 백업 정리"
        )
    
    async def start(self):
        """서버 시작"""
        self.is_running = True
        self.logger.info("데이터 관리 서버가 시작되었습니다.")
    
    async def stop(self):
        """서버 중지"""
        self.is_running = False
        self.logger.info("데이터 관리 서버가 중지되었습니다.")
    
    # 도구 구현 메서드들
    async def manage_local_database(self, operation: str, table: str, user_id: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """로컬 DB CRUD 작업"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if operation == "create":
                if table == "user_profiles":
                    cursor.execute(
                        "INSERT OR REPLACE INTO user_profiles (user_id, profile_data) VALUES (?, ?)",
                        (user_id, json.dumps(data, ensure_ascii=False))
                    )
                elif table == "economic_assumptions":
                    scenario_type = data.get("scenario_type", "moderate")
                    cursor.execute(
                        "INSERT OR REPLACE INTO economic_assumptions (user_id, scenario_type, assumptions_data) VALUES (?, ?, ?)",
                        (user_id, scenario_type, json.dumps(data, ensure_ascii=False))
                    )
                elif table == "investment_portfolios":
                    portfolio_id = data.get("portfolio_id", f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    cursor.execute(
                        "INSERT OR REPLACE INTO investment_portfolios (user_id, portfolio_id, portfolio_data) VALUES (?, ?, ?)",
                        (user_id, portfolio_id, json.dumps(data, ensure_ascii=False))
                    )
            
            elif operation == "read":
                if table == "user_profiles":
                    cursor.execute("SELECT profile_data FROM user_profiles WHERE user_id = ?", (user_id,))
                    result = cursor.fetchone()
                    if result:
                        return {"status": "success", "data": json.loads(result[0])}
                    else:
                        return {"status": "error", "message": "사용자 프로필을 찾을 수 없습니다."}
                
                elif table == "economic_assumptions":
                    scenario_type = kwargs.get("scenario_type", "moderate")
                    cursor.execute(
                        "SELECT assumptions_data FROM economic_assumptions WHERE user_id = ? AND scenario_type = ?",
                        (user_id, scenario_type)
                    )
                    result = cursor.fetchone()
                    if result:
                        return {"status": "success", "data": json.loads(result[0])}
                    else:
                        return {"status": "error", "message": "경제 가정을 찾을 수 없습니다."}
                
                elif table == "investment_portfolios":
                    cursor.execute(
                        "SELECT portfolio_id, portfolio_data FROM investment_portfolios WHERE user_id = ?",
                        (user_id,)
                    )
                    results = cursor.fetchall()
                    portfolios = []
                    for row in results:
                        portfolios.append({
                            "portfolio_id": row[0],
                            "data": json.loads(row[1])
                        })
                    return {"status": "success", "data": portfolios}
            
            elif operation == "delete":
                if table == "user_profiles":
                    cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
                elif table == "economic_assumptions":
                    scenario_type = kwargs.get("scenario_type", "moderate")
                    cursor.execute(
                        "DELETE FROM economic_assumptions WHERE user_id = ? AND scenario_type = ?",
                        (user_id, scenario_type)
                    )
                elif table == "investment_portfolios":
                    portfolio_id = kwargs.get("portfolio_id")
                    if portfolio_id:
                        cursor.execute(
                            "DELETE FROM investment_portfolios WHERE user_id = ? AND portfolio_id = ?",
                            (user_id, portfolio_id)
                        )
            
            conn.commit()
            conn.close()
            
            return {"status": "success", "message": f"DB {operation} 작업 완료"}
            
        except Exception as e:
            return {"status": "error", "message": f"DB 작업 실패: {str(e)}"}
    
    async def encrypt_sensitive_data(self, data: Dict[str, Any], user_id: str, **kwargs) -> Dict[str, Any]:
        """민감 데이터 암호화"""
        try:
            fernet = Fernet(self.encryption_key)
            
            # 민감한 필드들만 암호화
            sensitive_fields = ['ssn', 'bank_account', 'phone', 'address', 'email']
            encrypted_data = data.copy()
            
            for field in sensitive_fields:
                if field in encrypted_data and encrypted_data[field]:
                    # 문자열을 바이트로 변환 후 암호화
                    encrypted_bytes = fernet.encrypt(str(encrypted_data[field]).encode())
                    # Base64로 인코딩하여 저장
                    encrypted_data[f"{field}_encrypted"] = base64.b64encode(encrypted_bytes).decode()
                    # 원본 데이터 제거
                    del encrypted_data[field]
            
            return {
                "status": "success",
                "message": "민감 데이터 암호화 완료",
                "encrypted_data": encrypted_data
            }
            
        except Exception as e:
            return {"status": "error", "message": f"암호화 실패: {str(e)}"}
    
    async def decrypt_sensitive_data(self, encrypted_data: Dict[str, Any], user_id: str, **kwargs) -> Dict[str, Any]:
        """암호화된 데이터 복호화"""
        try:
            fernet = Fernet(self.encryption_key)
            
            # 암호화된 필드들 복호화
            sensitive_fields = ['ssn', 'bank_account', 'phone', 'address', 'email']
            decrypted_data = encrypted_data.copy()
            
            for field in sensitive_fields:
                encrypted_field = f"{field}_encrypted"
                if encrypted_field in decrypted_data and decrypted_data[encrypted_field]:
                    # Base64 디코딩 후 복호화
                    encrypted_bytes = base64.b64decode(decrypted_data[encrypted_field])
                    decrypted_bytes = fernet.decrypt(encrypted_bytes)
                    decrypted_data[field] = decrypted_bytes.decode()
                    # 암호화된 필드 제거
                    del decrypted_data[encrypted_field]
            
            return {
                "status": "success",
                "message": "데이터 복호화 완료",
                "decrypted_data": decrypted_data
            }
            
        except Exception as e:
            return {"status": "error", "message": f"복호화 실패: {str(e)}"}
    
    async def backup_user_data(self, user_id: str, backup_type: str = "full", **kwargs) -> Dict[str, Any]:
        """사용자 데이터 백업"""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{user_id}_{backup_type}_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # 사용자 데이터 수집
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            backup_data = {
                "user_id": user_id,
                "backup_type": backup_type,
                "timestamp": timestamp,
                "data": {}
            }
            
            # 사용자 프로필
            cursor.execute("SELECT profile_data FROM user_profiles WHERE user_id = ?", (user_id,))
            profile_result = cursor.fetchone()
            if profile_result:
                backup_data["data"]["profile"] = json.loads(profile_result[0])
            
            # 경제 가정
            cursor.execute("SELECT scenario_type, assumptions_data FROM economic_assumptions WHERE user_id = ?", (user_id,))
            assumptions_results = cursor.fetchall()
            backup_data["data"]["economic_assumptions"] = {}
            for row in assumptions_results:
                backup_data["data"]["economic_assumptions"][row[0]] = json.loads(row[1])
            
            # 투자 포트폴리오
            cursor.execute("SELECT portfolio_id, portfolio_data FROM investment_portfolios WHERE user_id = ?", (user_id,))
            portfolio_results = cursor.fetchall()
            backup_data["data"]["portfolios"] = {}
            for row in portfolio_results:
                backup_data["data"]["portfolios"][row[0]] = json.loads(row[1])
            
            conn.close()
            
            # 백업 파일 저장
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            # 백업 기록 저장
            backup_id = f"backup_{user_id}_{timestamp}"
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO backup_records (backup_id, user_id, backup_type, file_path, file_size) VALUES (?, ?, ?, ?, ?)",
                (backup_id, user_id, backup_type, backup_path, os.path.getsize(backup_path))
            )
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": "데이터 백업 완료",
                "backup_id": backup_id,
                "file_path": backup_path,
                "file_size": os.path.getsize(backup_path)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"백업 실패: {str(e)}"}
    
    async def restore_user_data(self, backup_id: str, user_id: str, **kwargs) -> Dict[str, Any]:
        """사용자 데이터 복원"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 백업 기록 조회
            cursor.execute(
                "SELECT file_path FROM backup_records WHERE backup_id = ? AND user_id = ?",
                (backup_id, user_id)
            )
            result = cursor.fetchone()
            
            if not result:
                return {"status": "error", "message": "백업 파일을 찾을 수 없습니다."}
            
            backup_path = result[0]
            
            if not os.path.exists(backup_path):
                return {"status": "error", "message": "백업 파일이 존재하지 않습니다."}
            
            # 백업 데이터 로드
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # 데이터 복원
            if "profile" in backup_data["data"]:
                cursor.execute(
                    "INSERT OR REPLACE INTO user_profiles (user_id, profile_data) VALUES (?, ?)",
                    (user_id, json.dumps(backup_data["data"]["profile"], ensure_ascii=False))
                )
            
            if "economic_assumptions" in backup_data["data"]:
                for scenario_type, assumptions in backup_data["data"]["economic_assumptions"].items():
                    cursor.execute(
                        "INSERT OR REPLACE INTO economic_assumptions (user_id, scenario_type, assumptions_data) VALUES (?, ?, ?)",
                        (user_id, scenario_type, json.dumps(assumptions, ensure_ascii=False))
                    )
            
            if "portfolios" in backup_data["data"]:
                for portfolio_id, portfolio_data in backup_data["data"]["portfolios"].items():
                    cursor.execute(
                        "INSERT OR REPLACE INTO investment_portfolios (user_id, portfolio_id, portfolio_data) VALUES (?, ?, ?)",
                        (user_id, portfolio_id, json.dumps(portfolio_data, ensure_ascii=False))
                    )
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": "데이터 복원 완료",
                "restored_data": list(backup_data["data"].keys())
            }
            
        except Exception as e:
            return {"status": "error", "message": f"복원 실패: {str(e)}"}
    
    async def list_backups(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """백업 목록 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT backup_id, backup_type, file_path, file_size, created_at FROM backup_records WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            results = cursor.fetchall()
            
            backups = []
            for row in results:
                backups.append({
                    "backup_id": row[0],
                    "backup_type": row[1],
                    "file_path": row[2],
                    "file_size": row[3],
                    "created_at": row[4],
                    "exists": os.path.exists(row[2])
                })
            
            conn.close()
            
            return {
                "status": "success",
                "message": f"백업 목록 조회 완료 (총 {len(backups)}개)",
                "backups": backups
            }
            
        except Exception as e:
            return {"status": "error", "message": f"백업 목록 조회 실패: {str(e)}"}
    
    async def cleanup_old_backups(self, user_id: str, days_to_keep: int = 30, **kwargs) -> Dict[str, Any]:
        """오래된 백업 정리"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 오래된 백업 조회
            cursor.execute(
                "SELECT backup_id, file_path FROM backup_records WHERE user_id = ? AND created_at < ?",
                (user_id, cutoff_date.strftime("%Y-%m-%d %H:%M:%S"))
            )
            old_backups = cursor.fetchall()
            
            deleted_count = 0
            deleted_files = []
            
            for backup_id, file_path in old_backups:
                # 파일 삭제
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                
                # DB에서 기록 삭제
                cursor.execute("DELETE FROM backup_records WHERE backup_id = ?", (backup_id,))
                deleted_count += 1
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": f"오래된 백업 {deleted_count}개 정리 완료",
                "deleted_files": deleted_files,
                "deleted_count": deleted_count
            }
            
        except Exception as e:
            return {"status": "error", "message": f"백업 정리 실패: {str(e)}"}
