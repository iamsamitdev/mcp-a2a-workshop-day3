from fastmcp import FastMCP
import pandas as pd
from typing import Optional
from src.utils.validation import get_safe_path, clean_nans, DATA_DIR

def register_csv_tools(mcp: FastMCP):

    # Tool to list all CSV files in the data directory
    @mcp.tool()
    def list_csv_files(
        sessionId: Optional[str] = None, 
        action: Optional[str] = None, 
        chatInput: Optional[str] = None, 
        toolCallId: Optional[str] = None) -> list[str]:
        """
        แสดงรายชื่อไฟล์ CSV ที่พร้อมใช้งานใน data
        """
        # ตรวจสอบว่าโฟลเดอร์มีอยู่จริงก่อน glob
        if not DATA_DIR.exists():
            return []
        return [p.name for p in DATA_DIR.glob("*.csv")]


    # Tool to summarize a specific CSV file
    @mcp.tool()
    def summarize_csv(
        file_name: str, 
        sessionId: Optional[str] = None, 
        action: Optional[str] = None, 
        chatInput: Optional[str] = None, 
        toolCallId: Optional[str] = None) -> dict:
        """
        สรุปข้อมูลไฟล์ CSV (จำนวนแถว, คอลัมน์, ตัวอย่างหัวตาราง, สถิติรวมของคอลัมน์ตัวเลข)
        """
        safe_path = get_safe_path(file_name)
        df = pd.read_csv(safe_path)

        summary = {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "columns": df.columns.tolist(),
            "head": clean_nans(df.head().to_dict(orient="records")),
            "describe": clean_nans(df.describe().to_dict())
        }
        return summary


    # Tool to read rows with pagination
    @mcp.tool()
    def read_csv_rows(
        file_name: str, 
        offset: int = 0, 
        limit: int = 10,
        sessionId: Optional[str] = None, 
        action: Optional[str] = None, 
        chatInput: Optional[str] = None, 
        toolCallId: Optional[str] = None) -> list[dict]:
        """
        อ่านข้อมูลจากไฟล์ CSV แบบระบุจำนวนแถว (Pagination)
        """
        file_path = get_safe_path(file_name)
        df = pd.read_csv(file_path)
        
        if offset >= len(df):
            return []
        
        # Clean NaN ก่อนส่งกลับ
        result_df = clean_nans(df.iloc[offset : offset + limit])
        return result_df.to_dict(orient="records")


    # Tool to get unique values
    @mcp.tool()
    def get_unique_values(
        file_name: str, 
        column_name: str, 
        sessionId: Optional[str] = None, 
        action: Optional[str] = None, 
        chatInput: Optional[str] = None, 
        toolCallId: Optional[str] = None) -> list:
        """
        ดึงค่าที่ไม่ซ้ำกัน (Unique values) จากคอลัมน์ที่ระบุ
        """
        file_path = get_safe_path(file_name)
        df = pd.read_csv(file_path)
        
        if column_name not in df.columns:
            raise ValueError(f"ไม่พบคอลัมน์ {column_name} ในไฟล์ {file_name}")
        
        # dropna() เพื่อไม่ส่งค่าว่างกลับไป
        values = df[column_name].dropna().unique().tolist()
        return values
        
    
    # Tool to filter data using pandas query
    @mcp.tool()
    def filter_csv(
        file_name: str, 
        query: str, 
        sessionId: Optional[str] = None, 
        action: Optional[str] = None, 
        chatInput: Optional[str] = None, 
        toolCallId: Optional[str] = None) -> list[dict]:
        """
        กรองข้อมูล CSV ด้วย query string (ใช้ syntax ของ pandas query)
        
        ตัวอย่างการใช้งาน:
        - "age > 25"
        - "department == 'Sales' and salary > 50000"
        - "product_name.str.contains('Pro', case=False)"
        """
        file_path = get_safe_path(file_name)
        df = pd.read_csv(file_path)
        
        try:
            result = df.query(query, engine='python')
            return clean_nans(result).to_dict(orient="records")
        except Exception as e:
            raise ValueError(f"Query Error: {str(e)}")