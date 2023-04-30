
import contextlib
import uuid
import requests
import json
import logging
from .model_interface import Model
from .GPT3_request import Request
from .config import config
from .gpt3_validation import validate_input_internally, validate_speech_result
from .gpt3_speach_sections import SpeechSection, MainPoints, Introduction, Body, Conclusion
from app.main.model.user.user import User
from app.main.util.AWS_S3.S3_operations import S3

log = logging.getLogger(__name__)


class Speech(Model):
    def __init__(self, user_request: dict) -> None:
        log.info(f"User request recieved for script generator: {user_request}\n")
        self.user_request = user_request
        self.final_payload = None
        self.title = user_request['description']
        self.length = user_request['length']
        self.tune = user_request['tune']
        self.content_type = "text"
        self.content_style = user_request["content"] # creative, facts, ..
        self.request = Request(self)
        self.model_type = config.MODEL
        self.new_file_name = None
        self.user = User.query.filter_by(email=user_request.get('email')).first()
        self.s3 = S3()
    
    @validate_input_internally
    # @validate_speech_result
    def get_full_sepeach(self):
        # get main points
        log.info("Action: get the the Full speech section!\n")
        main_points_ob = MainPoints(self.user_request)
        self.final_payload = main_points_ob.get_final_payload()
        request =  self.querry_gpt3_text()
        # if request failed
        if not self._did_request_accepted(request):
            return request
        main_points = main_points_ob.process_request_output(request)
        log.info(f"Main points of the speech: {main_points}!\n")


        # get introduction for the main points 
        intro_ob = Introduction({"description": main_points, "tune": self.tune, "content":self.content_style})
        request = self._get_part_specch(intro_ob, 'Introduction: ')
        # if request failed
        if not self._did_request_accepted(request):
            return request
        intro = request[0]['text']

        # get support for point 1, point2, points3
        details = []
        for point in main_points:
            point_ob = Body({"description": point, "tune": self.tune, "content":self.content_style})
            self.final_payload = point_ob.get_final_payload()
            request = self.querry_gpt3_text()
            # if request failed
            if not self._did_request_accepted(request):
                return request
            # point_det = point_ob.process_request_output(point_det)
            details.append(request[0]['text'])

        log.info(f"\nBody points: {details}\n")
        body = "\n".join(details)


        # draw conclusion from previous 
        con_ob = Conclusion({"description": main_points, "tune": self.tune, "content":self.content_style})
        request = self._get_part_specch(con_ob, '\nConclusion: ')
        # if request failed
        if not self._did_request_accepted(request):
            return request
        con = request[0]['text']
        
        # save speech into aws as text fil
        text = f"{intro}\n\n{body}\n\n{con}"

        if self.new_file_name:
            status,_ = self.save_speech_text(text)
            path = status['path']
            if status and status['status']=="Failed":
                log.error("ERROR: saving audio file to AWS!!")
                path = None
                return {"status": "fail", "message":  f"failed saving the aduio file to {self.new_file_name}"}, 500

        return {"status": "success", "text": text, "path": path}, 200
    
    def save_speech_text(self, text):
        """Save file to aws to retrieved later"""
        return self.s3.saveText_to_aws(text=text, file_path=self.new_file_name)
        

    def _get_part_specch(self, obj, part):
        self.final_payload = obj.get_final_payload()
        result = self.querry_gpt3_text()
        log.info(f"{part}{result}\n")
        return result
    
    def _did_request_accepted(self, request):
        with contextlib.suppress(KeyError or AttributeError):
            if request and request[1] == 200:
                return True
        return False 



    def get_body_request(self):
        """Lib to get body for the request based on the speech"""
        return {
            "model": self.model_type,
            "prompt": self.final_payload['prompt'],
            "max_tokens": self.final_payload['max_tokens'],
            "temperature": self.final_payload['temperature']
        }
        
    def get_params(self):
        return {"model": self.model_type}
    
    def get_url(self):
        return "https://api.openai.com/v1/completions"
    
   
    def querry_gpt3_text(self):
        return self.request.make_request(method="POST")