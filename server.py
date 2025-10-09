import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from utils.prep import read_10x_mtx
from fastmcp.server.auth.providers.google import GoogleProvider

# Load environment variables from .env file
load_dotenv()

# Validate required environment variables
required_vars = ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_BASE_URL"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}\n"
        f"Please copy .env.example to .env and configure your credentials."
    )

# The GoogleProvider handles Google's token format and validation
auth_provider = GoogleProvider(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),           # From environment
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),   # From environment
    base_url=os.getenv("GOOGLE_BASE_URL"),             # From environment
    required_scopes=[                                   # Request user information
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    # redirect_path="/auth/callback"                   # Default value, customize if needed
)


mcp = FastMCP("scanpy_mcp", auth=auth_provider)


# Add a protected tool to test authentication
@mcp.tool()
async def get_user_info() -> dict:
    """Returns information about the authenticated Google user."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()
    # The GoogleProvider stores user data in token claims
    return {
        "google_id": token.claims.get("sub"),
        "email": token.claims.get("email"),
        "name": token.claims.get("name"),
        "picture": token.claims.get("picture"),
        "locale": token.claims.get("locale")
    }


@mcp.tool()
def read_sc(
  filename: str, 
  savedir: str
) -> str:
  """
  Read in the count matrix (i.e., matrix.mtx) into an AnnData object (https://anndata.readthedocs.io/en/stable/), 
  which holds many slots for annotations and different representations of the data.
  It also comes with its own HDF5-based file format: .h5ad.

  Args:
    filename: the directory with the `.mtx` file

  Returns:
    AnnData object
  """
  adata = read_10x_mtx(filename)
  
  savedir = f"{savedir}/adata.h5ad"
  adata.write_h5ad(savedir)
  
  return savedir
