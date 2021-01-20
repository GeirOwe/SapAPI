#access ODATA thru a SAP API
#API is exposed in api.equinor.com and OATA are fecthed from D05
#auth done thru azure AD

#the library in python 3.x best suited to read REST API
import requests

#inKey = input('Oppgi subscription for geir owe (from api hub): ')
#inKey = 'dcc2d55f467b43699dfbe87f38b5319c'

#URL and identity data
url = "https://api-dev.gateway.equinor.com/sap-api-basic/ProductSet('HT-1000')"
payload = {
        'format': 'json'
}
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiI0ODkyNmFiYi0yYzU4LTRkNmMtYWJmNy1kNjk1ZDAxYmM2YzUiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAvIiwiaWF0IjoxNjExMTM3Mzg3LCJuYmYiOjE2MTExMzczODcsImV4cCI6MTYxMTE0MTI4NywiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhTQUFBQTRRR1g2aTRNcmZwM2tQZVM5M2xXWXNLRUZqN2FHUFVob2ptaVZIeDNadUU9IiwiYW1yIjpbInB3ZCJdLCJhcHBpZCI6IjQ4OTI2YWJiLTJjNTgtNGQ2Yy1hYmY3LWQ2OTVkMDFiYzZjNSIsImFwcGlkYWNyIjoiMSIsImZhbWlseV9uYW1lIjoiV8OmcnNsYW5kIiwiZ2l2ZW5fbmFtZSI6IkdlaXIgT3dlIiwiaXBhZGRyIjoiOTIuMjIxLjc1Ljg5IiwibmFtZSI6IkdlaXIgT3dlIFfDpnJzbGFuZCIsIm9pZCI6IjJiYmM4MjljLTI2NTktNDg4YS1iZTkwLTJhZjg4MjI0NzQwYyIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0yMjA1MjMzODgtMTA4NTAzMTIxNC03MjUzNDU1NDMtMTM3ODUiLCJyaCI6IjAuQUFBQU5hS2tPdUsyMVVpUmxYX1BCYlJac0x0cWtraFlMR3hOcV9mV2xkQWJ4c1VDQVBZLiIsInNjcCI6IlVzZXIuUmVhZCIsInN1YiI6Inp2QnItN0ZUM1ZOdWh6aGIzVHpWM0R0QW5nX2lzRlV3dU9fZHBfTFBkam8iLCJ0aWQiOiIzYWE0YTIzNS1iNmUyLTQ4ZDUtOTE5NS03ZmNmMDViNDU5YjAiLCJ1bmlxdWVfbmFtZSI6IkdPV0BlcXVpbm9yLmNvbSIsInVwbiI6IkdPV0BlcXVpbm9yLmNvbSIsInV0aSI6ImwtWFFmYzl1QkVDbFFLd2REbVhBQUEiLCJ2ZXIiOiIxLjAifQ.DLhzinzg2vQlaGPbh0mQMM8QOtl8t68ysgarc0WfF6urluhQANlKoYRsgSu2i1HI46HW-ur66S6Sq59UV5cyW_lSRYJFSsx8suyb_QUm01vS3BgDcWM2r2uk6e5bkDmFHpsuu7Jw6fQkxvXM0vd3P_nJXgfUVV3AN_whvjMjyHDyVEbY2n-33C9k_61FkGYYAvU8UApqhpJ2TAcRzFJ6ghNZhVTxQUEpJkgBP2u0zGoa4JNBdsAgWvgxdESFY8uEgTT6LIPkKuE2xtVdfnQ_NbWNKy_pNIjiSqBdMHvYLeUhMnZbXC11Lnse2hqQzyPpWYs0QOAshRGHu7vxjpQnfg',
  'Cookie': 'sap-usercontext=sap-client=235'
}

# send the request to the api
response = requests.request("GET", url, headers=headers, data=payload)

#testing the response code from the api -> 200 success. 401 no authorization. 404 not found
if response.status_code > 299:
    print('error received from the API - error code: ', response.status_code, '-', response.reason)
else :
    print(response.text)   