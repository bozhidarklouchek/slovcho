import requests, json

client_id = 'QJ4I9bfZT5jNKgavODggNw'
client_secret = '6V4DFZ-Z3JYuW3whyWfnOFGGXpov7w'
user_agent = 'TestScraper'
subreddit = 'Bulgaria'
specific_post_id = '170ip1v'
comments_url = f'https://reddit.com/r/{subreddit}/comments/{specific_post_id}.json'

def get_access_token(client_id, client_secret):
    auth_url = 'https://www.reddit.com/api/v1/access_token'
    auth_data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, auth=(client_id, client_secret), data=auth_data, headers={'User-Agent': user_agent})
    response_json = response.json()
    
    if 'access_token' in response_json:
        return response_json['access_token']
    else:
        raise Exception('Failed to get access token')
    
access_token = get_access_token(client_id, client_secret)
headers = {'Authorization': f'Bearer {access_token}', 'User-Agent': user_agent}


comments_response = requests.get(comments_url, headers=headers)

if comments_response.status_code == 200:
    data = comments_response.json()
    
    for item in data:
        json_object = json.dumps(item, indent=4)
        with open('test.json', 'w') as file:
            file.write(json_object)
    file.close()

else:
    print(f'Error: {comments_response.status_code}')