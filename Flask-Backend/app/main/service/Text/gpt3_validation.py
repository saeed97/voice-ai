
import contextlib
from functools import wraps
from app.main.util.decorator import validate_result
import logging

log = logging.getLogger(__name__)

@validate_result
def get_request_result(request):
    """Parse the request result!!"""
    request = request.json()
    if request.get('error'):
        response_object = {
            'status': 'fail',
            'message': f'Invalid request: {request["error"]["message"]}',
        }
        return response_object, 400
    if request.get("data") and request['data']:
        return clean_output_text(request['data'][0]), 200
    if request.get("choices") and request['choices']:
        return clean_output_text(request['choices'][0]), 200
    return (
        {'status': 'fail', 'message': 'Unexpected Error!!'},
        400,
    )

def clean_output_text(output):
    with contextlib.suppress(KeyError):
        text = output['text']
        text = text.replace("\n", "")
        text = text.replace("\\", "")
        output['text'] = text
    return output


def validate_input_internally(f):
    @wraps(f)
    def decorated(self, *args,**kwargs):
        log.info("Action: validate input!!")
        print(self.request.validate_request())
        validate, error = self.request.validate_request()
        err_mess = {"status": "Fail", "message": "Input validation error"}
       
        if isinstance(error, dict):
            err_mess.update(error)

        return f(self,*args,**kwargs) if validate else (err_mess, 400)

    return decorated

def validate_speech_result(f):
    @wraps(f)
    def decorated(self, *args,**kwargs):
        request_result = f(self,*args,**kwargs)
        if isinstance(request_result, str):
            return {"status":"success", "text": request_result}, 200
        return request_result

    return decorated
