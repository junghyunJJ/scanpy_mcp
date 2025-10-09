from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle Google OAuth
    async with Client("https://scanpy-mcp-test2.fastmcp.app/mcp/", auth="oauth") as client:
        # First-time connection will open Google login in your browser
        print("✓ Authenticated with Google!")

        # List available tools (requires server to be deployed)
        try:
            tools = await client.list_tools()
            print(f"\nAvailable tools on server: {[t.name for t in tools]}")

            # Test the protected tool if available
            if any(t.name == "get_user_info" for t in tools):
                result = await client.call_tool("get_user_info", arguments={})
                print(f"\nGoogle user: {result.data['email']}")
                print(f"Name: {result.data['name']}")
            else:
                print("\nNote: Server needs to be deployed for tool access")
                print("Run: fastmcp deploy server.py")
        except Exception as e:
            print(f"\nNote: {e}")
            print("Server may not be deployed yet")

if __name__ == "__main__":
    asyncio.run(main())