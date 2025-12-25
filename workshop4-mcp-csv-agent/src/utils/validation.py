import pandas as pd
import os
from pathlib import Path

# --- 1. การหา Path แบบ Robust (ไม่สนว่ารันจากไหน) ---
# โครงสร้าง: workshop4-mcp-csv-agent/src/utils/validation.py
# .parents[0] = utils
# .parents[1] = src
# .parents[2] = workshop4-mcp-csv-agent (Project Root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# กำหนด DATA_DIR จาก Root เสมอ
DATA_DIR = PROJECT_ROOT / "data"

# --- Helper Function: ป้องกัน Path Traversal ---
def get_safe_path(filename: str) -> Path:
    """ตรวจสอบความปลอดภัยของ Path และคืนค่า Absolute Path"""
    
    # ถ้าโฟลเดอร์ data ยังไม่มี ให้สร้างรอไว้เลย (Optional)
    if not DATA_DIR.exists():
        os.makedirs(DATA_DIR, exist_ok=True)

    safe_path = (DATA_DIR / filename).resolve()
    
    # ตรวจสอบว่า path ที่ได้ ยังคงอยู่ภายใต้ DATA_DIR หรือไม่
    if not str(safe_path).startswith(str(DATA_DIR.resolve())):
        raise ValueError(f"Access denied: ไม่สามารถเข้าถึงไฟล์นอกโฟลเดอร์ data ได้ ({filename})")
    
    if not safe_path.exists():
        # แก้ไขชื่อตัวแปรให้ตรงกับ parameter (filename)
        raise FileNotFoundError(f"ไม่พบไฟล์ {filename} ในโฟลเดอร์ data") 
        
    return safe_path


# --- Helper Function: แปลง NaN เป็น None ---
def clean_nans(data):
    """Helper: แปลง NaN เป็น None เพื่อให้ JSON Compatible"""
    if isinstance(data, (pd.DataFrame, pd.Series)):
        return data.where(pd.notnull(data), None)
    return data