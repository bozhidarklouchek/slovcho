import requests, csv, time

# Reddit API credentials
client_id = 'QJ4I9bfZT5jNKgavODggNw'
client_secret = '6V4DFZ-Z3JYuW3whyWfnOFGGXpov7w'
user_agent = 'TestScraper'
max_depth = 5  # Adjust the maximum depth you want to fetch replies to
# subreddit = 'BulgariaPics'
reddit_username = 'FewExcitement5823'
requests_made = 0
row_max = 50000

subreddits = ['BulgariaPics', 'bulgariaeu', 'Bulgaria', 'Sofia', 'Varna_Bulgaria']

# Authentication
def get_access_token(client_id, client_secret):
    auth_url = 'https://www.reddit.com/api/v1/access_token'
    auth_data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, auth=(client_id, client_secret), data=auth_data, headers={'User-Agent': user_agent})
    response_json = response.json()
    
    if 'access_token' in response_json:
        return response_json['access_token']
    else:
        raise Exception('Failed to get access token')
    
def fetch_replies(comment, depth=0):
    # print(comment)
    if(comment["kind"] != "more"):
        comment_data = comment['data']
        try:
            writer.writerow([subreddit, 'Comment', comment_data['id'], '-', comment_data['body']])
            global rows
            rows += 1
        except: 
            print(comment_data)
        print('Added comment')
        
        # Recursive call to fetch replies to this comment
        if depth < max_depth:
            if comment_data["replies"] != "":
                replies = comment_data["replies"]["data"].get("children", [])
                for reply in replies:
                    fetch_replies(reply, depth + 1)

access_token = get_access_token(client_id, client_secret)

# Make the API request
headers = {'Authorization': f'Bearer {access_token}', 'User-Agent': user_agent}


for subreddit in subreddits:
    print("Starting on r/", subreddit)
    end_curr_subreddit = False
    need_to_exit = False
    rows = 0
    limit = 100  # Number of posts to retrieve per request
    offset = 0  # Starting point (post index) for retrieval

    with open(f'{subreddit}.csv', 'r+', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['subreddit', 'content_type', 'id', 'title' 'content'])
        
        while not need_to_exit:
            # API endpoint for fetching posts
            url = f'https://reddit.com/r/{subreddit}/new.json?limit={limit}&count={offset}'

            time.sleep(2)
            if end_curr_subreddit:
                break
            response = requests.get(url, headers=headers)

            if response.status_code == 200:

                requests_made += 1
                print("(Get posts) this was request number ", requests_made)
                data = response.json()
                posts = data['data']['children']
                print("Need to go through ", len(posts), " posts")
                if(len(posts) != 100):
                    end_curr_subreddit = True
                for post in posts:
                    post_data = post['data']
                    # print(f'Title: {post_data["title"]}')
                    # print(f'Author: {post_data["author"]}')
                    # print(f'URL: {post_data["url"]}')

                    writer.writerow([subreddit, 'Post', post_data['id'], post_data["title"], post_data['selftext']])
                    rows += 1
                    print('Added post')

                    # Retrieve comments for the post
                    post_id = post_data['id']
                    comments_url = f'https://reddit.com/r/{subreddit}/comments/{post_id}.json'

                    while True:
                        time.sleep(2)
                        comments_response = requests.get(comments_url, headers=headers)

                        if comments_response.status_code == 200:
                            requests_made += 1
                            print("(Get comments) of ", post_id,"; this was request number ", requests_made)

                            comments_data = comments_response.json()
                            comments = comments_data[1]['data']['children']
                            # print('Comments:')
                            for comment in comments:
                                fetch_replies(comment, depth=0)
                            break
                                
                        elif comments_response.status_code == 429:
                            print("Limit reached. Waiting 120 seconds.")
                            time.sleep(120)

                        else:
                            print(f'Error: {comments_response.status_code}')

                    if rows + 1 >= row_max:
                        need_to_exit = True
                        break
                # Increment the offset for the next request
                if need_to_exit:
                    break
                offset += limit
            elif response.status_code == 429:
                print("Limit reached. Waiting 120 seconds.")
                time.sleep(120)
            else:
                print(f'Error: {response.status_code}')