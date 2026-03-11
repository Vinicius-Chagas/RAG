from abc import ABC, abstractmethod

class ExtractorCreator(ABC):

    @abstractmethod
    def getExtractor(self):
        pass

        