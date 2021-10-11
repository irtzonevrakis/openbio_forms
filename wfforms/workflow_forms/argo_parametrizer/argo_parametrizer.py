from yaml import safe_load, safe_dump

def add_argo_variables(wftext, addvariables):
    wfdict = safe_load(wftext)
    for template in wfdict['spec']['templates']:
        if 'script' in template.keys():
            template['script']['env'].extend(addvariables)
    return safe_dump(wfdict)

def add_obc_file_download(wftext, run_key, fname, server_url):
    wfdict = safe_load(wftext)
    for template in wfdict['spec']['templates']:
        if template['name'] == 'SCRIPTOBCINIT':
            # Found the init script
            template['script']['source'] += '\n'
            template['script']['source'] += f'curl {server_url}/wfforms/files/{run_key}/{fname} > ${{OBC_WORK_PATH}}/{fname}'
            break
    return safe_dump(wfdict)

def add_obc_download_preamble(wftext):
    wfdict = safe_load(wftext)
    for template in wfdict['spec']['templates']:
        if template['name'] == 'SCRIPTOBCINIT':
            template['script']['source'] += '\napt-get update\napt-get -y install curl\n'
            break
    return safe_dump(wfdict)
