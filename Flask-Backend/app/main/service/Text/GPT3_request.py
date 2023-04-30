from validator import validate 
import logging
import os
import requests
import json
from .gpt3_validation import get_request_result
from .model_interface import Model

log = logging.getLogger(__name__)


TOKEN = os.getenv("OPENAI_API_KEY")

class requestTypes:
    TEXT_REQUEST = "text"
    IMAGE_REQUEST = "image"
    SOUND_REQUEST = "sound"

class Request:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.headers =  {
        'Content-Type': 'application/json',
        'Authorization': TOKEN
        }
        self.content_type = model.content_type
        self.request_body = None
        self.user_request = model.user_request
        self.url_request = None
        self.params = None
        self.text_request = {
            "description": "required",
            "tune": "required",
            "content": "required",
            "length": "required|min:1"
            }
            
        self.image_request = {
            "description": "required",
            "size": "required",
            "number": "required|min:1",
            }
        self.sound_request = {

        }
        
    def validate_request(self):
        """Vladiate the request comming as expected"""

        result = True # validated correctly
        errors = None
        if self.content_type == requestTypes.TEXT_REQUEST:
            result,_, errors = validate(self.user_request, self.text_request, return_info=True)
        elif self.content_type == requestTypes.IMAGE_REQUEST:
            result,_, errors = validate(self.user_request, self.image_request, return_info=True)
        
        elif self.content_type == requestTypes.SOUND_REQUEST:
            # TODO: add this part
            result,_, errors = validate(self.user_request, self.sound_request, return_info=True)
        return  result, errors

    def set_request_data_for_model(self):
        """Get Data for text completion request"""
        # get description request
        self.body_request = self.model.get_body_request()

        # get URl
        self.url_request = self.model.get_url()

        # get params
        self.params = self.model.get_params()
        
        return True
    
    def make_request(self, method):
        error_mess = {"status": "FAIL", "message": "Internal Server ERROR!"}, 500
        log.info("Action: Set up request info!")

        self.set_request_data_for_model()
        return self._make_request(method)
        # try:
        #     log.info("Action: Set up request info!")
        #     self.set_request_data_for_model()

        # except Exception as e:
        #     log.error("ERROR: error during setting up request speach paramters!!")
        #     return error_mess

        # try:
        #     return self._make_request(method)
        # except Exception as e:
        #     log.error("ERROR: error during setting up request speach paramters!!")
        #     return error_mess

    def _make_request(self, method):
        log.info("Action: make request!")
        log.info(f"Body request for url {self.url_request}:  {self.body_request}")
        request = None

        if method == "POST":
            request = requests.post(self.url_request, params=self.params, headers=self.headers, data=json.dumps(self.body_request))

        if method == "GET":
            request = requests.get(self.url_request, params=self.params, headers=self.headers, data=json.dumps(self.body_request))

        if method == "PUT":
            request = requests.put(self.url_request, params=self.params, headers=self.headers, data=json.dumps(self.body_request))

        return get_request_result(request)
