from db import db 

class PostModel(db.Model): 
    __tablename__ = "posts" 

    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(), unique=False, nullable=False) 
    url = db.Column(db.String(), unique=False, nullable=False) 
    upvotes = db.Column(db.Integer, unique=False, nullable=False) 
    downvotes = db.Column(db.Integer, unique=False, nullable=False) 
    fullname = db.Column(db.String(), unique=True, nullable=False) 
