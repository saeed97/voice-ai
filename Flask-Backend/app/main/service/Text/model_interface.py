

from abc import abstractmethod, ABC

class Model(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.body_request = None
        self.url_request = None
        self.params_request = None
        self.content_type = "text"
      
    @abstractmethod
    def get_body_request(self):
        return self.body_request

    @abstractmethod
    def get_url(self):
        return self.url_request
    
    @abstractmethod
    def get_params(self):
        return self.params_request

