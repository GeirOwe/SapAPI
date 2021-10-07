import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
CLIENT_ID = os.environ.get("CLIENT_ID") # Application (client) ID of app registration
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

TENANT = '3aa4a235-b6e2-48d5-9195-7fcf05b459b0'
AUTHORITY = "https://login.microsoftonline.com/" + TENANT

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

#the url and scope for the api we are to connect to (defined in azure portal for the api)
ENDPOINT = 'https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet'  
SCOPE = ["api://ff7b420c-0c08-4e72-826b-b531bfc1dbc0/Products.Read"]

#basicPL apiet
SCOPEPL = ["https://StatoilSRM.onmicrosoft.com/1259e78a-ae07-4035-838c-2d5168271456/user_impersonation"]
ENDPOINTPL = "https://api.gateway.equinor.com/basic-pl-api-employee-internal/v1/Employee"
REDIRECT_PATHPL = "/getAToken"

#SCMDev apiet
SCOPESCM=["api://f5e64196-527b-4bc2-8338-d8bf4075f6e0/SCMAPIDev"]
ENDPOINTSCM = "https://api-dev.gateway.equinor.com/scm-api/v1/Ping"
REDIRECT_PATHPL="/getAToken"

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

API_BASE = os.environ.get('API_BASE')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
TENANT_ID = os.environ.get('TENANT_ID')