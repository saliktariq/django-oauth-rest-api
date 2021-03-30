# -*- coding: utf-8 -*-

def registerNewUser(username, password, firstname, lastname):
    import requests, json
    url = "http://10.61.64.150:8000/authentication/register/"
    userObject = {
        'username': username,
        'password': password,
        'first_name': firstname,
        'last_name': lastname
        }
    userRegistrationResponse = requests.post(url, data= userObject)
    serverResponse = userRegistrationResponse.json()
   # newUserToken = serverResponse['access_token']
    if (serverResponse is not None):
        print(serverResponse)
        return serverResponse
    else:
        print("Error! Unable to register user")

def requestNewToken(username, password):
    import requests, json
    url = "http://10.61.64.150:8000/authentication/token/"
    requestObject = {
        'username': username,
        'password': password,
        }
    requestedToken = requests.post(url, data= requestObject)
    serverResponse = requestedToken.json()
    #serverResponse = serverResponse['access_token']
    if (serverResponse is not None):
        print(serverResponse)
        return serverResponse
    else:
        print("Error! Unable to authenticate user")
        
def refreshToken(rToken):
    import requests, json
    url = "http://10.61.64.150:8000/authentication/token/refresh/"
    requestObject = {
        'refresh_token': rToken
        }

    refreshTokenRequest = requests.post(url, data= requestObject)
    serverResponse = refreshTokenRequest.json()
    if (serverResponse is not None):
        print(serverResponse)
        return serverResponse
    else:
         print("Error! Unable to refresh user token")
         
def revokeToken(token):
    import requests, json
    url = "http://10.61.64.150:8000/authentication/token/revoke/"
    requestObject = {
        'token': token
        }

    revokeRequest = requests.post(url, data= requestObject)
    serverResponse = revokeRequest.json()
    if (serverResponse is not None):
        print(serverResponse)
        return serverResponse
    else:
         print("Error! Unable to revoke token")
        
# RegisteredObject = registerNewUser('saliktariq', 'salik123', 'Salik', 'Tariq')

# accessToken = requestNewToken('saliktariq', 'salik123')

# rToken = accessToken['refresh_token']

# refreshedToken = refreshToken(rToken)

# newAccessToken = refreshedToken['access_token']

# revoke = revokeToken(newAccessToken)


