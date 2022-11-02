from marshmallow import Schema, fields 

class PostSchema(Schema): 
    id = fields.Int(dump_only=True) 
    title = fields.Str(required=True) 
    url = fields.Str(required=True) 
    upvotes = fields.Int(required=True) 
    downvotes = fields.Int(required=True) 
    fullname = fields.Str(required=True) 


class UserSchema(Schema): 
    id = fields.Int() 
    email = fields.Str() 
    password = fields.Str(load_only=True) 
    