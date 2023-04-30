

from .querry_gpt3_text import Speech
import uuid

def make_text_speach(data, file_name=None):
    speech_script = Speech(data)
    speech_script.new_file_name = file_name
    return speech_script.get_full_sepeach()
