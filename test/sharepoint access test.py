from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from requests_ntlm import HttpNtlmAuth
import requests

server_url = 'https://tbiholding.sharepoint.com/'
url_fill = ':f:/r/'
site_url = server_url + 'sites/DocumentManagementSysteem/'
folder_extention = 'Gedeelde%20documenten/General/Centrale%20opslag?csf=1&web=1&e=gj74AE'

username = 'croonwolterendros\\nilan.bais'
password = 'Focusrite2210-'


cred = HttpNtlmAuth('croonwolterendros\\nilan.bais', 'Focusrite2210-')  # On premise autentication

response = requests.get(site_url, auth=cred)
print(response.status_code)  # status_code = 403 --> 'forbidden'

authcookie = Office365(server_url, username='croonwolterendros\\nilan.bais', password=password).GetCookies()

site = Site(site_url, version=Version.v365, auth=authcookie)
