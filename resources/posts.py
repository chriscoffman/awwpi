import os 
from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError 
from dotenv import load_dotenv
import requests 
from db import db 
from models import PostModel 
from flask import jsonify


from schemas import PostSchema 

blp = Blueprint("Posts", "posts", description="Operations on posts pulled from reddit") 


@blp.route("/post") 
class PostList(MethodView): 
    @blp.response(201, PostSchema)
    def post(self):
        """get most recent top post of the day off reddit and store the post in the database"""
        load_dotenv()
        auth = requests.auth.HTTPBasicAuth(os.getenv("CLIENT_ID"), os.getenv("SECRET_KEY"))
        data = { 
            'grant_type': 'password',
            'username': os.getenv("REDDIT_USERNAME"),
            'password': os.getenv("PASSWORD")  
            }
        headers = {'User-Agent': 'MyAPI.0.0.1'}
        res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers) 
        TOKEN = res.json()['access_token'] 
        headers['Authorization'] = f'bearer {TOKEN}'
        res = requests.get(
            'https://oauth.reddit.com/r/aww/top', 
            headers=headers, 
            params={
                'limit': '25',
                't': 'day',
                })

        for post in res.json()['data']['children']:
            post_data= {
            'url': post['data']['url'],
            'upvotes': post['data']['ups'],
            'title': post['data']['title'],
            'downvotes': post['data']['downs'],
            'fullname': post['kind'] + '_' + post['data']['id']
            } 
            post = PostModel(**post_data) 
            try:
                db.session.add(post)
                db.session.commit() 
                
                return post_data 
            except IntegrityError: 
                db.session.rollback() 
                pass 

    @blp.response(200, PostSchema)
    def get(self): 
        """get most recent post"""
        descending = PostModel.query.order_by(PostModel.id.desc())
        return descending.first() 


@blp.route("/posts") 
class PostsList(MethodView): 
    """return all posts"""
    @blp.response(200, PostSchema(many=True))
    def get(self): 
        return PostModel.query.all()