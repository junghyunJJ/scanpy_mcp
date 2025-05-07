
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

4. **Add the MCP to Claude**:  
   Edit the Claude config file located at:

   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   Add the following entry to the `"mcpServers"` section:

   ```json
   {
     "mcpServers": {
       "scanpy_mcp": {
         "command": "uv",
         "args": [
           "--directory",
           "{path_to_directory_containing_main.py}",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```
