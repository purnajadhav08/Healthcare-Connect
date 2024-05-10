# healthcare/urls.py
from django.urls import path
from .views import index,register_user, authenticate_user, admin_dashboard, patient_dashboard,patient_logout,admin_logout,suggestions,book_appointment

urlpatterns = [
    path('', index, name='base'),
    path('<str:user_type>/register/', register_user, name='register_user'),
    path('login/', authenticate_user, name='custom_login'),
    path('receptionist/dashboard/<int:receptionist_id>/', admin_dashboard, name='receptionist_dashboard'),
    path('patient/dashboard/<int:patient_id>/', patient_dashboard, name='patient_dashboard'),
    path('patient/logout/', patient_logout, name='patient_logout'),
    path('receptionist/logout/', admin_logout, name='admin_logout'),
    path('search/', suggestions, name='search_suggestions'),
    path('bookappointment/', book_appointment, name='book_appointment'),

    # Add more URLs for other views as needed
]