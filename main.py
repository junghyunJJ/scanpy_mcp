from server import mcp

from tools.read import read_sc
from tools.prep import qc_plot
from tools.prep import prep_filtering


if __name__ == "__main__":
  print("Starting MCP server...")
  mcp.run(transport="stdio")
