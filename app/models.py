#access ODATA thru a SAP API. The API is exposed in api.equinor.com and the ODATA are fecthed from D05
#auth done thru azure AD 

import pandas as pd
import os
import requests                         #the library in python 3.x best suited to read REST API
import json

#start function
def check_if_error(response):
    #testing the response code -> 200 success. 401/403 no authorization. 404 not found    
    apiOK = False
    err_msg = ''
    
    #ok? empty data set?
    if response.status_code < 299:      
        #emptyDataset = (len(response.json()) == 0)
        emptyDataset = False
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

    return apiOK, err_msg
#end function

#start function
def get_token():
    theToken = os.getenv("TOKEN")           # from the .env file
    #APIkey = os.getenv("API_KEY")           # from the .env file
    return theToken
#end function

#start function
def connect_to_api():
    # get access token
    theToken = str(get_token())
    
    #URL and identity data
    url = "https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet?$format=json"
    payload = {}
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
    print(' ... looking for data in the SAP API ... ')
    print(' ---------------------------------------\n')
#end function

#start function
def read_sap_system(systemURI):
    res = systemURI.split('https://SAP')
    sapSystem = res[1][0:3]
    return sapSystem
#end function

#start function
def translate_json(xDict):
    df = pd.json_normalize(xDict['results'])
    productList = []
    noOfRowsToShow = 15
    sapSystem = ''
    i = 0
    for idx, row in df.iterrows():
        if sapSystem == '':
            sapSystem = read_sap_system(row['__metadata.uri'])
        i += 1
        if i <= noOfRowsToShow:
            productList.append(
            {
                'ProductID': row['ProductID'],
                'Name': row['Name'],
                'WeightMeasure': row['WeightMeasure'],
                'WeightUnit': row['WeightUnit'],
                'CurrencyCode': row['CurrencyCode'],
                'Price': row['Price'],
                'Width': row['Width'],
                'Depth': row['Depth'],
                'Height': row['Height'],
                'DimUnit': row['DimUnit']
            }
            )
    return productList, sapSystem
#end function

#start function
def print_the_data(response):
    apiData = response.json()           # API returns json inside a python list
    #print out first data item received
    xDict = apiData.get('d')
    productList, sapSystem = translate_json(xDict)
    return productList, sapSystem
#end function

#the main module
def main_module():
    response = connect_to_api()
    apiOK, err_msg = check_if_error(response)
    productList = ''
    sapSystem = ''
    # print feedback from API; data or error message
    if apiOK:
        productList, sapSystem = print_the_data(response)
    return productList, sapSystem 
#end main module

# -- start of programme ----
if __name__ == '__main__':
    clear_console()
    productList, sapSystem = main_module()
    print(productList)

