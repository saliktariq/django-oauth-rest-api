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
#                     "topic_name": "T"
#             }


# submitResponse = requests.post(messageURL, headers = headers, data= dataset)
# print(submitResponse.json())



############################################################

# import requests, json
# newUserToken = registerNewUser('saliktariq','salik1','Salik','Tariq')
# access_token = newUserToken['access_token']
# messageURL = 'http://127.0.0.1:8000/v1/message/'
# headers = {'Authorization': 'Bearer '+str(access_token)}
# dataset = {

#         "topic": [
#             {

#                 "topic_name": "H"
#             },
#             {

#                 "topic_name": "F"
#             }
#         ],
#         "title": "Title THREE",
#         "message": "This is third message"
       
#     }

# submitResponse = requests.post(messageURL, headers = headers, json= dataset)
# print(submitResponse.json())

####################################################################

import requests, json
newUserToken = registerNewUser('saliktariq2','salik1','Salik','Tariq')
access_token = newUserToken['access_token']
messageURL = 'http://127.0.0.1:8000/v1/feedback/'
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {
        "post_identifier": 6,
        "is_liked": False,
        "is_disliked": True,
        "comment": "third time a charm feedback"
       
    }

submitResponse = requests.post(messageURL, headers = headers, json= dataset)
print(submitResponse.json())

