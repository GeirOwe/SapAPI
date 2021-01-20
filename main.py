#access ODATA thru a SAP API. The API is exposed in api.equinor.com and the ODATA are fecthed from D05
#auth done thru azure AD 

import os
import requests                         #the library in python 3.x best suited to read REST API

#start function
def check_error_msg(response):
    #testing the response code -> 200 success. 401/403 no authorization. 404 not found
    if response.status_code < 299:      #ok  - but empty data set
        err_msg = 'for some reason we can not provide the data today - even if the response is: ' + response.reason
    #an error occurred
    elif response.status_code == 403:
        err_msg = 'The Auth token is ok. Most likely some roles are missing in SAP backend ERP. Error code ' + str(response.status_code) + ' - ' + response.reason
    elif response.status_code == 401:
        err_msg = 'Most likely the token has gotten a timeout, refresh the token. Error code ' + str(response.status_code) + ' - ' + response.reason
    else :
        err_msg = 'error received from the API. Error code ' + str(response.status_code) + ' - ' + response.reason
    return err_msg
#end function

#start function
def get_token():
    theToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiI0ODkyNmFiYi0yYzU4LTRkNmMtYWJmNy1kNjk1ZDAxYmM2YzUiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAvIiwiaWF0IjoxNjExMTQ5NzA2LCJuYmYiOjE2MTExNDk3MDYsImV4cCI6MTYxMTE1MzYwNiwiYWNyIjoiMSIsImFpbyI6IkUySmdZREJlTSt0b1FsQkZvdjNERzI5Y3psUXQrVjA5WDY4eVpJbm00amVPRnJvWFUyVUIiLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiNDg5MjZhYmItMmM1OC00ZDZjLWFiZjctZDY5NWQwMWJjNmM1IiwiYXBwaWRhY3IiOiIxIiwiZmFtaWx5X25hbWUiOiJXw6Zyc2xhbmQiLCJnaXZlbl9uYW1lIjoiR2VpciBPd2UiLCJpcGFkZHIiOiI5Mi4yMjEuNzUuODkiLCJuYW1lIjoiR2VpciBPd2UgV8OmcnNsYW5kIiwib2lkIjoiMmJiYzgyOWMtMjY1OS00ODhhLWJlOTAtMmFmODgyMjQ3NDBjIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTIyMDUyMzM4OC0xMDg1MDMxMjE0LTcyNTM0NTU0My0xMzc4NSIsInJoIjoiMC5BQUFBTmFLa091SzIxVWlSbFhfUEJiUlpzTHRxa2toWUxHeE5xX2ZXbGRBYnhzVUNBUFkuIiwic2NwIjoiVXNlci5SZWFkIiwic3ViIjoienZCci03RlQzVk51aHpoYjNUelYzRHRBbmdfaXNGVXd1T19kcF9MUGRqbyIsInRpZCI6IjNhYTRhMjM1LWI2ZTItNDhkNS05MTk1LTdmY2YwNWI0NTliMCIsInVuaXF1ZV9uYW1lIjoiR09XQGVxdWlub3IuY29tIiwidXBuIjoiR09XQGVxdWlub3IuY29tIiwidXRpIjoiVl9qZzB6ZHpza2VzOVd6OTF1VE9BQSIsInZlciI6IjEuMCJ9.iSE5iDreJSk2StTn4SA3K_FI8x_eu5ILXMga09u_jbCTqwVv_pTJZQXH_p7u5qvRbDJ96kAzK4I4htujZ_WM1JuJnnOrU2Ti7QbGcxTB4VcD45bzG3bT85YNJhEUNNUDBHInRsqx-8x-3xfsEpUTNf1TOh1MMt19FFcA0qTv9-_5v7GVa35KHs-msxw2lXULVH71OAkMZtn8ov446Gyn6iOL30QM-0A94mPjw7AyV7FBU7_rJC1Eg0bgWaJKF7KMLGnnbJkPg6KJtBa3Z9GuxH-DlXx-vpBd4WfOSmqX88KP-xcGJpyxZhMfBMbP9x15gNJmboaaZd43OQsOFW9ccQ'
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
def print_API_data(response):
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
    
    #call api
    response = connect_to_api()
    apiError = (response.status_code > 299)
    if apiError:
        err_msg = check_error_msg(response)
        print(err_msg)
    else:
        emptyDataset = (len(response.json()) == 0)
        if emptyDataset:
            err_msg = check_error_msg(response)
            print(err_msg)
        else :        
            print_API_data(response)   
#end main module

# -- start of programme ----
if __name__ == '__main__':
    main_module()
    print()