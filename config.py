import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
CLIENT_ID = os.environ.get("CLIENT_ID") # Application (client) ID of app registration
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

TENANT = '3aa4a235-b6e2-48d5-9195-7fcf05b459b0'
AUTHORITY = "https://login.microsoftonline.com/" + TENANT

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

ENDPOINT = 'https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet'  

SCOPE = ["api://ff7b420c-0c08-4e72-826b-b531bfc1dbc0/Products.Read"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

API_BASE = os.environ.get('API_BASE')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
TENANT_ID = os.environ.get('TENANT_ID')