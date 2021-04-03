# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 18:57:31 2021

@author: Salik
"""

###################Helper Funcitons###########################################


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
    if (serverResponse is not None):
        print(serverResponse)
        return serverResponse
    else:
        print("Error! Unable to register user")

def requestNewToken(username, password):
    import requests, json
    url = "http://127.0.0.1:8000/authentication/token/"
    requestObject = {
        'username': username,
        'password': password,
        }
    requestedToken = requests.post(url, data= requestObject)
    serverResponse = requestedToken.json()
    if (serverResponse is not None):
        print(serverResponse)
        return serverResponse
    else:
        print("Error! Unable to authenticate user")
        
def refreshToken(rToken):
    import requests, json
    url = "http://127.0.0.1:8000/authentication/token/refresh/"
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
    url = "http://127.0.0.1:8000/authentication/token/revoke/"
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
        
##############################################################################


"""
TC 1. Olga, Nick, Mary and Nestor register and are ready to access the Piazza API.

------------------------------------------------
COMMENT OUT THE FOLLOWING CODE FIRST FIRST EXECUTION
------------------------------------------------

"""

# olga = registerNewUser("olga", "olga123", "Olga", "Kiev")
# nick = registerNewUser("nick", "nick123", "Nick", "English")
# mary = registerNewUser("mary", "mary123", "Mary", "Johns")
# nester = registerNewUser("nester", "nester123", "Nester", "Smith")

# print('--------------------------------------------')
# print("This Olga's registered credentials response")
# print(olga)
# print('--------------------------------------------')


# print('--------------------------------------------')
# print("This Nick's registered credentials response")
# print(nick)
# print('--------------------------------------------')


# print('--------------------------------------------')
# print("This Mary's registered credentials response")
# print(mary)
# print('--------------------------------------------')

# print('--------------------------------------------')
# print("This Nester's registered credentials response")
# print(nester)
# print('--------------------------------------------')


"""
TC 2. Olga, Nick, Mary and Nestor use the oAuth v2 authorisation service to register and get their tokens.

"""

# print('Note: Olga, Nick, Mary and Nestor are already registered using oAuth v2 authorisation service in TC1')
# print('In this test, I will demonstrate, how the above registered users request Tokens using oAuth v2 service')


olga = requestNewToken("olga", "olga123")
nick = requestNewToken("nick", "nick123")
mary = requestNewToken("mary", "mary123")
nester = requestNewToken("nester", "nester123")


# print('--------------------------------------------')
# print("This Olga's new Token response")
# print(olga)
# print('--------------------------------------------')


# print('--------------------------------------------')
# print("This Nick's new Token response")
# print(nick)
# print('--------------------------------------------')


# print('--------------------------------------------')
# print("This Mary's new Token response")
# print(mary)
# print('--------------------------------------------')

# print('--------------------------------------------')
# print("This Nester's new Token response")
# print(nester)
# print('--------------------------------------------')


"""
TC 3. Olga makes a call to the API without using her token. This call should be
unsuccessful as the user is unauthorised
"""

# import requests, json
# message_URL = 'http://127.0.0.1:8000/v1/message/'

# olga_request = requests.get(message_URL)
# print(olga_request.json())

"""
IMPORTANT: In order to satisfy referential integrity constraints, Many-to-Many
relationship table TOPICS must be pre-populated before any POST requestes to
the message table or feedback table. This only needs to be done once, and the
'unique' constraint in the TOPICS table will not allow duplicate entries.
------------------------------------------------
COMMENT OUT THE FOLLOWING CODE FIRST FIRST EXECUTION
------------------------------------------------
"""


# access_token = olga['access_token']
# message_URL = 'http://127.0.0.1:8000/v1/topic/'
# headers = {'Authorization': 'Bearer '+str(access_token)}
# dataset = {
#                     "topic_name": "P"
#             }
# print("Making call to post topic Politics denoted by P")
# submit_topic = requests.post(message_URL, headers = headers, data= dataset)
# print(submit_topic.json())

# dataset = {
#                     "topic_name": "H"
#             }
# print("Making call to post topic Health denoted by H")
# submit_topic = requests.post(message_URL, headers = headers, data= dataset)
# print(submit_topic.json())

# dataset = {
#                     "topic_name": "S"
#             }
# print("Making call to post topic Sports denoted by S")
# submit_topic = requests.post(message_URL, headers = headers, data= dataset)
# print(submit_topic.json())

# dataset = {
#                     "topic_name": "T"
#             }
# print("Making call to post topic Technology denoted by T")
# submit_topic = requests.post(message_URL, headers = headers, data= dataset)
# print(submit_topic.json())

"""
TC 4. Olga posts a message in the Tech topic with an expiration time(eg. 5 minutes)
using her token. After the end of the expiration time, the message will not
accept any further user interactions (likes, dislikes or comments)
"""

import requests, json
message_URL = 'http://127.0.0.1:8000/v1/message/'
access_token = olga['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {

        "topic": [
            {

                "topic_name": "T"
            }
        ],
        "title": "Olga's first message in Technology",
        "message": "This is Olga's first message in the Tech topic.",
        'expiry_in_seconds': 300
       
    }

olga_request_to_post = requests.post(message_URL, headers = headers, json= dataset)
print(olga_request_to_post.json())

"""
TC 5. Nick posts a message in the Tech topic with an expiration time using his token
"""

import requests, json
message_URL = 'http://127.0.0.1:8000/v1/message/'
access_token = nick['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {

        "topic": [
            {

                "topic_name": "T"
            }
        ],
        "title": "Nick's first message in Technology",
        "message": "This is Nick's first message in the Tech topic.",
        'expiry_in_seconds': 300
       
    }

nick_request_to_post = requests.post(message_URL, headers = headers, json= dataset)
print(nick_request_to_post.json())

"""
TC 6. Mary posts a message in the Tech topic with an expiration time using his token
"""

import requests, json
message_URL = 'http://127.0.0.1:8000/v1/message/'
access_token = mary['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {

        "topic": [
            {

                "topic_name": "T"
            }
        ],
        "title": "Mary's first message in Technology",
        "message": "This is Mary's first message in the Tech topic.",
        'expiry_in_seconds': 300
       
    }

mary_request_to_post = requests.post(message_URL, headers = headers, json= dataset)
print(mary_request_to_post.json())


"""
TC. 7 Nick and Olga browse all the available posts in the Tech topic, there should
be three posts available with zero likes and without any comments
"""

import requests, json
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
access_token = nick['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}

nick_request = requests.get(tech_posts_URL, headers = headers)

print('----------NICKs REQUEST: FULL DATASET RECEIVED--------------------')
print(nick_request.json())
print('---------------------------------------------------')
post_number = 0
for request in nick_request.json():
    post_number = post_number + 1
    print('Post number : ' + str(post_number))
    print('Post by : ' + str(request['username']))
    print('Topic : ' + str(request['topic'][0]['topic_name']))
    print('Likes : ' + str(request['likes']))
    print('Dislikes : ' + str(request['dislikes']))
    print('Comments : ' + str(request['feedbacks']))
    
    
access_token = olga['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}
olga_request = requests.get(tech_posts_URL, headers = headers)

print('----------OLGAs REQUEST FULL DATASET RECEIVED--------------------')
print(olga_request.json())
print('---------------------------------------------------')
post_number = 0
for request in olga_request.json():
    post_number = post_number + 1
    print('Post number : ' + str(post_number))
    print('Post by : ' + str(request['username']))
    print('Topic : ' + str(request['topic'][0]['topic_name']))
    print('Likes : ' + str(request['likes']))
    print('Dislikes : ' + str(request['dislikes']))
    print('Comments : ' + str(request['feedbacks']))


"""
TC 8. Nick and Olga "likes" Mary's post in the Tech topic
"""

import requests, json
access_token = nick['access_token']
feedback_URL = 'http://127.0.0.1:8000/v1/feedback/'
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
headers = {'Authorization': 'Bearer '+str(access_token)}

marys_post_identifier = 0
post_count = 0
posts_in_tech = requests.get(tech_posts_URL, headers = headers)
for request in posts_in_tech.json():
    if request['username'] == 'mary':
        marys_post_identifier = request['post_identifier']
        post_count = post_count + 1
if post_count != 1:
    print('There are more than 1 posts by Mary or none at all. Test failed. Re-check previous tests')
else:
    
    dataset = {
            "post_identifier": marys_post_identifier,
            "is_liked": True,
            "is_disliked": False,
            "comment": ""
        }

    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    

access_token = olga['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}


dataset = {
        "post_identifier": marys_post_identifier,
        "is_liked": True,
        "is_disliked": False,
        "comment": ""

    }

submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
print(submit_request.json())


"""
TC 9. Nestor "likes" Nick's post and "dislikes" Mary's post in Tech topic.
"""

import requests, json
access_token = nester['access_token']
feedback_URL = 'http://127.0.0.1:8000/v1/feedback/'
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
headers = {'Authorization': 'Bearer '+str(access_token)}

nicks_post_identifier = 0
post_count = 0
posts_in_tech = requests.get(tech_posts_URL, headers = headers)
for request in posts_in_tech.json():
    if request['username'] == 'nick':
        nicks_post_identifier = request['post_identifier']
        post_count = post_count + 1
if post_count != 1:
    print('There are more than 1 posts by Nick or none at all. Test failed. Re-check previous tests')
else:
    
    dataset = {
            "post_identifier": nicks_post_identifier,
            "is_liked": True,
            "is_disliked": False,
            "comment": ""
        }

    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    



marys_post_identifier = 0
post_count = 0
posts_in_tech = requests.get(tech_posts_URL, headers = headers)
for request in posts_in_tech.json():
    if request['username'] == 'mary':
        marys_post_identifier = request['post_identifier']
        post_count = post_count + 1
if post_count != 1:
    print('There are more than 1 posts by Mary or none at all. Test failed. Re-check previous tests')
else:
    
    dataset = {
            "post_identifier": marys_post_identifier,
            "is_liked": False,
            "is_disliked": True,
            "comment": ""
        }

    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())



"""
TC 10. Nick browse all the available posts in the Tech topic at this stage,
he can see the number of likes and dislikes for each post. Mary has 2 likes and
1 dislike and Nick has 1 like. There are no comments made yet.
"""

import requests, json
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
access_token = nick['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}

nick_request = requests.get(tech_posts_URL, headers = headers)

print('----------FULL DATASET RECEIVED--------------------')
print(nick_request.json())
print('---------------------------------------------------')
post_number = 0
for request in nick_request.json():
    post_number = post_number + 1
    print('Post number : ' + str(post_number))
    print('Post by : ' + str(request['username']))
    print('Topic : ' + str(request['topic'][0]['topic_name']))
    print('Title : ' + str(request['title']))
    print('Message : ' + str(request['message']))
    print('Likes : ' + str(request['likes']))
    print('Dislikes : ' + str(request['dislikes']))
    print('Comments : ' + str(request['feedbacks']))







