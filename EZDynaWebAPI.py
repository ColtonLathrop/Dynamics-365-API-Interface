import requests
import json
from datetime import date, datetime, time, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Msolauth():
    # Connection class is use to manage your API token and refresh as needed

    def __init__(self, publicorgname, username, password, clientid, tenantid, crmdblocation):
        # String pre-fix to crm subdomain
        self.publicorgname = publicorgname
        # String O365 login (typically emailaddress)
        self.username = username
        self.password = password
        # String Azure Application ID (Must be authorized for CRM)
        self.clientid = clientid
        # String Azure AD DirectoryID - AAD -> Overview -> Properties
        self.tenantid = tenantid
        # String for the CRM GEO I.E. crm, crm4, crm3
        self.crmdblocation = crmdblocation
        #sets current token expiration to now to default the login()
        self.tokenexpiration = datetime.utcnow()
        self.apiurl = 'https://' + publicorgname + '.api.crm.dynamics.com/api/data/v8.2'
        self.token = None

        self.tokenendpoint = 'https://login.microsoftonline.com/' + tenantid + '/oauth2/token'
        self.crmorgurl = 'https://' + publicorgname + '.' + crmdblocation + '.dynamics.com'

        self.authdata = {
            'client_id': self.clientid,
            'resource': self.crmorgurl,
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
        }


    def login(self):
        response = requests.post(self.tokenendpoint, data=self.authdata, verify=False)
        #checks if response from token request was valid and returns response
        if response.status_code != 200:
            print("There was an error with the request.")
            print("HTTP response is as follows:" + str(response.status_code))
            print(response.text)
        #try to pull access_token from json request
        if response.status_code == 200:
            try:
                self.token = response.json()['access_token']
                timeout = response.json()['expires_in']
                timeout = int(timeout)/60
                self.tokenexpiration = self.tokenexpiration + timedelta(minutes=int(timeout))
            except(KeyError):
                print("Unable to find Access Token within:")
                print(response.json())


    def execute(self, odatarequest):
        if self.token == None:
            self.login()
        if self.tokenexpiration <= datetime.now():
            self.login()
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Prefer': 'odata.maxpagesize=500',
            'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
        }
        response = requests.get(self.apiurl + odatarequest, headers=self.headers, verify=False)
        return response.json()


    def printvariable(self, select=None):
        if select == None:
            print({
                'publicorgname': self.publicorgname,
                'username': self.username,
                'password': self.password,
                'clientid': self.clientid,
                'tentantid': self.tenantid,
                'crmdblocation': self.crmdblocation,
                'tokenendpoint': self.tokenendpoint,
                'crmorgurl': self.crmorgurl,
                'authdata': self.authdata
            })
        if select == 'publicorgname':
            #print(self.publicorgname)
            return self.publicorgname
        if select == 'username':
            #print(self.username)
            return self.username
        if select == 'password':
            #print(self.password)
            return self.password
        if select == 'clientid':
            #print(self.clientid)
            return self.clientid
        if select == 'tentantid':
            #print(self.tenantid)
            return self.tenantid
        if select == 'crmdblocation':
            #print(self.crmdblocation)
            return self.crmdblocation
        if select == 'tokenendpoint':
            #print(self.tokenendpoint)
            return tokenendpoint
        if select == 'authdata':
            #print(self.authdata)
            return authdata
        else:
            #print('No object selected')
            return "Error: " + select + " does not exist as a valid init variable."
