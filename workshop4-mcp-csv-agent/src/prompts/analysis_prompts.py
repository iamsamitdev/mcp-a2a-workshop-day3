from fastmcp import FastMCP

def register_prompts(mcp: FastMCP):
    
    @mcp.prompt()
    def analyze_monthly_report(filename: str) -> str:
        """แม่แบบสำหรับสั่งให้ AI วิเคราะห์รายงานประจำเดือน"""
        return f"""
        คุณคือผู้เชี่ยวชาญด้าน Data Analyst
        1. กรุณาอ่านไฟล์ CSV ชื่อ: {filename}
        2. สรุปยอดขายรวม และแนวโน้มที่น่าสนใจ
        3. หาความผิดปกติของข้อมูล (Anomalies)
        4. ตอบกลับในรูปแบบ Markdown Table
        """

    @mcp.prompt()
    def debug_csv_format() -> str:
        """แม่แบบสำหรับช่วยแก้ปัญหาไฟล์ CSV"""
        return "ช่วยตรวจสอบโครงสร้างไฟล์ CSV นี้หน่อยว่าถูกต้องตามมาตรฐานหรือไม่ และมีคอลัมน์ไหนหายไปบ้าง"