import os 
from flask.views import MethodView 
from flask_smorest import Blueprint, abort 

from passlib.hash import pbkdf2_sha256

from models import UserModel, PostModel
from schemas import UserSchema, PostSchema

import requests 

blp = Blueprint("Users", "users", description="Operations on users") 


def send_emails(to, subject, body): 
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", os.getenv("MAILGUN_API_KEY")),
		data={"from": f"Chris Coffman <mailgun@{domain}>",
			"to": to,
			"subject": subject,
			"text": body})

@blp.route("/register") 
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data): 
        if UserModel.find_by_email(user_data["email"]):
            abort(400, message="That email is already taken.") 
        
        user = UserModel( 
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        user.save_to_db() 

        send_emails(
            to=user.email,
            subject="Thank you for signing up for the awwpi!",
            body="You have signed up for the awwpi, and will now be able to receive emails of the top posts from the aww subreddit."
            )

        return {"message": "You have successfully registered!"}


@blp.route("/users/top_post") 
class UsersList(MethodView): 
    """
    access data while testing the app, 
    do not allow access to public users
    """
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all() 
        recent_post = PostModel.query.order_by(PostModel.id.desc()).first()
        for user in users:
            send_emails(user.email, recent_post.title, recent_post.url) 
        return users 





