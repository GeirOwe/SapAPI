#automated test of main.py

from main import *

#the main module
def automated_test():
    print()
    response = connect_to_api()
    if response.status_code >= 200:
        print('connect api module ok')
    apiOK, err_msg = check_if_error(response)
    # print feedback from API; data or error message
    if apiOK:
        print('received data from api') 
    else:
        print('error message processed ok')
    print('automated test finalized ok')
    print()
    return True

# -- start of programme ----
if __name__ == '__main__':
    automated_test()
