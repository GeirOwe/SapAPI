# the API is published in the Equinor API hub. The API returns the information based on a given employee number. 
# more information is published here: https://api.equinor.com/docs/services/Basic-Pl-Employee-V1/operations/get-employee

#the library in python 3.x best suited to read REST API
import requests
import config

#connect to the api
def connect_to_api(theToken, emplNo):
    #inKey = input('Oppgi subscription for geir owe (from api hub): ')
    inKey = 'dcc2d55f467b43699dfbe87f38b5319c'

    #the endpoint URL for api 
    #url = "https://api.gateway.equinor.com/basic-pl-api-employee-internal/v1/Employee"
    url = config.ENDPOINTPL + "?$format=json"
    #API parameters, including the accessToken received earlier
    headers = {
        'Ocp-Apim-Subscription-Key': inKey,
        'Authorization': 'Bearer ' + theToken
    }
    params = {
        'PERNR': emplNo
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
        else:
            print('for some reason we can not provide the data for this employee number today - even if the response is: ', response.reason)
            print('maybe the system has gotten the COVID-19 virus?')
            apiOK = False
    return apiOK

def print_the_data(apiData):
    xDict = apiData[0]
    sapSystem = ''
    return xDict, sapSystem

#the main module
def pl_module(theToken, emplNo):
    # get access token
    response = connect_to_api(theToken, emplNo)
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