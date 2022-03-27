from typing import List

import py
import pytest
from app import schemas

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate,res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

    
def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_get_one_post_not_exist(client,test_posts):
    res = client.get(f"/posts/888")
    assert res.status_code == 401

def test_authorized_user_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

def test_authorized_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/888")
    assert res.status_code == 404

@pytest.mark.parametrize("title,content,published",[("awesome new title","awesome new content",True),("favorite pizza","awesome new content",True),("awesome new title","awesome new content",True)])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client,test_user,test_posts):
    res = authorized_client.post("/posts/",json={"title":"Test title","content":"Test content for the test post"})
    created_post = schemas.Post(**res.json())
    assert created_post.published == True


def test_unauthorized_create_post(client,test_user,test_posts):
    res = client.post("/posts/",json={"title":"Test title","content":"Test content for the test post"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client,test_user,test_posts):
    res = authorized_client.delete("/posts/55555551515")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {"title":"updated title","content":"updated content","id":test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user,test_posts):
    data = {"title":"updated title","content":"updated content","id":test_posts[3].id}
    res = authorized_client.put(f"/posts/{test_posts[3].id}",json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_user,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_update_non_exist(authorized_client,test_user,test_posts):
    data = {"title":"updated title","content":"updated content","id":test_posts[3].id}
    res = authorized_client.put("/posts/55555551515",json = data)
    assert res.status_code == 404
