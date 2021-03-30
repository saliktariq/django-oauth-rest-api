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
        

import requests, json
newUserToken = registerNewUser('saliktariq4','salik1','Salik','Tariq')
access_token = newUserToken['access_token']
messageURL = 'http://10.61.64.150:8000/v1/messages/'
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {
            "postIdentifier": 2,
            "topicName": [
                {
                    "topicName": "P"
                }
            ],
            "title": "Message One",
            "message": "This is Message One",
            "creationTimestamp": "2021-03-27T21:15:32Z",
            "expirationTimestamp": "2021-03-28T18:00:00Z",
            "isLive": True,
            "username": "admin",
            "user_id": 1,
            "feedbacks": [
                {
                    "isLiked": True,
                    "isDisliked": True,
                    "comment": "this is feedback one",
                    "username": "admin",
                    "user_id": 1
                }
            ]
        }


submitResponse = requests.post(messageURL, headers = headers, data= dataset)
print(submitResponse.json())

