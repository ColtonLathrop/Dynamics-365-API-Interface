# Dynamics-365-API-Interface
Currently a simple class that handles the authentication via user impersonation with an Azure Client to O365.

Features:
Automatically handles the token refreshes as needed
Allows execution of the webapi with json response

Designed to be the interface for the webapi requests, all data handling would be done outside of the class.

Class object is created with the following parameters:

(self, publicorgname, username, password, clientid, tenantid, crmdblocation)

if org url == supportrepro.crm.dynamics.com:
  publicorgname = "supportrepro"
  crmdblocation = "crm"
tenantid = AAD directory ID (Available in the Azure portal properties)
clientid = Azure App Registration Application ID (Create as a Native App, be sure to grant all permissions for impersonation)
username & password = credentials for user the application will impersonate

Class methods and attributes:

Methods:
login() - for manually retrieving the access token. Takes no parameters. fired due to check prior to webapi call.
execute(uri) - takes single parameter as the odata call. Example: '/contacts?$select=fullname,contactid'
  Assumes api version 8.2
printvariable(select=None) - returns the active attributes of the class

Attributes:
headers = the http request headers with the current access token (not initialized until webapoi request is fired)
tokenexpiration = datetime object thats generated when login() is ran to track when the token should expire
token = Access token used in the uaht headers to make webapi calls
tokenendpoint = the endpoint used by login()to authenticate
crmorgurl = is the built crm org url to pass in login()

Example Code:

import ConnectionClass as con

connection = con.Connection('microsoft', 'admin@microsoft.onmicrosoft.com', 'password',
                            'd3d6f571-dbfc-47a7-933d-51620c5faaac', '05651e63-2d6b-4116-92fe-d3db88bf4dd3', 'crm4')
connection.execute('/accounts?$select=accountid')


     






