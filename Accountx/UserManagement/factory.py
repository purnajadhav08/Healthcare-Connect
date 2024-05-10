# healthcare/factory.py
from .models import Receptionist, Patient

class UserFactory:
    @staticmethod
    def create_user(user_type, data):
        if user_type == 'receptionist':
            return Receptionist.objects.create(**data)
        elif user_type == 'patient':
            return Patient.objects.create(**data)
        else:
            raise ValueError("Invalid user type")
