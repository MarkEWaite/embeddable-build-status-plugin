import json
from urllib.parse import quote

branch_names = {}
branch_names['asm-api'] = 'main'
branch_names['declarative-pipeline-migration-assistant-api'] = 'main'
branch_names['json-api'] = 'main'
branch_names['json-path-api'] = 'main'
branch_names['saml'] = 'main'
branch_names['ssh-agents'] = 'main'
branch_names['token-macro'] = 'main'

exclusions = []
exclusions.append('declarative-pipeline-migration-assistant-api')

with open('verified.json') as json_data:
    d = json.load(json_data)
    d.sort()
    for item in d:
        my_id = item[0]
        my_desc = quote(item[1])
        if my_id in exclusions:
            continue
        if my_id in branch_names:
            my_branch = branch_names[my_id]
        else:
            my_branch = 'master'
        template = '[![{id}](https://ci.jenkins.io/buildStatus/icon?job=Plugins%2F{id}-plugin%2F{branch}&subject={desc})](https://ci.jenkins.io/job/Plugins/job/{id}-plugin/job/{branch}/)'
        print(template.format(id = my_id, desc = my_desc, branch = my_branch))
