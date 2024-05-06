import requests
import time
import json
from typing import Optional, Union, Callable, List

save_url = 'http://localhost:31991/v1.0/invoke/dapr-post/method/save'
del_url = 'http://localhost:31991/v1.0/invoke/dapr-post/method/del'
meta_url = 'http://localhost:31991/v1.0/invoke/dapr-post/method/meta'
comment_url = 'http://localhost:31991/v1.0/invoke/dapr-post/method/comment'
upvote_url = 'http://localhost:31991/v1.0/invoke/dapr-post/method/upvote'
read_url = 'http://localhost:31991/v1.0/invoke/dapr-post/method/read'
# state store url
state_url = 'http://localhost:31991/v1.0/state/post-store-test/'

# helper functions
def make_save_post(post_id: str, user_id: str, text: str, images: List[str]):
    cont = {
        'user_id': user_id,
        'text': text,
        'images': images,
    }
    return {
        'send_unix_ms': int(time.time() * 1000),
        'post_id': post_id,
        'content': cont,
    }

def make_meta(post_id: str, sent: Optional[str]=None, objects: Optional[dict]=None):
    payload = {
        'post_id': post_id,
    }
    if sent != None:
        payload['sentiment'] = sent
    if objects != None:
        payload['objects'] = objects
    payload['send_unix_ms'] = int(time.time() * 1000)
    return payload

def make_read(post_ids: List[str]):
    return {
        'post_ids': post_ids,
        'send_unix_ms': int(time.time() * 1000),
    }

def make_comment(post_id: str, user_id: str, comm_id: str, reply_to: str, text: str):
    comm = {
        'comment_id': comm_id,
        'user_id': user_id,
        'reply_to': reply_to,
        'text': text,
    }
    return {
        'post_id': post_id,
        'comm': comm,
        'send_unix_ms': int(time.time() * 1000),
    }

def make_upvote(post_id: str, user_id: str):
    return {
        'post_id': post_id,
        'user_id': user_id,
        'send_unix_ms': int(time.time() * 1000),
    }

def show_posts(postsjson: str):
    postsdata = json.loads(postsjson)
    posts = postsdata['posts']
    for post_id in posts:
        post = posts[post_id]
        print('-- post_id:', post_id)
        print('------ content:', post['content'])
        print('------ meta:', post['meta'])
        print('------ comments:', post['comments'])
        print('------ upvotes:', post['upvotes'])

# variables
post_id = 'post-0'
def inc_post_id():
    global post_id
    post_id = int(post_id.split('-')[-1]) + 1
    post_id = 'post-' + str(post_id)

print("------ save post contents ------")
save_req = make_save_post(
    post_id=post_id, 
    user_id='Integrity', 
    text='Fakers get out of academia!', 
    images=['FGW.jpg'],
)
r = requests.post(save_url, json=save_req)
print(r.text)

print("------ read post ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)

# # read store directly
# cont_url = state_url + post_id + '-ct'
# print(cont_url)
# r = requests.get(cont_url, json=read_req)
# print(r.text)

print("------ update post meta (empty) ------")
meta_req = make_meta(post_id=post_id)
r = requests.post(meta_url, json=meta_req)
print(r.text)
print("------ read post (no meta updated) ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)


print("------ update post meta (sentiment) ------")
meta_req = make_meta(post_id=post_id, sent='angry')
r = requests.post(meta_url, json=meta_req)
print(r.text)
print("------ read post (sentiment meta updated) ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)

print("------ update post meta (objects) ------")
meta_req = make_meta(post_id=post_id, objects={'FGW.jpg': 'Youguess'})
r = requests.post(meta_url, json=meta_req)
print(r.text)
print("------ read post (objects meta updated) ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)

print("------ add post comment ------")
comm_id = post_id + '-comm-0'
comm_req = make_comment(
    post_id=post_id, 
    user_id='ZhenShiYin',
    comm_id=comm_id, 
    reply_to='', 
    text='Why is this fucking liar never punished?')
r = requests.post(comment_url, json=comm_req)
print(r.text)
print("------ read post (comment updated) ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)

print("------ add another post comment ------")
comm_id = post_id + '-comm-1'
comm_req = make_comment(
    post_id=post_id, 
    user_id='JiaYuCun',
    comm_id=comm_id, 
    reply_to=post_id + '-comm-2', 
    text='The xila gangster :)')
r = requests.post(comment_url, json=comm_req)
print(r.text)
print("------ read post (another comment updated) ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)

print("------ add upvotes to post ------")
for i in range(0, 3):
    comm_req = make_upvote(post_id=post_id, user_id='cd-grp-chn-' + str(i))
    r = requests.post(upvote_url, json=comm_req)
    print(r.text)
print("------ read post (upvotes updated) ------")
read_req = make_read(post_ids=[post_id])
r = requests.get(read_url, json=read_req)
show_posts(r.text)

# post_id += 1