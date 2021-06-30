# the API is published in the Equinor API hub. The API returns the information based on a given employee number. 
# more information is published here: https://api.equinor.com/docs/services/Basic-Pl-Employee-V1/operations/get-employee

#the library in python 3.x best suited to read REST API
import requests

#connect to the api
def connect_to_api(theToken):
    # getting the input needed to authorize and fetch the wanted data
    inPernr = '686603'
    #inKey = input('Oppgi subscription for geir owe (from api hub): ')
    inKey = 'dcc2d55f467b43699dfbe87f38b5319c'
    #theToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiJjODgwYjY3MC00Y2NkLTQyOTAtYTYxMi0wY2ZhOWY3NzcxZmIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAvIiwiaWF0IjoxNjE4Mzk2ODY3LCJuYmYiOjE2MTgzOTY4NjcsImV4cCI6MTYxODQwMDc2NywiYWlvIjoiRTJaZ1lIQ2M1MXJ4bnJ2ZmlMczZnYVByWGtBUEFBPT0iLCJhcHBpZCI6IjEyNTllNzhhLWFlMDctNDAzNS04MzhjLTJkNTE2ODI3MTQ1NiIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzNhYTRhMjM1LWI2ZTItNDhkNS05MTk1LTdmY2YwNWI0NTliMC8iLCJvaWQiOiJhMmI3ZDgxZi0xZDdhLTQ5ZWYtOWEyZS01MmJlMzc5ZDZjMjIiLCJyaCI6IjAuQVFJQU5hS2tPdUsyMVVpUmxYX1BCYlJac0lybldSSUhyalZBZzR3dFVXZ25GRllDQUFBLiIsInJvbGVzIjpbIkVtcEludGVybmFsIl0sInN1YiI6ImEyYjdkODFmLTFkN2EtNDllZi05YTJlLTUyYmUzNzlkNmMyMiIsInRpZCI6IjNhYTRhMjM1LWI2ZTItNDhkNS05MTk1LTdmY2YwNWI0NTliMCIsInV0aSI6IkVHR3RrS2p4MEVLU2Z6Q3YtZkF5QUEiLCJ2ZXIiOiIxLjAifQ.Vo5OOgpY4dpGCDRgknv3wu6bjGgV2feTlbX_l6-2PSa2cC9LQndnbKHwZx6_OkEO5BE5XTaeUBkZnfZw0Pyf8FMukmsm9aeMqpGZ7RFNzwuQt6gNj-EbUiu3TIyHQ13zo-DfsHzKfLLrnUikc0t5i51kGC1j0_2BpdVsBYGyHJwFxID6XEc4NhtPn3GUWcucjta0tovAkjC2RAw79uzax7bMVGDbXbFzRf48gpCh_OU-RBSzGQMzmd5Lr1IGLx6GJPbbyHLjW5PpnAUTiQ0isTMy34OFFJ93ROXfbJBDfMuO6wpoihW5i8raCpsYmP8Y3_wr_yOqNxEhVij0cyGe3g'

    #the endpoint URL for api 
    url = "https://api.gateway.equinor.com/basic-pl-api-employee-internal/v1/Employee"

    #API parameters, including the accessToken received earlier
    headers = {
        'Ocp-Apim-Subscription-Key': inKey,
        'Authorization': 'Bearer ' + theToken
    }
    params = {
        'PERNR': inPernr
    }
    #the request to get the API data
    response = requests.request("GET", url, headers=headers, params = params)
    return response 


def check_if_error(response):
    #testing the response code from the api -> 200 success. 401 no authorization. 404 not found
    if response.status_code > 299:
        print('error received from the API - error code: ', response.status_code, '-', response.reason)
        apiOK = False
    else :
        #reading the data  - it returns the json inside a python list
        apiData = response.json()
        #reading the list item to get the json dictionary
        if len(apiData) > 0:
            apiOK = True
            xDict = apiData[0]
            #print out the key and the value from the dictionary; i.e. the content received from the rest API
            for key, values in xDict.items():
                print(key, ': ', values) 
        else:
            print('for some reason we can not provide the data for this employee number today - even if the response is: ', response.reason)
            print('maybe the system has gotten the COVID-19 virus?')
            apiOK = False
    return apiOK

def print_the_data(apiData):
    xDict = apiData[0]
    sapSystem = 'SAP ECC in Azure'
    #print out the key and the value from the dictionary; i.e. the content received from the rest API
    for key, values in xDict.items():
        print(key, ': ', values) 
    return xDict, sapSystem

#the main module
def pl_module(theToken):
    # get access token
    response = connect_to_api(theToken)
    apiOK = check_if_error(response)
    employeeData = ''
    sapSystem = ''
    # print feedback from API; data or error message
    if apiOK:
        employeeData, sapSystem = print_the_data(response.json())
    else:
        sapSystem = ' - we are not able to connect with the SAP ECC in Azure now. Bother me another time.'
    return employeeData, sapSystem 
#end main module

# -- start of programme ----
if __name__ == '__main__':
    #clear_console()
    productList = '<empty>'
    #productList, sapSystem = main_module()
    print(productList)