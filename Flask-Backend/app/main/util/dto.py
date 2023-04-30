from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class GPT3:
    api = Namespace('model', description='Querry the AI models for yourself!!')
    image_data = api.model('image_ai', {
        "prompt": fields.String(required=True, description='The Prompt details: Blue sky with sun!!'),
        "n": fields.Integer(required=True, description='Number of images: 1-10'),
        "size": fields.String(required=True, description='Size of image, ex:"1024x1024"')
    })
    text_data = api.model('text_ai', {
        "description": fields.String(required=True, description='The Prompt details: Blue sky with sun!!'),
        "tune": fields.String(required=True, description='The tune of speaker: Friendly, mad, sad,...!!'),
        "content": fields.String(required=True, description='Facts or more creative!'),
        "length": fields.Integer(required=True, description='Number of images: 1-10')
    })

class Speech:
    api = Namespace('model', description='Querry the AI models for yourself!!')
    text_data = api.model('text_ai', {
        "text": fields.String(required=True, description='The Prompt details: Blue sky with sun!!'),
    })

class Speech:
    api = Namespace('model', description='Querry the AI models for yourself!!')
    text_data = api.model('audio_ai', {
        "description": fields.String(required=True, description='The Prompt details: Blue sky with sun!!'),
        "tune": fields.String(required=True, description='The tune of speaker: Friendly, mad, sad,...!!'),
        "content": fields.String(required=True, description='Facts or more creative!'),
        "length": fields.Integer(required=True, description='Number of images: 1-10')
    })