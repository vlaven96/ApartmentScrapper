from abc import ABC, abstractmethod
from models.models import Apartment
class ApartmentScraper(ABC):
    @abstractmethod
    def get_apartment(self, url: str) -> Apartment:
        pass