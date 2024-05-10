from django import forms
from .models import Receptionist, Patient,Appointment

class ReceptionistRegistrationForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = ['first_name','last_name','username', 'password']

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name','last_name','username', 'password', 'age', 'contact', 'dob', 'gender']

    
    exclude = ['last_login']    


class PreferencesForm(forms.Form):
    choice = forms.ChoiceField(choices=[('hospital', 'Hospital'), ('specialist', 'Specialist')])
    search_query = forms.CharField(max_length=255, required=True)    

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['user','hospital','specialist', 'date', 'status', 'visit_reason']
