# the API is published in the Equinor API hub. The API returns the information based on a given employee number. 

#the library in python 3.x best suited to read REST API
import requests
import config

#connect to the api
def connect_to_api(theToken):
    #URL and identity data
    url = config.ENDPOINTSCM + "?$format=json"
    payload = {}
    headers = {
        'Ocp-Apim-Trace': 'true',
        'Authorization': 'Bearer ' + theToken
    }
    # send the request to the api
    response = requests.request("GET", url, headers=headers, data=payload)
    return response
#end function


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
            print('for some reason we can not provide the data from SCM today - even if the response is: ', response.reason)
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
def scm_module(theToken):
    # get access token
    response = connect_to_api(theToken)
    apiOK = check_if_error(response)
    SCMData = ''
    sapSystem = ''
    # print feedback from API; data or error message
    if apiOK:
        SCMData, sapSystem = print_the_data(response.json())
    else:
        sapSystem = ' - we are not able to connect with the SAP ECC in Azure now. Bother me another time.'
    return SCMData, sapSystem 
#end main module

# -- start of programme ----
if __name__ == '__main__':
    #clear_console()
    productList = '<empty>'
    #productList, sapSystem = main_module()
    print(productList)