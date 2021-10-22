# openbio_forms
Create forms from your OpenBio.eu workflows
## Installation (using conda)
Input the following commands in a shell:
```
# Create venv
conda create -n wc_dbg python=3.9
conda activate wc_dbg
# Install dependencies
pip install Django pyyaml 
```
## Configuration
Create a file named `secrets.py` in `wfforms/workflow_forms`, with the following content:
```python
argo_token = 'Bearer v2:...' # Your Argo API authentication token
argo_server = 'https://argoserver.argodomain' # URL of your Argo server (with protocol scheme)
argo_namespace = 'your-namespace' # Argo namespace you are authorized to write to
```
## Execution
From the root of the repository, `cd` to the `wfforms` directory. Then, having activated the venv you created during installation, simply run:
```
python manage.py runserver
```
