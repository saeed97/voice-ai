"""
List of the supported APIs for users:
- Get list of voices names/samples 
- Synthesize speech and save speech to AWS by user
- Git list of saved speeches by user


Database:
each user:
- Speech Table: file_name,title,tune,speeker,speech content. 

class Presentation:
    username: str
    speech_content: str ---> change to a file from aws

    def sythesize_speech(): -> 
        return file_name
    
    def save_to_aws(path):
        return True/False
    
    def get_list_audio_files(path):
        return josnify(files)
    
    def add_data_info(audio_files_info):
        return audio_files_info
    
    def stream_audio_file(path)
        return preassigned_url
    
    def save_speech_info_to_database()
        return True/False
"""

import uuid
import azure.cognitiveservices.speech as speechsdk
from .config import config
from flask import make_response
from app.main.model.user.user import User
from app.main.util.AWS_S3.S3_operations import S3
import logging

log = logging.getLogger(__name__)

class Presentation:
    def __init__(self, request, audio_path, locally=False) -> None:
        self.user =  User.query.filter_by(email=request.get('email')).first()
        self.speech_content = None
        self.path = None
        self.locally = locally #  weather save audios locally or to AWS S3
        self.s3 = S3()
        self.audio_path = audio_path 
        self.speech_config = speechsdk.SpeechConfig(
            subscription=config.speech_key,
            region=config.service_region
        )
        # Required for WordBoundary event sentences.
        self.speech_config.set_property(
            property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestSentenceBoundary,
            value='true'
        )
            
    def fetch_content_of_text_file(self, path):
        self.speech_content =  self.s3.fetch_text_file(file_path=path)
        return self.speech_content
    


    # The language of the voice that speaks.
    def get_ssml_header(self, vocie_name=None):
        speech_synthesis_voice_name= vocie_name or 'en-US-JennyNeural'

        return f"""<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'>
            <voice name='{config.voice_name}'>
                <mstts:viseme type='redlips_front'/>
                {self.speech_content}
            </voice>
        </speak>"""
    
    def _sythesize_speech(self):
        # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

        # Synthesize the SSML
        ssml = self.get_ssml_header()
        log.info(f"User: {self.user.public_id} SSML to synthesize: \r\n{ssml}")

        speech_synthesis_result =  speech_synthesizer.speak_ssml_async(self.get_ssml_header(self.speech_content)).get()
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            log.info("SynthesizingAudioCompleted result")
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            log.info(f"Speech synthesis canceled: {cancellation_details.reason}")
            if (
                cancellation_details.reason == speechsdk.CancellationReason.Error
                and cancellation_details.error_details
            ):
                log.error(f"Error details: {cancellation_details.error_details}")
                log.error("Did you set the speech resource key and region values?")
                return False
        return speech_synthesis_result

    def sythesize_speech_and_save_locally(self):

        speech_synthesis_result = self._sythesize_speech()
        stream = speechsdk.AudioDataStream(speech_synthesis_result)

        # TODO: change the name of the file to the id of the audio generated randomly 
        stream.save_to_wav_file(f"./app/main/service/Speech/tmp_files/{self.user.public_id}/example.wav")
        self.audio_path =  f"./service/Speech/{self.user.public_id}/example.wav"
        return self.audio_path
    
    def sythesize_speech_and_save_to_aws(self):
        """Save audio to AWS"""
        # Upload the audio stream to S3
        speech_synthesis_result = self._sythesize_speech()
        return (
            self.s3.save_audioFile_to_bucket(
                speech_synthesis_result, self.audio_path
            )
            if speech_synthesis_result
            else (
                {"status": "Failed", "message": "Failed sythesize the speech!"},
                500,
            )
        )
        
    def stream_audio_file(self):
        return self.s3.get_audio_stream(self.audio_path)

        