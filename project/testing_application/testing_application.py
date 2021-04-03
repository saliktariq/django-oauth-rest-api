# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 18:57:31 2021

@author: Salik
"""

###################Helper Funcitons###########################################


def registerNewUser(username, password, firstname, lastname):
    import requests
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
    import requests
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
    import requests
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
    import requests
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

print('\n\n\nTC 1. Olga, Nick, Mary and Nestor register and are ready to access the Piazza API.\n\n\n')

olga = registerNewUser("olga", "olga123", "Olga", "Kiev")
nick = registerNewUser("nick", "nick123", "Nick", "English")
mary = registerNewUser("mary", "mary123", "Mary", "Johns")
nester = registerNewUser("nester", "nester123", "Nester", "Smith")

print('--------------------------------------------')
print("This Olga's registered credentials response")
print(olga)
print('--------------------------------------------')


print('--------------------------------------------')
print("This Nick's registered credentials response")
print(nick)
print('--------------------------------------------')


print('--------------------------------------------')
print("This Mary's registered credentials response")
print(mary)
print('--------------------------------------------')

print('--------------------------------------------')
print("This Nester's registered credentials response")
print(nester)
print('--------------------------------------------')


"""
TC 2. Olga, Nick, Mary and Nestor use the oAuth v2 authorisation service to register and get their tokens.

"""
print('\n\n\nTC 2. Olga, Nick, Mary and Nestor use the oAuth v2 authorisation service to register and get their tokens.\n\n\n')
print('Note: Olga, Nick, Mary and Nestor are already registered using oAuth v2 authorisation service in TC1')
print('In this test, I will demonstrate, how the above registered users request Tokens using oAuth v2 service')


olga = requestNewToken("olga", "olga123")
nick = requestNewToken("nick", "nick123")
mary = requestNewToken("mary", "mary123")
nester = requestNewToken("nester", "nester123")


print('--------------------------------------------')
print("This Olga's new Token response")
print(olga)
print('--------------------------------------------')


print('--------------------------------------------')
print("This Nick's new Token response")
print(nick)
print('--------------------------------------------')


print('--------------------------------------------')
print("This Mary's new Token response")
print(mary)
print('--------------------------------------------')

print('--------------------------------------------')
print("This Nester's new Token response")
print(nester)
print('--------------------------------------------')


"""
TC 3. Olga makes a call to the API without using her token. This call should be
unsuccessful as the user is unauthorised
"""
print('\n\n\nTC 3. Olga makes a call to the API without using her token. This call should be unsuccessful as the user is unauthorised\n\n\n')

import requests, json
message_URL = 'http://127.0.0.1:8000/v1/message/'

olga_request = requests.get(message_URL)
print(olga_request.json())

"""
IMPORTANT: In order to satisfy referential integrity constraints, Many-to-Many
relationship table TOPICS must be pre-populated before any POST requestes to
the message table or feedback table. This only needs to be done once, and the
'unique' constraint in the TOPICS table will not allow duplicate entries.
------------------------------------------------
COMMENT OUT THE FOLLOWING CODE FIRST FIRST EXECUTION
------------------------------------------------
"""


access_token = olga['access_token']
message_URL = 'http://127.0.0.1:8000/v1/topic/'
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {
                    "topic_name": "P"
            }
print("Making call to post topic Politics denoted by P")
submit_topic = requests.post(message_URL, headers = headers, data= dataset)
print(submit_topic.json())

dataset = {
                    "topic_name": "H"
            }
print("Making call to post topic Health denoted by H")
submit_topic = requests.post(message_URL, headers = headers, data= dataset)
print(submit_topic.json())

dataset = {
                    "topic_name": "S"
            }
print("Making call to post topic Sports denoted by S")
submit_topic = requests.post(message_URL, headers = headers, data= dataset)
print(submit_topic.json())

dataset = {
                    "topic_name": "T"
            }
print("Making call to post topic Technology denoted by T")
submit_topic = requests.post(message_URL, headers = headers, data= dataset)
print(submit_topic.json())

"""
TC 4. Olga posts a message in the Tech topic with an expiration time(eg. 5 minutes)
using her token. After the end of the expiration time, the message will not
accept any further user interactions (likes, dislikes or comments)
"""

print('\n\n\nTC 4. Olga posts a message in the Tech topic with an expiration time(eg. 5 minutes) using her token. After the end of the expiration time, the message will not accept any further user interactions (likes, dislikes or comments)\n\n\n')

import requests
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
print('\n\n\nTC 5. Nick posts a message in the Tech topic with an expiration time using his token\n\n\n')

import requests
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
print('\n\n\nTC 6. Mary posts a message in the Tech topic with an expiration time using his token\n\n\n')

import requests
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
print('\n\n\nTC. 7 Nick and Olga browse all the available posts in the Tech topic, there should be three posts available with zero likes and without any comments\n\n\n')

import requests
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
    print('Title : ' + str(request['title']))
    print('Message : ' + str(request['message']))
    print('Likes : ' + str(request['likes']))
    print('Dislikes : ' + str(request['dislikes']))
    print('Comments : ' + str(request['feedbacks']))


"""
TC 8. Nick and Olga "likes" Mary's post in the Tech topic
"""
print('\n\n\nTC 8. Nick and Olga "likes" Mary\'s post in the Tech topic\n\n\n')

import requests
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
print('\n\n\nTC 9. Nestor "likes" Nick\'s post and "dislikes" Mary\'s post in Tech topic.\n\n\n')

import requests
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
print('\n\n\nTC 10. Nick browse all the available posts in the Tech topic at this stage, he can see the number of likes and dislikes for each post. Mary has 2 likes and 1 dislike and Nick has 1 like. There are no comments made yet.\n\n\n')

import requests
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


"""
TC 11. Mary likes her post in the Tech topic. This call should be unsuccessful,
as in Piazza a post owner cannot like their own message.
"""
print('\n\n\nTC 11. Mary likes her post in the Tech topic. This call should be unsuccessful, as in Piazza a post owner cannot like their own message.\n\n\n')

import requests
access_token = mary['access_token']
feedback_URL = 'http://127.0.0.1:8000/v1/feedback/'
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
headers = {'Authorization': 'Bearer '+str(access_token)}

mary_post_identifier = 0
post_count = 0
posts_in_tech = requests.get(tech_posts_URL, headers = headers)
for request in posts_in_tech.json():
    if request['username'] == 'mary':
        mary_post_identifier = request['post_identifier']
        post_count = post_count + 1
if post_count != 1:
    print('There are more than 1 posts by Mary or none at all. Test failed. Re-check previous tests')
else:
    
    dataset = {
            "post_identifier": mary_post_identifier,
            "is_liked": True,
            "is_disliked": False,
            "comment": ""
        }

    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    

"""
TC 12. Nick and Olga comment for Mary's post in the Tech topic in a round-robin
fashion(one after another adding atleast 2 comments each)
"""
print('\n\n\nTC 12. Nick and Olga comment for Mary\'s post in the Tech topic in a round-robin fashion(one after another adding atleast 2 comments each)\n\n\n')

print('TC 12. Nick and Olga comment for Mary\'s post in the Tech topic in a round-robin fashion(one after another adding atleast 2 comments each)\n\n\n')
import requests
nick_access_token = nick['access_token']
feedback_URL = 'http://127.0.0.1:8000/v1/feedback/'
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
headers = {'Authorization': 'Bearer '+str(nick_access_token)}

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
            "is_disliked": False,
            "comment": "Nick's first comment on Mary's post"
        }

    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    

    olga_access_token = olga['access_token']
    headers = {'Authorization': 'Bearer '+str(olga_access_token)}
    
    
    dataset = {
            "post_identifier": marys_post_identifier,
            "is_liked": False,
            "is_disliked": False,
            "comment": "Olga's first comment on Mary's post"
    
        }
    
    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    
    headers = {'Authorization': 'Bearer '+str(nick_access_token)}
    dataset = {
            "post_identifier": marys_post_identifier,
            "is_liked": False,
            "is_disliked": False,
            "comment": "Nick's second comment on Mary's post"
    
        }
    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    
    headers = {'Authorization': 'Bearer '+str(olga_access_token)}
    
    
    dataset = {
            "post_identifier": marys_post_identifier,
            "is_liked": False,
            "is_disliked": False,
            "comment": "Olga's second comment on Mary's post"
    
        }
    
    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    
"""
TC 13. Nick browse all the available posts in the Tech topic, at this stage he
can see the number of likes and dislikes of each post and the comments made
"""

print('\n\n\nTC 13. Nick browse all the available posts in the Tech topic, at this stage he can see the number of likes and dislikes of each post and the comments made\n\n\n')

import requests
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
    for comment in request['feedbacks']:
        print('Comment: ' + str(comment['comment']))
        print('Commented by: '+ str(comment['username']))
    
"""
TC 14. Nester posts a message in the Health topic with an expiration time using her token
"""

print('\n\n\nTC 14. Nester posts a message in the Health topic with an expiration time using her token\n\n\n')

import requests
message_URL = 'http://127.0.0.1:8000/v1/message/'
access_token = nester['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}
dataset = {

        "topic": [
            {

                "topic_name": "H"
            }
        ],
        "title": "Nester's first message in Health",
        "message": "This is Nester's first message in the Health topic.",
        'expiry_in_seconds': 1
       
    }

nester_request_to_post = requests.post(message_URL, headers = headers, json= dataset)
print(nester_request_to_post.json())


"""
TC. 15 Mary browse all the available posts in the Health topic, at this stage
she can see only Nestor's post'
"""

print('\n\n\nTC. 15 Mary browse all the available posts in the Health topic, at this stage she can see only Nestor\'s post\n\n\n')

import requests
health_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/H/'
access_token = mary['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}

marys_request = requests.get(health_posts_URL, headers = headers)

print('----------MARYs REQUEST: FULL DATASET RECEIVED--------------------')
print(marys_request.json())
print('---------------------------------------------------')
post_number = 0
for request in marys_request.json():
    post_number = post_number + 1
    print('Post number : ' + str(post_number))
    print('Post by : ' + str(request['username']))
    print('Topic : ' + str(request['topic'][0]['topic_name']))
    print('Title : ' + str(request['title']))
    print('Message : ' + str(request['message']))
    print('Likes : ' + str(request['likes']))
    print('Dislikes : ' + str(request['dislikes']))
    print('Comments : ' + str(request['feedbacks']))
    

"""
TC. 16 Many posts a comment in the Nestor's message in the Health topic
"""

print('\n\n\nTC. 16 Many posts a comment in the Nestor\'s message in the Health topic\n\n\n')

import requests
mary_access_token = mary['access_token']
feedback_URL = 'http://127.0.0.1:8000/v1/feedback/'
health_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/H/'
headers = {'Authorization': 'Bearer '+str(mary_access_token)}

nestor_post_identifier = 0
post_count = 0
posts_in_health = requests.get(health_posts_URL, headers = headers)
for request in posts_in_health.json():
    if request['username'] == 'nester':
        nestor_post_identifier = request['post_identifier']
        post_count = post_count + 1
if post_count != 1:
    print('There are more than 1 posts by Nestor or none at all. Test failed. Re-check previous tests')
else:
    
    dataset = {
            "post_identifier": nestor_post_identifier,
            "is_liked": False,
            "is_disliked": False,
            "comment": "Mary's comment on Nestor's message in Health topic"
        }

    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())


"""
TC 17. Mary dislikes Nester's message in the Health topic after the end of post
expiration time. This should fail.
"""

print('\n\n\nTC 17. Mary dislikes Nester\'s message in the Health topic after the end of post expiration time. This should fail.\n\n\n')

import requests, time
mary_access_token = mary['access_token']
feedback_URL = 'http://127.0.0.1:8000/v1/feedback/'
health_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/H/'
headers = {'Authorization': 'Bearer '+str(mary_access_token)}

nester_post_identifier = 0
post_count = 0
posts_in_health = requests.get(health_posts_URL, headers = headers)
for request in posts_in_health.json():
    if request['username'] == 'nester':
        nester_post_identifier = request['post_identifier']
        post_count = post_count + 1
if post_count != 1:
    print('There are more than 1 posts by Nester or none at all. Test failed. Re-check previous tests')
else:
    
    dataset = {
            "post_identifier": nester_post_identifier,
            "is_liked": False,
            "is_disliked": True,
            "comment": ""
        }
    time.sleep(3) #Adding 3 seconds delay. Nester's post expiry was set to 1 second in last test
    submit_request = requests.post(feedback_URL, headers = headers, json= dataset)
    print(submit_request.json())
    
"""
TC 18. Nestor browses all the messages in the Health topic. There should be only post(his own)
with one comment (Mary's)
"""

print("\n\n\nTC 18. Nestor browses all the messages in the Health topic. There should be only post(his own) with one comment (Mary's)\n\n\n")

    
import requests
health_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/H/'
access_token = nester['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}
nester_request = requests.get(health_posts_URL, headers = headers)

print('----------FULL DATASET RECEIVED--------------------')
print(nester_request.json())
print('---------------------------------------------------')
post_number = 0
for request in nester_request.json():
    post_number = post_number + 1
    print('Post number : ' + str(post_number))
    print('Post by : ' + str(request['username']))
    print('Topic : ' + str(request['topic'][0]['topic_name']))
    print('Title : ' + str(request['title']))
    print('Message : ' + str(request['message']))
    print('Likes : ' + str(request['likes']))
    print('Dislikes : ' + str(request['dislikes']))
    for comment in request['feedbacks']:
        print('Comment: ' + str(comment['comment']))
        print('Commented by: '+ str(comment['username']))
        
"""
TC 19. Nick browses all the expired messages in Sport topic. These should be empty
"""

print('\n\n\nTC 19. Nick browses all the expired messages in Sport topic. These should be empty\n\n\n')

import requests
sports_posts_URL = 'http://127.0.0.1:8000/v1/expiredmessagebytopic/S/'
access_token = nick['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}

nick_request = requests.get(sports_posts_URL, headers = headers)

if ("post_identifier" not in nick_request.json()):
    print("******No records found******")
else:
    

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
        for comment in request['feedbacks']:
            print('Comment: ' + str(comment['comment']))
            print('Commented by: '+ str(comment['username']))
            
"""
TC 20. Nester queries for an active post having the hightest interest 
(maximum sum of likes and dislikes) in the Tech topic. This should be Mary's post.
"""

print('\n\n\nTC 20. Nester queries for an active post having the hightest interest (maximum sum of likes and dislikes) in the Tech topic. This should be Mary\'s post.\n\n\n')

import requests
tech_posts_URL = 'http://127.0.0.1:8000/v1/messagebytopic/T/'
access_token = nester['access_token']
headers = {'Authorization': 'Bearer '+str(access_token)}

nester_request = requests.get(tech_posts_URL, headers = headers)

#Kindly note, I have set up most active post as TOTAL NUMBER OF INTERACTIONS instead of just LIKES + DISLIKES 
#as I believe that would give more accurate measure of 'activeness'. This can simple by changed in messaging/views.py
#I will add more details about that in my project report.

print('----------TOP POST-------------------')
print(nester_request.json()[0])
print('---------------------------------------------------')

print('Post by : ' + str(nester_request.json()[0]['username']))
print('Topic : ' + str(nester_request.json()[0]['topic'][0]['topic_name']))
print('Title : ' + str(nester_request.json()[0]['title']))
print('Message : ' + str(nester_request.json()[0]['message']))
print('Likes : ' + str(nester_request.json()[0]['likes']))
print('Dislikes : ' + str(nester_request.json()[0]['dislikes']))
print('Comments : ' + str(nester_request.json()[0]['feedbacks']))