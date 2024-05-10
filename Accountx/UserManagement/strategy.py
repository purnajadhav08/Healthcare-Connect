# strategy.py
from abc import ABC, abstractmethod
from .models import Hospital,Specialist

class RecommendationStrategy(ABC):
    @abstractmethod
    def suggest(self, search_query):
        pass

class HospitalStrategy(RecommendationStrategy):
    def suggest(self, search_query):
        suggestions = Hospital.objects.filter(name__icontains=search_query)
        return suggestions

class SpecialistStrategy(RecommendationStrategy):
    def suggest(self, search_query):
        suggestions = Specialist.objects.filter(name__icontains=search_query)
        return suggestions
