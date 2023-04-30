from flask import request
from flask_restx import Resource

from app.main.service.Text.GPT3_main import make_text_speach

from app.main.util.decorator import admin_token_required, token_required
from app.main.util.dto import GPT3
from typing import Dict, Tuple

api = GPT3.api
image_data = GPT3.image_data
text_data = GPT3.text_data



@api.route('/image')
class PromptImage(Resource):
    @api.expect(image_data, validate=True)
    @api.doc('Request a  New image')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Request a new image """
        data = request.json
        return querry_qpt3_image(data=data)

@api.route('/text')
class PromptText(Resource):
    @api.expect(text_data, validate=True)
    @api.doc('Generate New Text')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Request new text completion """
        data = request.json
        return make_text_speach(data=data)


