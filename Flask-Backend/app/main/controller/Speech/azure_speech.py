from flask import request
from flask_restx import Resource

from app.main.service.Speech.azure_main import UserSpeech

from app.main.util.decorator import admin_token_required, token_required
from app.main.util.dto import Speech
from flask import render_template, send_file, make_response

api = Speech.api
text_data = Speech.text_data
speech = UserSpeech()

# @api.route('/text')
# class Speeches(Resource):
#     # @token_required
#     def get(self):
#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template('templates/index.html'),200,headers)

@api.route('/inputs')
class SpeechInputs(Resource):
    # @token_required
    @api.response(200, 'input has fetched')
    @api.doc('Get Input')
    def get(self):
        return UserSpeech.get_all_speech_input_options()

# @api.route('/speech')
# class Speech(Resource):
#     # @token_required
#     def get(self):
#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template('templates/speeches.html'),200,headers)

# @api.route('/synthesize')
# class synthesize(Resource):
#     # @token_required
#     @api.expect(text_data, validate=True)
#     @api.doc("Create audio file from text")
#     def post(self):
#         data = request.json
#         presentation = get_presentation(data)
#         try: 
#             audio_stream, code, audio_path =  presentation
#             if code != 200:
#                 message = audio_stream
#                 return message, code
#             return send_file(audio_stream, attachment_filename=audio_path)
#         except Exception:
#             # send audio file with excuse message instead 
#             return send_file(presentation[0][0], attachment_filename=audio_path[1])

@api.route("/create_speech")
class SpeechCreation(Resource):
    @api.doc("Create speech as requested")
    def post(self):
        print(request.json)
        speech = UserSpeech(request)
        return speech.create_speech()

@api.route("/script")
class SpeechCreation(Resource):
    @api.doc("Get speech Script")
    def get(self):
        speech = UserSpeech(request)
        return speech.get_script_file()

@api.route("/audio")
class SpeechCreation(Resource):
    @api.doc("Create speech Audio")
    def get(self):
        speech = UserSpeech(request)
        return speech.get_audio_file()
