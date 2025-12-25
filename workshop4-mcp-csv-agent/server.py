from fastmcp import FastMCP
from src.tools.csv_tools import register_csv_tools
from src.prompts.analysis_prompts import register_prompts
from src.resources.system_resources import register_resources

# 1. Initialize
mcp = FastMCP("mcp-csv-agent")

# 2. Register Tools (ส่ง mcp ไปให้ csv_tools ช่วยแปะ)
register_csv_tools(mcp)

# 3. Register Prompts
register_prompts(mcp)

# 4. Register Resources
register_resources(mcp)

# 5. Run
if __name__ == "__main__":
    print("🚀 Server starting with Tools, Prompts, and Resources loaded!")
    mcp.run(transport="http", host="0.0.0.0", port=8000)