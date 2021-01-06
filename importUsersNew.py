import json
import sys
import pandas as pd
import requests

# define variables for accessing octane rest api

url = "https://almoctane-eur.saas.microfocus.com" #sys.argv[1]
shared_space = "306003" #sys.argv[2]
ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true', 'HPECLIENTTYPE':'ALM_OCTANE_TECH_PREVIEW'}
excel_path = "C:\\tmp\\import_users.xlsx" #sys.argv[5]
client_id = "test_6l2x8jpzdjpvxi093vxxy8ewv" #sys.argv[3]
client_secret = "?13918716813521331225232Q" #sys.argv[4]

data_xls = pd.read_excel(excel_path)

# Login to Octane
resource = 'authentication/sign_in'
payload = {"client_id": client_id, "client_secret": client_secret}
resp = requests.post(url + '/' + resource,
                     data=json.dumps(payload),
                     headers=ContentType)

cookie = resp.cookies
print('Login: ' + str(resp.status_code))

print(data_xls)
print('Total Rows in Excel: ' + str(data_xls.shape[0]))
for i in range(data_xls.shape[0]):

    # get workspaces
    a_workspace = data_xls.workspaces[i].split(";")

    for a_ws in a_workspace:
        resource = 'workspaces?query="name EQ ^' + a_ws + '^"'
        workspaces = requests.get(url + '/api/shared_spaces/' + shared_space + '/' + resource,
                                  headers=ContentType,
                                  cookies=cookie)

        print('Getting Workspaces: ' + str(workspaces.status_code))
        workspaces_data = workspaces.json()
        workspaces_total_count = workspaces_data['total_count']
        workspaces_list = workspaces_data['data']
        print('Total Workspaces Found: ' + str(workspaces_total_count))

        workspace = workspaces_list[0]['id']
        resource = 'workspace_users'
        workspaces = requests.get(
            url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
            headers=ContentType,
            cookies=cookie)

        a_roles = data_xls.roles[i].split(";")
        resource = 'workspace_roles?query="role EQ {name IN '
        for a_role in a_roles:
            resource = resource + '^' + a_role + '^,'


        resource = resource[:-1] + '};workspace EQ {id EQ ^' + workspace + '^}""'
        roles = requests.get(
            url + '/api/shared_spaces/' + shared_space +  '/' + resource,
            headers=ContentType,
            cookies=cookie)
        roles_data = roles.json()
        roles_list = roles_data['data']
        userroles = "["
        for role in roles_list:
            userroles = userroles + '{"type": "workspace_role", "id":"' + role['id'] + '"},'

        userroles = json.loads(userroles[:-1] + ']')
        userdata = {
            "data": [
                {
                    "email": data_xls.email[i],
                    "first_name": data_xls.firstname[i],
                    "last_name": data_xls.lastname[i],
                    "name": data_xls.loginname[i],
                    "phone1": str(data_xls.telephone[i]),
                    "workspace_roles": {
                        "data":
                            userroles

                    }
                }
            ]
        }
        print('Json payload: ' + str(userdata))
        resource = 'users?fetch_single_entity=true'
        resp = requests.post(url + '/api/shared_spaces/' + shared_space + '/' + resource,
                             data=json.dumps(userdata),
                             headers=ContentType,
                             cookies=cookie)
        print('User created: ' + str(resp.status_code))
        if resp.status_code == 409:
            print('User already exist in workspace: ' + workspace + ' - ' + data_xls.email[i] + ' - Please check'+ ' username or email.')
            print(resp.text)
            print(str(resp.headers))
            print(str(resp.content))                                                                                  

#######################
# Logout from Octane
resource = 'authentication/sign_out'
resp = requests.post(url + '/' + resource,
                     data=json.dumps(payload),
                     headers=ContentType,
                     cookies=cookie)
print('Logout: ' + str(resp.status_code))
