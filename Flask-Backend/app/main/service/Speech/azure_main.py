from .azure_text_to_speech import Presentation
from app.main.model.user.user import User
from app.main.model.user.user import User
from ..Text.GPT3_main import make_text_speach
import logging
from .config import inputs
from flask import jsonify
import uuid
from .config import config


log = logging.getLogger(__name__)

class UserSpeech:
    def __init__(self, request, file_name=None) -> None:
        self.request = request
        self.file_name = file_name
        self.user_id = self.get_user_id()

    @staticmethod
    def get_all_speech_input_options(self):
        """Get all the supported inputs in speech and text generator"""
        return jsonify({
            "speakers": list(inputs.speakers),
            "tunes": list(inputs.tunes),
            "length": list(inputs.length)
        })

    def get_user_id(self):
        data = self.request.headers.get('Authorization')
        auth_token = data.split(" ")[1]
       
        return User.decode_auth_token(auth_token)
    
    def get_file_name(self):
        return self.file_name or str(uuid.uuid4())
    
    def get_audio_file(self):
        return f"{config.S3_PATH_TEXT}/{self.user_id}/{self.get_file_name()}.txt"
    
    def get_text_file(self):
        return f"{config.S3_PATH_AUDIO}/{self.user_id}/{self.get_file_name()}.wav"

    @staticmethod
    def create_speech(self):

        self.speech_audio = Presentation(self.request, audio_path=self.get_audio_file())

        #1. Generate Speech content
        log.info("\nAction: make speech content")
        speech,code= make_text_speach(self.request, file_name=self.get_text_file())
        if code != 200:
            return speech, "", code
        
        #2. fetch content of text of the file
        log.info(f"\nAction: fetch the speech content for file: {speech['path']}")
        self.speech_audio.fetch_content_of_text_file(self.get_audio_file())
        
        #2. request synthesize the fetched text
        log.info(f"\nAction: start synthesize the content of the file: {speech['path']}!")
        status, code = self.speech_audio.sythesize_speech_and_save_to_aws()
        if "status" in status and status['status'] == "Failed":
            return status, "", code
        
        return {"status": "success", "file_name": self.file_name}, 200

    @staticmethod
    def stream_audio_file(self):
        # return the synthesized speech 
        log.info("\nAction: start stream the speech content!!")
        if not self.file_name:
            self.file_name = self.request.get("file_name")
        if not self.speech_audio:
            self.speech_audio = Presentation(self.request, audio_path=self.get_audio_file())
        return self.speech_audio.stream_audio_file()
    
    @staticmethod
    def stream_audio_file(self):
        # return the synthesized speech 
        log.info("\nAction: start stream the speech content!!")
        if not self.file_name:
            self.file_name = self.request.get("file_name")
        if not self.speech_audio:
            self.speech_audio = Presentation(self.request, audio_path=self.get_audio_file())
        return self.speech_audio.stream_audio_file()