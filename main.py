#access ODATA thru a SAP API. The API is exposed in api.equinor.com and the ODATA are fecthed from D05
#auth done thru azure AD 

import os
#the library in python 3.x best suited to read REST API
import requests

#start function
def check_error_msg(response):
    #testing the response code -> 200 success. 401/403 no authorization. 404 not found
    if response.status_code < 299:      #ok  - but empty data set
        err_msg = 'for some reason we can not provide the data today - even if the response is: ' + response.reason
    #an error occurred
    elif response.status_code == 403:
        err_msg = 'Most likely some roles are missing in SAP backend ERP. Error code ' + str(response.status_code) + ' - ' + response.reason
    elif response.status_code == 401:
        err_msg = 'Most likely the token has gotten a timeout, refresh the token. Error code ' + str(response.status_code) + ' - ' + response.reason
    else :
        err_msg = 'error received from the API. Error code ' + str(response.status_code) + ' - ' + response.reason
    return err_msg
#end function

#start function
def connect_to_api():
    #URL and identity data
    #url = "https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet('HT-1000')"
    url = "https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet"
    payload = {
        'format': 'json'
    }
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiI0ODkyNmFiYi0yYzU4LTRkNmMtYWJmNy1kNjk1ZDAxYmM2YzUiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAvIiwiaWF0IjoxNjExMTQzOTQ1LCJuYmYiOjE2MTExNDM5NDUsImV4cCI6MTYxMTE0Nzg0NSwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhTQUFBQWFDUUY5cGYyQk1wUXlGR0RNV2ZSdzFaY1FBazRvOWdRcHZ3RjR2a3YvTzQ9IiwiYW1yIjpbInB3ZCJdLCJhcHBpZCI6IjQ4OTI2YWJiLTJjNTgtNGQ2Yy1hYmY3LWQ2OTVkMDFiYzZjNSIsImFwcGlkYWNyIjoiMSIsImZhbWlseV9uYW1lIjoiV8OmcnNsYW5kIiwiZ2l2ZW5fbmFtZSI6IkdlaXIgT3dlIiwiaXBhZGRyIjoiOTIuMjIxLjc1Ljg5IiwibmFtZSI6IkdlaXIgT3dlIFfDpnJzbGFuZCIsIm9pZCI6IjJiYmM4MjljLTI2NTktNDg4YS1iZTkwLTJhZjg4MjI0NzQwYyIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0yMjA1MjMzODgtMTA4NTAzMTIxNC03MjUzNDU1NDMtMTM3ODUiLCJyaCI6IjAuQUFBQU5hS2tPdUsyMVVpUmxYX1BCYlJac0x0cWtraFlMR3hOcV9mV2xkQWJ4c1VDQVBZLiIsInNjcCI6IlVzZXIuUmVhZCIsInN1YiI6Inp2QnItN0ZUM1ZOdWh6aGIzVHpWM0R0QW5nX2lzRlV3dU9fZHBfTFBkam8iLCJ0aWQiOiIzYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAiLCJ1bmlxdWVfbmFtZSI6IkdPV0BlcXVpbm9yLmNvbSIsInVwbiI6IkdPV0BlcXVpbm9yLmNvbSIsInV0aSI6IlZLSXFSTnZxRlVpYXpZNmNfU214QUEiLCJ2ZXIiOiIxLjAifQ.kUcn7XmmrgqQ251LkZBL8Vk_QFqIgS0P2vp80CcvdEdNs3HRTSU-o2N1pI3EXBzluT_ioPJ-7cdGb4nA1Fndh7G2Rgfwjj_-LE1sYcumoicJQTdXNjdt6iWihxHg1z641NKPKd6W4xVYN9_-5EpAWcFXD0zNPew4dtrtP-TWDRf0207DqQ6uwJUcEH5pfV9jtaV3ufKUXr0q4vbtHSyeKB4HL8Wq60rJDmPq1u58uVAInZV6GoCPEU4KgCCEDE1VD4DKkXXvjW5uvnl8S7k3_4pmrjK6yOHaGm9K9_Q1ct98YqssfUf6wmXR69MaEn4dJ3Qt6aOjHfxz_XsewqzOIQ',
        'Cookie': 'sap-usercontext=sap-client=235'
    }
    # send the request to the api
    response = requests.request("GET", url, headers=headers, data=payload)
    return response
#end function

#the main programe
def main_program():
    #call api
    response = connect_to_api()
    #check response
    if (response.status_code > 299) or (len(response.json()) == 0):
        err_msg = check_error_msg(response)
        print(err_msg)
    else :
        print(response.text)                # data received
        apiData = response.json()           # API returns json inside a python list
        #print out first data item received
        xDict = apiData[0]
        print('.. print the first row of data received fom the SAP ODATA service ..\n')
        for key, values in xDict.items():
            print(key, ': ', values) 
#end main programe

# -- start of programme ----
if __name__ == '__main__':
    os.system('clear')
    print(' ... ut å se etter SAP data ... ')
    print(' ------------------------------\n')
    main_program()
    print()
