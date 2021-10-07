# the API is published in the Equinor API hub. The API returns the information based on a given employee number. 

#the library in python 3.x best suited to read REST API
import requests
import config

#connect to the api
def connect_to_api(theToken):
    # getting the input needed to authorize and fetch the wanted data
    #inKey = input('Oppgi subscription for geir owe (from api hub): ')
    inKey = 'dcc2d55f467b43699dfbe87f38b5319c'
    #theToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtpZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJjODgwYjY3MC00Y2NkLTQyOTAtYTYxMi0wY2ZhOWY3NzcxZmIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAvIiwiaWF0IjoxNjMzNTkyMTY0LCJuYmYiOjE2MzM1OTIxNjQsImV4cCI6MTYzMzU5NjA2NCwiYWlvIjoiRTJZQWd1VzZuN1k4RUpPWFRuK3UrWmJQL3dNQSIsImFwcGlkIjoiMTI1OWU3OGEtYWUwNy00MDM1LTgzOGMtMmQ1MTY4MjcxNDU2IiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvM2FhNGEyMzUtYjZlMi00OGQ1LTkxOTUtN2ZjZjA1YjQ1OWIwLyIsIm9pZCI6ImEyYjdkODFmLTFkN2EtNDllZi05YTJlLTUyYmUzNzlkNmMyMiIsInJoIjoiMC5BUUlBTmFLa091SzIxVWlSbFhfUEJiUlpzSXJuV1JJSHJqVkFnNHd0VVdnbkZGWUNBQUEuIiwicm9sZXMiOlsiRW1wSW50ZXJuYWwiXSwic3ViIjoiYTJiN2Q4MWYtMWQ3YS00OWVmLTlhMmUtNTJiZTM3OWQ2YzIyIiwidGlkIjoiM2FhNGEyMzUtYjZlMi00OGQ1LTkxOTUtN2ZjZjA1YjQ1OWIwIiwidXRpIjoiQUlXczdZVmx3VVNfdXNXa3NtODJBQSIsInZlciI6IjEuMCJ9.W1n1DQ636QDSqx1xHjESUI5gqAiNh9P3rfinigIcoX8ql9mXsNQg888EW4GEPD_h43tB8oF84GBekaVhc3a9tHl_CV9DzeVmw6gCiBD4hy3AugAr3GQWcpl-9tbnC15iXJ0VYOubAG7qhRvf4I76Er6rsZQejyiLp1YU-CTSPXeG2DxvE0zStfZY2mRyOsMR5pzO3QPcHBKOgD9wpH0kIto9QS-izkGPoGQZNZCCNiywqteJIsUUQS85eq2dXZpoBsRmC2i3-Qe7CFFTPo7RQviqmmQIZG7OFf7mYq_cdP0gYGv26s5zg4LT9NwMHKci02erGVqevwFdQsGtyFnZ7A'

    #the endpoint URL for api 
    #url = "https://api-dev.gateway.equinor.com/scm-api/v1/Ping"
    url = config.ENDPOINTSCM + "?$format=json"
    #API parameters, including the accessToken received earlier
    headers = {
        'Ocp-Apim-Subscription-Key': inKey,
        'Authorization': 'Bearer ' + theToken
    }
    params = {}
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