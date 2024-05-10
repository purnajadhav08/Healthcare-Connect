from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ReceptionistRegistrationForm, PatientRegistrationForm
from .factory import UserFactory
from .composite import IndividualPatient, PatientGroup
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Receptionist,Patient,Hospital,Specialist,Appointment
from django.shortcuts import render, get_object_or_404
from .forms import PreferencesForm
from .strategy import HospitalStrategy, SpecialistStrategy
from django.urls import reverse
from django.utils.dateparse import parse_datetime


def index(request):
    return render(request, 'base.html')


def admin_dashboard(request, receptionist_id):
    receptionist = get_object_or_404(Receptionist, id=receptionist_id)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            patient_component = IndividualPatient(patient)
            return render(request, 'admin_dashboard.html', {'receptionist': receptionist, 'patient_data': [patient_component.display_info()]})

    
    patients = receptionist.patients.all()
    patient_group = PatientGroup([IndividualPatient(patient) for patient in patients])

    return render(request, 'admin_dashboard.html', {'receptionist': receptionist, 'patient_data': patient_group.display_info()})

def patient_dashboard(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

   
    search_suggestions_url = reverse('search_suggestions')

    return render(request, 'patient_dashboard.html', {'patient': patient, 'search_suggestions_url': search_suggestions_url})


def register_user(request, user_type):
    form_class = ReceptionistRegistrationForm if user_type == 'receptionist' else PatientRegistrationForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = UserFactory.create_user(user_type, data)
            login(request, user)
            if user_type == 'receptionist':
                receptionist_id = user.receptionist.user_ptr_id 
                return redirect('receptionist_dashboard', receptionist_id=receptionist_id)
            elif user_type == 'patient':
                patient_id = user.patient.user_ptr_id
                return redirect('patient_dashboard', patient_id=patient_id)
    else:
        form = form_class()
    
    return render(request, 'custom_register.html', {'form': form, 'user_type': user_type})



def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        print(f"Received data - username: {username}, password: {password}, user_type: {user_type}")

        if username is not None and password is not None:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                if user_type == 'admin':
                    return redirect('admin_dashboard')
                elif user_type == 'patient':
                    return redirect('patient_dashboard')

    else:
        
        return render(request, 'custom_login.html')

    return HttpResponse("Login failed. Handle the case when login fails.")


def patient_logout(request):
    logout(request)
    return redirect('custom_login')

def admin_logout(request):
    logout(request)
    return redirect('custom_login')


def suggestions(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            search_query = form.cleaned_data['search_query']

            if choice == 'hospital':
                strategy = HospitalStrategy()
            elif choice == 'specialist':
                strategy = SpecialistStrategy()
            else:
                strategy = None

            if strategy:
                suggestions = strategy.suggest(search_query)
                return render(request, 'suggestions.html', {'suggestions': suggestions, 'choice': choice, 'search_query': search_query})

    else:
        form = PreferencesForm()

    return render(request, 'search_form.html', {'form': form})

def book_appointment(request):
    if request.method == 'POST':
        # Extracting data from the form
        first_name = request.POST.get('firstName')
        birth_date = request.POST.get('birthDate')
        appointment_date = request.POST.get('appointmentDate')
        appointment_time = request.POST.get('appointmentTime')
        preferred_physician = request.POST.get('preferredPhysician')
        visit_reason = request.POST.get('visitReason')

        # Date and time parsing and combining
        date = parse_datetime(appointment_date + " " + appointment_time)

        # Example: Fetch user, hospital, and specialist based on form data.
        # Adjust the logic based on how you want to find these entities.
        user = Receptionist.objects.filter(first_name=first_name, date_of_birth=birth_date).first()
        hospital = Hospital.objects.first()  # Placeholder: Replace with actual logic
        specialist = Specialist.objects.filter(name=preferred_physician).first()

        if not all([user, hospital, specialist, date]):
            # Handle the case where any of the required entities are not found or date is invalid
            return HttpResponse("Invalid data provided", status=400)

        # Create and save the appointment
        appointment = Appointment(
            user=user,
            hospital=hospital,
            specialist=specialist,
            date=date,
            status='Scheduled',
            visit_reason=visit_reason
        )
        appointment.save()
        return HttpResponse("Appointment created successfully")

    else:
        # For a GET request, render the empty form
        hospitals = Hospital.objects.all()  # If you have a list of hospitals to choose from
        specialists = Specialist.objects.all()  # If you have a list of specialists to choose from
        return render(request, 'book_appointment.html', {'hospitals': hospitals, 'specialists': specialists})

