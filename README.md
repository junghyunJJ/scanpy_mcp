
## `scanpy_mcp` Tutorial & Setup Instructions

1. **Check the Scanpy tutorial**:  
   👉 [Scanpy clustering tutorial (3k PBMCs)](https://scanpy.readthedocs.io/en/stable/tutorials/basics/clustering-2017.html)

2. **Download the 3k PBMC dataset from 10X Genomics**:  
   Run the following command to download the dataset:

   ```bash
   wget https://cf.10xgenomics.com/samples/cell-exp/1.1.0/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz
   ```

3. **Set up the Python environment**:  
   Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/junghyunJJ/scanpy_mcp.git
   cd scanpy_mcp
   uv sync --python=python3.10
   source .venv/bin/activate
   ```

4. **Project structure**:
   ```
   scanpy_mcp
   ├── data
   │   └── filtered_gene_bc_matrices
   │       └── hg19
   │           ├── barcodes.tsv
   │           ├── genes.tsv
   │           └── matrix.mtx
   ├── main.py
   ├── pyproject.toml
   ├── README.md
   ├── requirements.txt
   ├── server.py
   ├── tools
   │   ├── prep.py
   │   └── read.py
   ├── utils
   │   └── prep.py
   └── uv.lock
   ```

5. **Configure OAuth credentials**:

   a. **Create Google OAuth credentials**:
      - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
      - Create OAuth 2.0 Client ID (Application type: Web application)
      - Add authorized redirect URIs:
        - `http://localhost:*/callback` (for local development)
        - `https://your-domain.fastmcp.app/oauth2/callback` (for deployment)
      - Copy Client ID and Client Secret

   b. **Set up environment variables**:
      ```bash
      cp .env.example .env
      # Edit .env with your credentials:
      # GOOGLE_CLIENT_ID=your-client-id
      # GOOGLE_CLIENT_SECRET=your-client-secret
      # GOOGLE_BASE_URL=https://your-domain.fastmcp.app
      ```

   ⚠️ **SECURITY**: Never commit `.env` file to version control. It's already in `.gitignore`.

6. **Add the MCP to Claude**:
   Edit the Claude config file located at:

   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   Add the following entry to the `"mcpServers"` section:

   ```json
   {
     "mcpServers": {
       "scanpy_mcp": {
         "command": "/Users/jungj2/.local/bin/uv",
         "args": [
           "--directory",
           "/path/to/scanpy_mcp",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

## Security Best Practices

### Credential Management

**DO**:
- ✅ Store credentials in `.env` file (excluded from git)
- ✅ Use environment variables in code
- ✅ Copy `.env.example` as template
- ✅ Use FastMCP secrets for deployment: `fastmcp secret set KEY value`
- ✅ Rotate credentials if exposed

**DON'T**:
- ❌ Commit credentials to version control
- ❌ Hard-code credentials in source files
- ❌ Share `.env` file publicly
- ❌ Reuse exposed credentials

### Deployment with FastMCP

```bash
# Set secrets for deployment
fastmcp secret set GOOGLE_CLIENT_ID "your-client-id"
fastmcp secret set GOOGLE_CLIENT_SECRET "your-client-secret"
fastmcp secret set GOOGLE_BASE_URL "https://your-domain.fastmcp.app"

# Deploy server
fastmcp deploy server.py
```

### If Credentials Are Exposed

1. **Immediately revoke** credentials in Google Cloud Console
2. **Generate new** OAuth Client ID and Secret
3. **Update** `.env` with new credentials
4. **Clean git history** to remove exposed secrets:
   ```bash
   git reset --soft HEAD~1
   git add -A
   git commit -m "Configure OAuth with environment variables"
   git push --force
   ```