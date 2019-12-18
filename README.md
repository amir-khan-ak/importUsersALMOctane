# ALM Octane Tools
# importUsers.py
This python scripts uses the data from an excel file (sample file provided) to import users into ALM Octane. During the upload, the script will only create the users, workspaces and roles have to exist prior import. 

# Pre-requisites
- Download & Install Python 3.8 or higher: https://www.python.org/downloads/
- Install pandas library - https://pypi.org/project/pandas/
- Install requests library - https://pypi.org/project/requests/2.7.0/

# Usage
Using commandline run:
cd "directory where importUsers.py is located"
python importUsers.py <url> <shared_space_id> <client_id> <client_secret> <path_to_excel_file_with_users.xls>

# Parameters
<url> ALM Octane URL in the exact format as follow: http(s)://<serverhost>:<port> 
<shared_space_id> shared_space id where the users should be imported
<client_id> client id which is generated on the shared space level - this client id should be link to all workspaces which are included in the excel file.
<client_secret> client secret of the client id.
<path_to_excel_file_with_users.xls> the full path to the upload excel containing the users

# Example: 
cd C:\importUsers
C:\importUsers>python importUsers.py "https://112.133.5.18:8481" "1001" "webhooks_lke98dje3qi65my2w9kxv3" ")184sade31rr3eW" "C:\\ALM Octane Tools\\import_users.xlsx"

