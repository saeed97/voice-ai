
""""
Instructions:
The maximum allowed total tokens are 4075. Please, in the code
we calculate the token by multibly MAX_TOKEN*MAX_LENGTH. 

Note: the user description words are also considered part of the total tokens, So make sure to consider the
user inuput, plus your instructions.

"""

class config:
    MAX_TOKEN = 150 # Don not increase this more than 152. 
    WORDS_TO_TOKEN = 100 # 75word for 100 tokens
    MAX_LENGTH = 25 # in minutes
    MODEL = "text-davinci-003"
    SPEECH_POINTS = 3 # TODO: add this config to script files 

    #  AWS S3 Settings
    S3_PATH = 'speechtext'

