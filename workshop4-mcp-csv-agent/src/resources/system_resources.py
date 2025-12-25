from fastmcp import FastMCP
from src.utils.validation import DATA_DIR

def register_resources(mcp: FastMCP):

    # Resource แบบ Static (ค่าคงที่)
    @mcp.resource("config://app-version")
    def get_app_version() -> str:
        return "CSV Agent v1.0.0 (Beta)"

    # Resource แบบ Dynamic (อ่านจากไฟล์จริง)
    @mcp.resource("csv://schema/{filename}")
    def get_csv_schema(filename: str) -> str:
        """อ่านแค่บรรทัดแรก (Header) ของไฟล์ CSV เพื่อดู Schema"""
        # (ควรใส่ logic get_safe_path ที่นี่ด้วย)
        file_path = DATA_DIR / filename
        if file_path.exists():
             with open(file_path, "r", encoding="utf-8") as f:
                 return f.readline().strip()
        return "Error: File not found"