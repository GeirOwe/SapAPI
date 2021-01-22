#access ODATA thru a SAP API. The API is exposed in api.equinor.com and the ODATA are fecthed from D05
#auth done thru azure AD 

import os
import requests                         #the library in python 3.x best suited to read REST API

#start function
def check_if_error(response):
    #testing the response code -> 200 success. 401/403 no authorization. 404 not found    
    apiOK = False
    err_msg = ''
    
    #ok? empty data set?
    if response.status_code < 299:      
        emptyDataset = (len(response.json()) == 0)
        if emptyDataset: 
            err_msg = 'for some reason we can not provide the data today - even if the response is: ' + response.reason
            apiOK = False
        else:
            apiOK = True
    elif response.status_code == 403:
        err_msg = 'The Auth token is ok. Most likely some roles are missing in SAP backend ERP. Error code ' + str(response.status_code) + ' - ' + response.reason
    elif response.status_code == 401:
        err_msg = 'Most likely the token has gotten a timeout, refresh the token. Error code ' + str(response.status_code) + ' - ' + response.reason
    else:
        err_msg = 'error received from the API. Error code ' + str(response.status_code) + ' - ' + response.reason
    #if error the print error message
    if apiOK == False:
        print(err_msg)

    return apiOK
#end function

#start function
def get_token():
    #theToken = '<.. replace with token (from Postman) ..>'
    theToken = 'eyJ0eXAiOiJKV1QiLCJhbG ..'
    return theToken
#end function

#start function
def connect_to_api():
    # get access token
    theToken = get_token()
    
    #URL and identity data
    #url = "https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet('HT-1000')"
    url = "https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet"
    payload = {
        'format': 'json'
    }
    headers = {
        'Ocp-Apim-Trace': 'true',
        'Authorization': 'Bearer ' + theToken,
        'Cookie': 'sap-usercontext=sap-client=235'
    }
    # send the request to the api
    response = requests.request("GET", url, headers=headers, data=payload)
    return response
#end function

#start function
def clear_console():
    os.system('clear')
    print(' ... ut å se etter SAP data ... ')
    print(' ------------------------------\n')
#end function

#start function
def print_the_data(response):
    print(response.text)                # data received
    apiData = response.json()           # API returns json inside a python list
    #print out first data item received
    xDict = apiData[0]
    print('.. print the first row of data received fom the SAP ODATA service ..\n')
    for key, values in xDict.items():
        print(key, ': ', values) 
#end function

#the main module
def main_module():
    clear_console()
    response = connect_to_api()
    apiOK = check_if_error(response)
    if apiOK:
        print_the_data(response)   
#end main module

# -- start of programme ----
if __name__ == '__main__':
    main_module()
    print()
