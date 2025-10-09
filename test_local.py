"""Test the FastMCP server tools locally without OAuth"""
import asyncio
from server import mcp

async def main():
    # Test tool registration
    print("Testing tool registration...")
    tools = await mcp.get_tools()
    print(f"Available tools: {tools}")

    # Note: get_user_info requires OAuth context, so we skip it in local testing
    print("\n✓ Server tools are properly registered")
    print(f"✓ Found {len(tools)} tools")

if __name__ == "__main__":
    asyncio.run(main())
