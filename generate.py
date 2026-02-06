import json
from urllib.parse import quote

branch_names = {}
branch_names['asm-api'] = 'main'
branch_names['declarative-pipeline-migration-assistant-api'] = 'main'
branch_names['json-api'] = 'main'
branch_names['json-path-api'] = 'main'

branch_names['pipeline-stage-tags-metadata'] = 'main'
branch_names['plugin-util-api'] = 'main'
branch_names['prism-api'] = 'main'
branch_names['saml'] = 'main'
branch_names['ssh-agents'] = 'main'
branch_names['sshd'] = 'main'
branch_names['token-macro'] = 'main'
branch_names['trilead-api'] = 'main'
branch_names['warnings-ng'] = 'main'

exclusions = []
exclusions.append('declarative-pipeline-migration-assistant-api')
exclusions.append('pipeline-stage-tags-metadata')

repository_names = {}
repository_names['ssh-slaves'] = 'ssh-agents'

def section(name, src_file):
    with open(src_file) as json_data:
        d = json.load(json_data)
        d.sort()
        print('')
        print('## ' + name)
        print('')
        for item in d:
            my_id = item[0]
            if my_id in repository_names:
                my_id = repository_names[my_id]
            my_desc = quote(item[1])
            if my_id in exclusions:
                continue
            if my_id in branch_names:
                my_branch = branch_names[my_id]
            else:
                my_branch = 'master'
            template = '[![{id}](https://ci.jenkins.io/buildStatus/icon?job=Plugins%2F{id}-plugin%2F{branch}&subject={desc})](https://ci.jenkins.io/job/Plugins/job/{id}-plugin/job/{branch}/)'
            print(template.format(id = my_id, desc = my_desc, branch = my_branch))

section('Verified', 'verified.json')
section('Compatible', 'compatible.json')
