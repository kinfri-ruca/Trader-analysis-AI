import json
import os
from pathlib import Path
from typing import Optional, Dict, List

class DesktopCommanderClient:
    """MCP Desktop Commander 클라이언트"""
    
    def __init__(self, config_path: str = 'mcp_config.json'):
        self.config = self._load_config(config_path)
        self.data_dir = self.config.get('data_directory', 'data')
        
    def _load_config(self, config_path: str) -> Dict:
        """MCP 설정 로드"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 기본 설정
            return {
                'server': 'desktop-commander',
                'data_directory': 'data',
                'watch_files': [
                    'trading_transactions_enhanced.csv',
                    'analysis_results.json'
                ],
                'auto_refresh': True,
                'refresh_interval': 60
            }
    
    def read_csv(self, filename: str) -> Optional[str]:
        """CSV 파일 읽기"""
        file_path = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR] Failed to read {filename}: {e}")
            return None
    
    def read_json(self, filename: str) -> Optional[Dict]:
        """JSON 파일 읽기"""
        file_path = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read {filename}: {e}")
            return None
    
    def list_files(self, directory: Optional[str] = None) -> List[str]:
        """디렉토리 파일 목록"""
        target_dir = directory if directory else self.data_dir
        
        if not os.path.exists(target_dir):
            print(f"[ERROR] Directory not found: {target_dir}")
            return []
        
        try:
            files = os.listdir(target_dir)
            return [f for f in files if os.path.isfile(os.path.join(target_dir, f))]
        except Exception as e:
            print(f"[ERROR] Failed to list directory: {e}")
            return []
    
    def file_exists(self, filename: str) -> bool:
        """파일 존재 확인"""
        file_path = os.path.join(self.data_dir, filename)
        return os.path.exists(file_path)
    
    def get_file_info(self, filename: str) -> Optional[Dict]:
        """파일 정보 조회"""
        file_path = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(file_path):
            return None
        
        try:
            stat = os.stat(file_path)
            return {
                'name': filename,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'path': file_path
            }
        except Exception as e:
            print(f"[ERROR] Failed to get file info: {e}")
            return None
    
    def refresh_data(self) -> bool:
        """데이터 새로고침"""
        print("[INFO] Refreshing data...")
        
        # analysis_results.json 존재 확인
        if self.file_exists('analysis_results.json'):
            print("[OK] Data files are up to date")
            return True
        else:
            print("[WARNING] analysis_results.json not found. Run analyzer.py first.")
            return False
    
    def get_status(self) -> Dict:
        """시스템 상태 확인"""
        status = {
            'data_directory': self.data_dir,
            'files': {},
            'total_files': 0
        }
        
        for filename in self.config.get('watch_files', []):
            if self.file_exists(filename):
                info = self.get_file_info(filename)
                status['files'][filename] = 'OK' if info else 'ERROR'
                if info:
                    status['total_files'] += 1
            else:
                status['files'][filename] = 'NOT FOUND'
        
        return status

# 테스트
if __name__ == "__main__":
    client = DesktopCommanderClient()
    
    print("=== MCP Client Test ===\n")
    
    # Test 1: 파일 목록
    print("1. Files in data directory:")
    files = client.list_files()
    for f in files:
        print(f"   - {f}")
    
    # Test 2: JSON 읽기
    print("\n2. Read analysis_results.json:")
    data = client.read_json('analysis_results.json')
    if data:
        print(f"   Loaded {len(data)} traders")
    
    # Test 3: 상태 확인
    print("\n3. System status:")
    status = client.get_status()
    print(f"   Data dir: {status['data_directory']}")
    print(f"   Total files: {status['total_files']}")
    for fname, fstatus in status['files'].items():
        print(f"   - {fname}: {fstatus}")
    
    print("\n[OK] MCP Client ready")
