from yaml import safe_load
import json
class ArgoWF:
    def __init__(self, wftext):
        self.wfdict = safe_load(wftext)
    def add_argo_variables(self, addvariables):
        for template in self.wfdict['spec']['templates']:
            if 'script' in template.keys():
                template['script']['env'].extend(addvariables)
    def add_obc_file_download(self, run_key, fname, server_url):
        for template in self.wfdict['spec']['templates']:
            if template['name'] == 'SCRIPTOBCINIT':
                # Found the init script
                template['script']['source'] += '\n'
                template['script']['source'] += f'curl {server_url}/wfforms/files/{run_key}/{fname} > ${{OBC_WORK_PATH}}/{fname}'
                break
    def add_obc_download_preamble(self):
        for template in self.wfdict['spec']['templates']:
            if template['name'] == 'SCRIPTOBCINIT':
                template['script']['source'] += '\napt-get update\napt-get -y install curl\n'
                break
    def dump_json_for_argo_api(self):
        # Argo API expects workflow encapsulated in a JSON workflow field:
        rv = {'workflow': self.wfdict}
        return json.dumps(rv)

