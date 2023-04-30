

"""
Author: Muammar Saeed
This file is to orgnize all the tunes of the application based on the temperature 
of the request.
Tunes:
- Friendly
- Luxury
- Sadness
- Happyness 
- Persuasive 
"""
from .config import config
from abc import abstractmethod, ABC
from .gpt3_validation import clean_output_text

class SpeechSection:
    def __init__(self, data:  dict) -> None:
        self.data = data 

    @abstractmethod
    def get_description(self, description, tune):
        pass

    def get_required_temperature(self, content):
        return 0 if content.find("fact") != -1 else 0.8

    def calculate_required_length(self):
        return config.MAX_TOKEN * config.MAX_LENGTH

    def get_final_payload(self):
        return {
        "prompt" : self.get_description(self.data['description'], self.data['tune']),
        "max_tokens": self.calculate_required_length(),
        "temperature": self.get_required_temperature(self.data['content'])
        }
    
    @abstractmethod
    def process_request_output(self, output):
        pass

    
class MainPoints(SpeechSection):
    def __call__(self, *args, **kwds) -> None:
        return super().__call__(*args, **kwds)
    
    def get_description(self, description, tune):
        return f"""
        You are a professional and creative speaker.\n
        Give me at least three solid points to talk about on my speech that has to be {tune}\n
        Each point should start with "_" without numbers
        the title has the following description:\n {description}\n.
        """
    
    def process_request_output(self, output):
        """This lib is to process the text and split the points into list"""
        print("procissssss")
        output = output[0]['text'].split("_")
        output = [point.replace("_","") for point in output][1:4]
        return output


class Introduction(SpeechSection):
    def __init__(self, *args, **kwds) -> None:
        self.length = 2
        return super().__init__(*args, **kwds)
    
    def get_description(self, description, tune):
        return f"""
        Give me a really powerfull amazing speech introduction using the three main points you mentioned ealier {"".join(description)}
        with tune {tune}. I am using these points for my speech. Do not end with thank you, make the introduction as it is opening for my speech.
        Give me the script straight, do not add sub text like "Example Introduction:". Do not start Speech with Good morning or Good evening.
        """
    
class Body(SpeechSection):
    def __init__(self, *args, **kwds) -> None:
        self.num = 0
        return super().__init__(*args, **kwds)
    
    def get_description(self, description, tune):
        self.num +=1
        return f"""
            I have a speech I asked  you about earlier, and my first point in the body is {description}. 
            Give me a really supporting solid details as speech script for the {self.num + 1} of my speech {tune}, dont forgot
            to give me the speech script in {tune} tune. Remember, this is not introduction neither conclusion, I still have other point to mention. 
            Give me the script straight, do not add sub text like "Example Speech Script:". Also you can add speech punctuation, popular qoutotes, stories or statstic data as necessary.
            """
        
class Conclusion(SpeechSection):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
    
    def get_description(self, description, tune):
        return f"""
        Give me a really powerfull amazing speech conclusion using the three main points you mentioned ealier {"".join(description)}
        with tune {tune}. I used these points for my speech. Wrap my speech in beatiful way!
        Give the script straight, do not add sub text like "Example Conclusion:"
        """
