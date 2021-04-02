# -*- coding: utf-8 -*-

def registerNewUser(username, password, firstname, lastname):
    import requests, json
    url = "http://127.0.0.1:8000/authentication/register/"
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
        
######################################################

# import requests, json
# newUserToken = registerNewUser('saliktariq4','salik1','Salik','Tariq')
# access_token = newUserToken['access_token']
# messageURL = 'http://127.0.0.1:8000/v1/topic/'
# headers = {'Authorization': 'Bearer '+str(access_token)}
# dataset = {
#                     "topic_name": "S"
#             }


# submitResponse = requests.post(messageURL, headers = headers, data= dataset)
# print(submitResponse.json())



############################################################

import requests, json
newUserToken = registerNewUser('saliktariq189','salik1','Salik','Tariq')
access_token = newUserToken['access_token']
messageURL = 'http://127.0.0.1:8000/v1/message/'
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {

        "topic": [
            {

                "topic_name": "P"
            },
            {

                "topic_name": "H"
            }
        ],
        "title": "Second Message",
        "message": "This is second message",
        'expiry_in_seconds': 10
       
    }

submitResponse = requests.post(messageURL, headers = headers, json= dataset)
print(submitResponse.json())

####################################################################

# import requests, json
# newUserToken = registerNewUser('saliktariq','salik1','Salik','Tariq')
# access_token = newUserToken['access_token']
# messageURL = 'http://127.0.0.1:8000/v1/feedback/'
# headers = {'Authorization': 'Bearer '+str(access_token)}
# dataset = {
#         "post_identifier": 9,
#         "is_liked": False,
#         "is_disliked": True,
#         "comment": "first feedback"
       
#     }

# submitResponse = requests.post(messageURL, headers = headers, json= dataset)
# print(submitResponse.json())

