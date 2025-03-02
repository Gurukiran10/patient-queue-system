import logging
from flask import Flask, flash, json, render_template, redirect, url_for, request, session, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import random
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
import string
from flask_mail import Mail, Message



from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from pymongo import MongoClient
import random
from bson import ObjectId

# Initialize Flask App and MongoDB
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Setup (adjust with your MongoDB URI)
client = MongoClient("mongodb://localhost:27017/")
mongo = client['clinic_db']

# Flask-Mail Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail example
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# Translations Dictionary (example for 'en')
translations = {
    'en': {
        'slot_booked': 'The selected slot is already booked.',
        'appointment_successful': 'Your appointment has been successfully booked.',
        'appointment_confirmation': 'Appointment Confirmation',
        'doctor': 'Doctor',
        'date': 'Date',
        'time': 'Time',
        'book_appointment': 'Book Appointment',
        'logout': 'Logout',
        'back': 'Back',
    }
}





# Initialize Flask app
#app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['MONGO_URI'] = 'mongodb://localhost:27017/patient_queue'
mongo = PyMongo(app)

translations = {
    'en': {
        'dashboard_title': 'Admin Dashboard',
        'logout': 'Logout',
        'manage_users': 'Manage Users',
        'view_feedback': 'View Feedback',
        'book_appointment': 'Book Appointment',
        'doctor': 'Doctor',
        'date': 'Date',
        'time': 'Time',
        'submit': 'Book Appointment',
        'back': 'Back',
        'doctor_dashboard': 'Doctor Dashboard',
        'appointments': 'Appointments',
        'profile': 'Profile',
        'patient': 'Patient',
        'room_number': 'Room Number',
        'welcome': 'Welcome, Dr.',
        'manage_your_account': 'Here you can manage your appointments, update your profile, and more.',
        'update_profile': 'Update Profile',
        'manage_your_information': 'Manage your personal and professional information.',
        'manage_appointments_title': 'Manage Appointments',
        'manage_appointments_header': 'Appointments for Dr.',
        'registration_success': 'Registration successful!',
        'appointment_id': 'Appointment ID',
        'patient_name': 'Patient Name',
        'appointment_date': 'Date',
        'appointment_time': 'Time',
        'actions': 'Actions',
        'cancel': 'Cancel',
        'back_to_dashboard': 'Back to Dashboard',
        'appointment_successful': 'Appointment successfully updated!',
        'slot_booked': 'Slot successfully booked!',
        'lang': 'en',
        'go': 'Go',
        'view_and_manage_appointments': 'View and manage your scheduled appointments.',
        'name': 'Name',
        'age': 'Age',
        'qualification': 'Qualification',
        'branch': 'Branch',
        'phone_number': 'Phone Number',
        'profile_updated': 'Profile updated successfully',
        'available_time': 'Available Time',
        'login': 'Login',
        'username': 'Username',
        'password': 'Password',
        'register': 'Register',
        'patient_username': 'Patient Username',
        'appointment_date': 'Appointment Date',
        'appointment_time': 'Appointment Time',
        'appointment_type': 'Appointment Type',
        'status': 'Status',
        'accept': 'Accept',
        'reject': 'Reject',
        'approved_doctors': 'Approved Doctors',
        'approved_patients': 'Approved Patients',
        'approve': 'Approve',
        'delete': 'Delete',
        'patient_dashboard': 'Patient Dashboard',
        'welcome': 'Welcome',
        'overview': 'Overview of your appointments and actions.',
        'book_appointment': 'Book Appointment',
        'view_appointments': 'View Appointments',
        'submit_feedback': 'Submit Feedback',
        'find_nearby_hospitals': 'Find Nearby Hospitals',
        'schedule': 'Schedule a new appointment with a doctor.',
        'check_appointments': 'Check your upcoming and past appointments.',
        'manage_info': 'Manage your personal information and settings.',
        'doctor_dashboard': 'Doctor Dashboard',
        'logout': 'Logout',
        'welcome': 'Welcome',
        'dashboard_greeting': 'Here is your dashboard overview',
        'profile_update': 'Profile Update',
        'profile_update_desc': 'Update your profile information here.',
        'manage_appointments': 'Manage Appointments',
        'manage_appointments_desc': 'Manage your appointments with patients.',
        'go': 'Go',
        'provide_feedback': 'Provide feedback on your experience.',
        'sign_out': 'Sign out of your account.',
        'locate_hospitals': 'Locate hospitals near you.',
        'patient_profile': 'Patient Profile',
        'save_changes': 'Save Changes',
        'male': 'Male',
        'female': 'Female',
        'other': 'Other',
        'a_plus': 'A+',
        'a_minus': 'A-',
        'b_plus': 'B+',
        'b_minus': 'B-',
        'ab_plus': 'AB+',
        'ab_minus': 'AB-',
        'o_plus': 'O+',
        'o_minus': 'O-',
        'register': 'Register',
        'role': 'Role',
        'admin': 'Admin',
        'doctor': 'Doctor',
        'patient': 'Patient',
        'hospital_feedback_summary': 'Hospital Feedback Summary',
        'enter_feedback': 'Enter your feedback here...',
        'analyze_feedback': 'Analyze Feedback',
        'back': 'Back',
        'please_enter_feedback': 'Please enter your feedback.',
        'feedback_summary': 'Feedback Summary',
        'error_submitting_feedback': 'Error submitting feedback.',
        'error_analyzing_feedback': 'Error analyzing feedback.',
        'your_appointments': 'Your Appointments',
        'doctor_username': 'Doctor Username',
        'no_appointments_found': 'No appointments found',
        'toggle_navigation': 'Toggle navigation',
        'dashboard_title': 'Dashboard',
        'user_deleted_successfully': 'User deleted successfully',
        'select_language': 'Select Language',
        'login': 'Login',
        'register': 'Register',
        'registration_success': 'Registration successful!',
        'account_not_approved': 'Your account is not approved yet. Please contact the administrator.',
        'view_user': 'View User',
        'user_details': 'User Details',
        'appointment_status_updated': 'Appointment status updated',
        'appointment_update_failed': 'Appointment update failed',
        'user_approved_successfully': 'User approved successfully',
        'back_to_manage_users': 'Back to Manage Users',
        'invalid_credentials': 'Invalid credentials'
    },
    'kn': {
        'dashboard_title': 'ಅಡ್ಮಿನ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'logout': 'ಲಾಗ್ ಔಟ್',
        'manage_users': 'ಬಳಕೆದಾರರನ್ನು ನಿರ್ವಹಿಸಿ',
        'view_feedback': 'ಮತಾಮಸವನ್ನು ವೀಕ್ಷಿಸಿ',
        'book_appointment': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಬುಕ್ ಮಾಡಿ',
        'user_approved_successfully': 'ಬಳಕೆದಾರರನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಅನುಮೋದಿಸಲಾಗಿದೆ',
        'doctor': 'ಡಾಕ್ಟರ್',
        'appointment_status_updated': 'ನೇಮಕಾತಿ ಸ್ಥಿತಿ ನವೀಕರಿಸಲಾಗಿದೆ',
        'date': 'ದಿನಾಂಕ',
        'time': 'ಸಮಯ',
        'submit': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಬುಕ್ ಮಾಡಿ',
        'back': 'ಹಿಂದೆ',
        'doctor_dashboard': 'ಡಾಕ್ಟರ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'appointments': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳು',
        'profile': 'ಪ್ರೊಫೈಲ್',
        'patient': 'ರೋಗಿ',
        'room_number': 'ಕೋಣೆ ಸಂಖ್ಯೆ',
        'welcome': 'ಸ್ವಾಗತ ಡಾ.',
        'manage_your_account': 'ಇಲ್ಲಿ ನೀವು ನಿಮ್ಮ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಬಹುದು, ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಅನ್ನು ನವೀಕರಿಸಬಹುದು, ಮತ್ತು ಇನ್ನೂ ಹೆಚ್ಚಿನವು ಮಾಡಬಹುದು.',
        'update_profile': 'ಪ್ರೊಫೈಲ್ ನವೀಕರಿಸಿ',
        'manage_your_information': 'ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಮತ್ತು ವೃತ್ತಿಪರ ಮಾಹಿತಿಯನ್ನು ನಿರ್ವಹಿಸಿ.',
        'appointment_successful': 'ಅಪಾಯಿಂಟ್ಮೆಂಟ್ ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ!',
        'dashboard_title': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'doctor_dashboard': 'ಡಾಕ್ಟರ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'logout': 'ಲಾಗ್ ಔಟ್',
        'welcome': 'ಸ್ವಾಗತ',
        'dashboard_greeting': 'ಇದು ನಿಮ್ಮ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಅವಲೋಕನವಾಗಿದೆ',
        'profile_update': 'ಪ್ರೊಫೈಲ್ ನವೀಕರಣ',
        'profile_update_desc': 'ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಮಾಹಿತಿಯನ್ನು ಇಲ್ಲಿ ನವೀಕರಿಸಿ.',
        'manage_appointments': 'ನೇಮಕಾತಿಗಳನ್ನು ನಿರ್ವಹಿಸಿ',
        'manage_appointments_desc': 'ರೋಗಿಗಳೊಂದಿಗೆ ನಿಮ್ಮ ನೇಮಕಾತಿಗಳನ್ನು ನಿರ್ವಹಿಸಿ.',
        'go': 'ಹೋಗಿ',
        'select_language': 'ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'login': 'ಲಾಗಿನ್',
        'register': 'ನೋಂದಣಿ',
        'registration_success': 'ನೋಂದಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ!',
        'account_not_approved': 'ನಿಮ್ಮ ಖಾತೆಯನ್ನು ಇನ್ನೂ ಅನುಮೋದಿಸಲಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಆಡಳಿತಗಾರರನ್ನು ಸಂಪರ್ಕಿಸಿ.',
        'go': 'ಹೋಗಿ',
        'manage_appointments': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ',
        'view_and_manage_appointments': 'ನಿಮ್ಮ ಶೆಡ್ಯೂಲ್ ಮಾಡಿದ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳನ್ನು ವೀಕ್ಷಿಸಿ ಮತ್ತು ನಿರ್ವಹಿಸಿ.',
        'name': 'ಹೆಸರು',
        'age': 'ವಯಸ್ಸು',
        'qualification': 'ಅರ್ಹತೆ',
        'branch': 'ಶಾಖೆ',
        'phone_number': 'ದೂರವಾಣಿ ಸಂಖ್ಯೆ',
        'available_time': 'ಲಭ್ಯವಿರುವ ಸಮಯ',
        'update_profile': 'ಪ್ರೊಫೈಲ್ ನವೀಕರಿಸಿ',
        'login': 'ಲಾಗಿನ್',
        'username': 'ಬಳಕೆದಾರರ ಹೆಸರು',
        'password': 'ಪಾಸ್ವರ್ಡ್',
        'register': 'ನೋಂದಣಿ',
        'patient_username': 'ರೋಗಿ ಬಳಕೆದಾರ ಹೆಸರು',
        'appointment_date': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ದಿನಾಂಕ',
        'appointment_time': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಸಮಯ',
        'appointment_type': 'ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಪ್ರಕಾರ',
        'status': 'ಸ್ಥಿತಿ',
        'accept': 'ಅಂಗೀಕರಿಸಿ',
        'reject': 'ನಿರಾಕರಿಸಿ',
        'approved_doctors': 'ಅಂಗೀಕೃತ ಡಾಕ್ಟರ್‌ಗಳು',
        'approved_patients': 'ಅಂಗೀಕೃತ ರೋಗಿಗಳು',
        'manage_appointments_title': 'ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ',
        'manage_appointments_header': 'ಡಾ.-ರ ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳು',
        'appointment_id': 'ಅಪಾಯಿಂಟ್ಮೆಂಟ್ ಐಡಿ',
         'registration_success': 'ನೋಂದಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ!',
        'patient_name': 'ಆಸ್ಪತ್ರೆ ಹೆಸರು',
        'appointment_date': 'ದಿನಾಂಕ',
        'appointment_time': 'ಸಮಯ',
        'actions': 'ಚಟುವಟಿಕೆಗಳು',
        'cancel': 'ಅಸ್ವೀಕೃತಿ',
        'back_to_dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂತಿರುಗಿ',
        'slot_booked': 'ಆಸಕ್ತಿ ಯಶಸ್ವಿಯಾಗಿ ಬುಕ್ಕಾಗಿದೆ!',
        'lang': 'kn',
        'username': 'ಬಳಕೆದಾರ ಹೆಸರು',
        'role': 'ಪಾತ್ರ',
        'approve': 'ಅಂಗೀಕರಿಸಿ',
        'delete': 'ಅಳಿಸಿ',
        'patient_dashboard': 'ರೋಗಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'welcome': 'ಸ್ವಾಗತ',
        'overview': 'ನಿಮ್ಮ ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳು ಮತ್ತು ಕ್ರಮಗಳ ಅವಲೋಕನ.',
        'book_appointment': 'ಅಪಾಯಿಂಟ್ಮೆಂಟ್ ಬುಕ್ ಮಾಡಿ',
        'view_appointments': 'ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳನ್ನು ನೋಡಿ',
        'submit_feedback': 'ಫೀಡ್‌ಬ್ಯಾಕ್ ಸಲ್ಲಿಸಿ',
        'profile_updated': 'ಪ್ರೊಫೈಲ್ ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ',
        'find_nearby_hospitals': 'ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಗಳನ್ನು ಹುಡುಕಿ',
        'schedule': 'ಡಾಕ್ಟರ್ ಜೊತೆಗೆ ಹೊಸ ಅಪಾಯಿಂಟ್ಮೆಂಟ್ ಅನ್ನು ಶೆಡ್ಯೂಲ್ ಮಾಡಿ.',
        'check_appointments': 'ನಿಮ್ಮ ಮುಂಬರುವ ಮತ್ತು ಹಿಂದಿನ ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.',
        'manage_info': 'ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಮಾಹಿತಿಯು ಮತ್ತು ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ.',
        'provide_feedback': 'ನಿಮ್ಮ ಅನುಭವದ ಕುರಿತು ಪ್ರತಿಕ್ರಿಯೆ ನೀಡು.',
        'sign_out': 'ನಿಮ್ಮ ಖಾತೆದಿಂದ ಲಾಗ್ ಔಟ್ ಮಾಡಿ.',
        'locate_hospitals': 'ನಿಮ್ಮ ಬಳಿ ಇರುವ ಆಸ್ಪತ್ರೆಗಳನ್ನು ಹುಡುಕಿ.',
        'patient_profile': 'ರೋಗಿಯ ಪ್ರೊಫೈಲ್',
        'save_changes': 'ಬದಲಾವಣೆಗಳನ್ನು ಉಳಿಸಿ',
        'male': 'ಪುರುಷ',
        'appointment_update_failed': 'ನೇಮಕಾತಿ ನವೀಕರಣ ವಿಫಲವಾಗಿದೆ',
        'female': 'ಮಹಿಳೆ',
        'other': 'ಇತರೆ',
        'a_plus': 'ಎ +',
        'a_minus': 'ಎ-',
        'b_plus': 'ಬಿ +',
        'b_minus': 'ಬಿ-',
        'ab_plus': 'ಎಬಿ +',
        'ab_minus': 'ಎಬಿ-',
        'o_plus': 'ಒ +',
        'o_minus': 'ಒ-',
        'register': 'ನೋಂದಣಿ',
        'role': 'ಪಾತ್ರ',
        'admin': 'ಅಡ್ಮಿನ್',
        'doctor': 'ಡಾಕ್ಟರ್',
        'patient': 'ರೋಗಿ',
        'hospital_feedback_summary': 'ಆಸ್ಪತ್ರೆಯ ಪ್ರತಿಕ್ರಿಯೆ ಸಾರಾಂಶ',
        'user_deleted_successfully': 'ಬಳಕೆದಾರರನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಅಳಿಸಲಾಗಿದೆ',
        'enter_feedback': 'ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆ ಇಲ್ಲಿ ನಮೂದಿಸಿ...',
        'analyze_feedback': 'ಮತಾಮಸ ವಿಶ್ಲೇಷಿಸಿ',
        'back': 'ಹಿಂತಿರುಗಿ',
        'please_enter_feedback': 'ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆ ನಮೂದಿಸಿ.',
        'feedback_summary': 'ಮತಾಮಸ ಸಾರಾಂಶ',
        'error_submitting_feedback': 'ಪ್ರತಿಕ್ರಿಯೆ ಸಲ್ಲಿಸುವಾಗ ದೋಷ.',
        'error_analyzing_feedback': 'ಮತಾಮಸವನ್ನು ವಿಶ್ಲೇಷಿಸುವಾಗ ದೋಷ.',
        'your_appointments': 'ನಿಮ್ಮ ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳು',
        'doctor_username': 'ಡಾಕ್ಟರ್ ಬಳಕೆದಾರ ಹೆಸರು',
        'no_appointments_found': 'ಯಾವುದೇ ಅಪಾಯಿಂಟ್ಮೆಂಟ್‌ಗಳನ್ನು ಕಂಡುಬಂದಿಲ್ಲ',
        'toggle_navigation': 'ನೇವಿಗೇಶನ್ ಅನ್ನು ಟಾಗಲ್ ಮಾಡಿ',
        'view_user': 'ಬಳಕೆದಾರನನ್ನು ವೀಕ್ಷಿಸಿ',
        'user_details': 'ಬಳಕೆದಾರ ವಿವರಗಳು',
        'registration_success': 'ನೋಂದಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ!',
        'back_to_manage_users': 'ಬಳಕೆದಾರರನ್ನು ನಿರ್ವಹಿಸಲು ಹಿಂದಿರುಗಿ',
        'invalid_credentials': 'ಅಮಾನ್ಯ ಪ್ರಮಾಣಪತ್ರಗಳು'
    }
}


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}



def get_translations(language):
    return translations.get(language, translations['en'])

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load NLTK stopwords
nltk.download('stopwords')

# Preprocessing function
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = [word.lower() for word in text.split() if word.lower() not in stop_words]
    return " ".join(tokens)

# Function to analyze and summarize feedback
def analyze_feedback(feedback_data):
    if not feedback_data:
        return []
    
    processed_feedback = [preprocess_text(feedback) for feedback in feedback_data]
    vectorizer = TfidfVectorizer(max_features=50)
    X = vectorizer.fit_transform(processed_feedback)
    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(X)
    common_issues = []
    terms = vectorizer.get_feature_names_out()
    for i in range(num_clusters):
        common_terms = [terms[ind] for ind in kmeans.cluster_centers_.argsort()[:, -1:-6:-1][i]]
        common_issues.append(" ".join(common_terms))
    return common_issues

# Route for rendering the feedback submission page
@app.route('/submit_feedback', methods=['GET'])
def feedback_page():
    return render_template('submit_feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.json.get('feedback')
    logger.debug(f"Feedback received: {feedback}")
    if feedback:
        feedback_data = load_feedback()
        logger.debug(f"Current feedback data: {feedback_data}")
        feedback_data.append(feedback)
        save_feedback(feedback_data)
        logger.debug("Feedback successfully saved.")
        return jsonify({"message": "Feedback submitted successfully!"}), 200
    else:
        logger.warning("No feedback provided in POST request.")
        return jsonify({"error": "No feedback provided!"}), 400
















@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    lang = request.args.get('language', 'en')
    trans = get_translations(lang)
    username = session['username']
    doctor = mongo.db.users.find_one({"username": username})

    if doctor is None:
        return redirect(url_for('login'))

    # Extract the doctor's name from the doctor object
    doctor_name = doctor.get('name', 'Doctor')  # Default to 'Doctor' if name is not found

    return render_template('doctor_dashboard.html', translations=trans, language=lang, doctor_name=doctor_name)



@app.route('/doctor/manage_appointments')
def manage_appointments():
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    doctor_username = session['username']
    appointments = mongo.db.appointments.find({"doctor_username": doctor_username})

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('language', 'en')
    translations = get_translations(lang)

    return render_template(
        'manage_appointments.html',
        appointments=appointments,
        username=doctor_username,
        translations=translations
    )


@app.route('/doctor/appointment_action/<appointment_id>/<action>')
def appointment_action(appointment_id, action):
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    if action not in ['accept', 'reject']:
        return "Invalid action"

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    translations = get_translations(lang)

    try:
        # Update appointment status in the database
        result = mongo.db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": action.capitalize()}}
        )

        if result.modified_count:
            # Retrieve the updated appointment
            appointment = mongo.db.appointments.find_one({"_id": ObjectId(appointment_id)})

            # Create the notification message
            message = f"Your appointment with Dr. {appointment['doctor_username']} on {appointment['appointment_date']} at {appointment['appointment_time']} has been {action.lower()}."

            # Create a notification entry in the notifications collection
            notification = {
                "_id": str(ObjectId()),  # Creating a unique notification ID
                "patient_username": appointment['patient_username'],
                "message": message,
                "status": "read",  # Default status to 'read'
                "appointment_id": str(appointment_id)
            }
            mongo.db.notifications.insert_one(notification)

            flash(translations['appointment_status_updated'], 'success')
        else:
            flash(translations['appointment_update_failed'], 'danger')

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')

    return redirect(url_for('manage_appointments', lang=lang))




















# MongoDB URI configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/patient_queue"  # MongoDB URI with database name
mongo = PyMongo(app)

@app.route('/blood_donation', methods=['GET'])
def blood_donation():
    """
    Render the Blood Donation Management page with the updated history from MongoDB.
    """
    search_region = request.args.get('region', '').lower()  # Get the search term from the query string
    print(f"Searching for donations with region: {search_region}")  # Debugging line
    
    if search_region:
        # Filter the history by region (case-insensitive)
        filtered_history = mongo.db.donations.find({"region": {"$regex": search_region, "$options": "i"}})
    else:
        filtered_history = mongo.db.donations.find()  # If no search term, show all history
    
    # Convert the cursor object to a list for rendering
    filtered_history = list(filtered_history)
    
    print(f"Found donations: {filtered_history}")  # Debugging line

    return render_template('blood_donation.html', history=filtered_history, search_region=search_region)


@app.route('/schedule_donation', methods=['POST'])
def schedule_donation():
    """
    Handle the form submission for scheduling a blood donation.
    Save the data to MongoDB and redirect back to the main page.
    """
    name = request.form['name']
    email = request.form['email']
    blood_group = request.form['blood_group']
    donation_date = request.form['donation_date']
    location = request.form['location']
    phone = request.form['phone']
    region = request.form['region']

    # Save the donation data to MongoDB (into donations collection)
    mongo.db.donations.insert_one({
        'name': name,
        'email': email,
        'blood_group': blood_group,
        'date': donation_date,
        'location': location,
        'phone': phone,
        'region': region
    })

    # Redirect back to the blood donation page
    return redirect(url_for('blood_donation'))
@app.route('/test_feedback', methods=['GET'])
def test_feedback():
    feedback_data = load_feedback()
    return jsonify(feedback_data)



@app.route('/analyze_feedback', methods=['GET'])
def analyze_feedback_route():
    try:
        feedback_data = load_feedback()
        if not feedback_data:
            return jsonify({"error": "No feedback available for analysis."}), 200
        
        summary = analyze_feedback(feedback_data)
        return jsonify({"summary": summary}), 200

    except Exception as e:
        app.logger.error(f"Error analyzing feedback: {e}")
        return jsonify({"error": "Error analyzing feedback."}), 500


def load_feedback():
    feedback_file = 'feedback.json'
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as file:
            return json.load(file)
    return []


def save_feedback(feedback_data):
    feedback_file = 'feedback.json'
    with open(feedback_file, 'w') as file:
        json.dump(feedback_data, file, indent=4)
        logger.debug(f"Saved feedback data: {feedback_data}")

@app.route('/', methods=['GET', 'POST'])
def index():
    language = request.form.get('language', 'en')
    translations = get_translations(language)
    
    # Render the index page with the updated language
    return render_template('index.html', translations=translations, language=language)



@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = request.args.get('language', 'en')
    trans = get_translations(lang)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongo.db.users.find_one({"username": username})

        if user and user['password'] == password:
            if user['role'] == 'patient' or user['approved']:
                session['username'] = username
                session['role'] = user['role']

                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard', language=lang))
                elif user['role'] == 'doctor':
                    return redirect(url_for('doctor_dashboard', language=lang))
                elif user['role'] == 'patient':
                    return redirect(url_for('patient_dashboard', language=lang))
            else:
                flash(trans['account_not_approved'], 'danger')
                return redirect(url_for('login', language=lang))
        else:
            flash(trans['invalid_credentials'], 'danger')
            return redirect(url_for('login', language=lang))

    return render_template('login.html', translations=trans)


@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = request.args.get('language', 'en')
    trans = get_translations(lang)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(password_regex, password):
            flash(trans['password_requirements'], 'danger')
            return redirect(url_for('register', language=lang))

        if mongo.db.users.find_one({"username": username}):
            flash(trans['username_exists'], 'danger')
            return redirect(url_for('register', language=lang))

        approved = role == 'patient'
        mongo.db.users.insert_one({"username": username, "password": password, "role": role, "approved": approved})

        flash(trans['registration_success'], 'success')
        return redirect(url_for('login', language=lang))

    return render_template('register.html', translations=trans)


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    lang = request.args.get('language', 'en')
    trans = get_translations(lang)
    users = mongo.db.users.find()

    return render_template('admin_dashboard.html', translations=trans, language=lang, users=users)


@app.route('/admin/manage_users')
def manage_users():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    pending_users = list(mongo.db.users.find({"approved": False}))
    doctors = list(mongo.db.users.find({"role": "doctor", "approved": True}))
    patients = list(mongo.db.users.find({"role": "patient", "approved": True}))

    return render_template('manage_users.html', 
                           pending_users=pending_users, 
                           doctors=doctors, 
                           patients=patients,
                           translations=trans)


@app.route('/admin/approve_user/<username>')
def approve_user(username):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    # Approve the user
    mongo.db.users.update_one({"username": username}, {"$set": {"approved": True}})
    
    # Flash message with translation
    flash(trans['user_approved_successfully'], 'success')
    return redirect(url_for('manage_users', lang=lang))




@app.route('/admin/delete_user/<username>')
def delete_user(username):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    # Delete user from the database
    mongo.db.users.delete_one({"username": username})
    
    flash(trans['user_deleted_successfully'], 'success')
    return redirect(url_for('manage_users', lang=lang))



@app.route('/doctor/view_patient/<patient_username>')
def view_patient_profile(patient_username):
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    patient = mongo.db.users.find_one({"username": patient_username})
    if not patient:
        flash(trans['patient_not_found'], 'danger')
        return redirect(url_for('doctor_dashboard'))

    return render_template('view_patient_profile.html', patient=patient, translations=trans)

from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'  # Folder where you will save images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/doctor/profile', methods=['GET', 'POST'])
def doctor_profile():
    # Redirect to login if not a doctor
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    lang = request.args.get('lang', 'en')
    trans = translations.get(lang, translations['en'])

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        qualification = request.form.get('qualification')
        branch = request.form.get('branch')
        phone_number = request.form.get('phone_number')
        available_time = request.form.get('available_time')
        hospital_name = request.form.get('hospital_name')

        profile_image = None

        # Handling the uploaded image file
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                # Secure and save the file
                filename = secure_filename(file.filename)
                upload_folder = app.config.get('UPLOAD_FOLDER', 'static/uploads')  # Ensure UPLOAD_FOLDER is defined
                file_path = os.path.join(upload_folder, filename)
                
                # Ensure the upload directory exists
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save the file
                file.save(file_path)
                profile_image = f'uploads/{filename}'

        # Retrieve the current doctor profile
        doctor = mongo.db.users.find_one({"username": session['username']})

        # If no new image is uploaded, retain the existing profile image
        if not profile_image:
            profile_image = doctor.get('profile_image')

        # Update the database with profile details
        mongo.db.users.update_one(
            {"username": session['username']},
            {"$set": {
                "name": name,
                "age": age,
                "qualification": qualification,
                "branch": branch,
                "phone_number": phone_number,
                "available_time": available_time,
                "hospital_name": hospital_name,
                "profile_image": profile_image  # Save/retain the image path
            }}
        )

        flash(trans['profile_updated'], 'success')
        return redirect(url_for('doctor_dashboard', lang=lang))

    # Fetch doctor profile data
    doctor = mongo.db.users.find_one({"username": session['username']})
    return render_template('doctor_profile.html', doctor=doctor, translations=trans)



@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'username' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    if request.method == 'POST':
        doctor_username = request.form.get('doctor')
        appointment_date = request.form.get('date')
        appointment_time = request.form.get('time')
        patient_email = request.form.get('patient_email')
        patient_phone = request.form.get('patient_phone')

        # Validate inputs
        if not all([doctor_username, appointment_date, appointment_time, patient_email, patient_phone]):
            flash(trans['all_fields_required'], 'danger')
            return redirect(url_for('book_appointment', lang=lang))

        if '@' not in patient_email or '.' not in patient_email:
            flash(trans['invalid_email'], 'danger')
            return redirect(url_for('book_appointment', lang=lang))

        try:
            # Check if the appointment slot is already booked
            existing_appointment = mongo.db.appointments.find_one({
                "doctor_username": doctor_username,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time
            })

            if existing_appointment:
                flash(trans['slot_booked'], 'danger')
                return redirect(url_for('book_appointment', lang=lang))

            # Generate a random room number
            room_number = random.randint(100, 999)

            # Insert the new appointment into the database
            mongo.db.appointments.insert_one({
                "patient_username": session['username'],
                "doctor_username": doctor_username,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "patient_email": patient_email,
                "patient_phone": patient_phone,
                "room_number": room_number,
                "status": "Pending"  # Default status
            })

            flash(trans['appointment_successful'], 'success')
            return redirect(url_for('patient_dashboard', lang=lang))

        except Exception as e:
            flash(trans['unexpected_error'], 'danger')
            print(f"Error occurred while booking appointment: {e}")
            return redirect(url_for('book_appointment', lang=lang))

    # Fetch available doctors from the database
    doctors = mongo.db.users.find({"role": "doctor"})
    return render_template('book_appointment.html', doctors=doctors, translations=trans)


# MongoDB connection setup
def get_db_connection():
    client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
    db = client['test_db']  # Use the database 'emergency_db'
    return db

# Home page for emergency SOS
@app.route('/emergency_sos')
def emergency_sos_page():
    return render_template('emergency_sos.html')  # Serve the HTML page

# Endpoint to handle sending SOS alerts
@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    user_id = data.get('user_id')  # This would come from the frontend or session

    if not latitude or not longitude or not user_id:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Save the SOS request in the MongoDB database
    db = get_db_connection()
    alerts_collection = db['emergency_alerts']  # Use the 'emergency_alerts' collection
    alert_data = {
        "user_id": user_id,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": datetime.now()
    }
    alerts_collection.insert_one(alert_data)  # Insert SOS alert into MongoDB

    # Fetch nearby donors from the database (example data)
    donors = [
        {"name": "John Doe", "phone": "+123456789", "blood_group": "O+"},
        {"name": "Jane Smith", "phone": "+987654321", "blood_group": "A-"}
    ]

    # Removed SMS sending functionality

    return jsonify({"success": True, "message": "SOS alert recorded successfully!"})

# Doctor Dashboard to view SOS alerts
@app.route('/doctor_dashboard', methods=['GET'], endpoint="doctor_dashboard_page")
def doctor_dashboard():
    # Fetch all emergency alerts from the MongoDB database
    db = get_db_connection()
    alerts_collection = db['emergency_alerts']
    alerts = list(alerts_collection.find())  # Get all alerts from the collection

    # Render doctor dashboard page with alerts
    return render_template('doctor_dashboard.html', alerts=alerts)  # Create this HTML page for doctors

# Admin Dashboard to view SOS alerts
@app.route('/admin_dashboard', methods=['GET'], endpoint="admin_dashboard_page")
def admin_dashboard():
    # Fetch all emergency alerts from the MongoDB database
    db = get_db_connection()
    alerts_collection = db['emergency_alerts']
    alerts = list(alerts_collection.find())  # Get all alerts from the collection

    # Render admin dashboard page with alerts
    return render_template('admin_dashboard.html', alerts=alerts)






# Route for Doctor to Accept Appointment
@app.route('/accept_appointment/<appointment_id>', methods=['GET'])
def accept_appointment(appointment_id):
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    # Fetch the appointment from the database
    appointment = mongo.db.appointments.find_one({"_id": ObjectId(appointment_id)})

    if not appointment or appointment['doctor_username'] != session['username']:
        flash("Appointment not found or you're not authorized to accept it", 'danger')
        return redirect(url_for('doctor_dashboard'))

    # Update appointment status to 'Accepted'
    mongo.db.appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": {"status": "Accepted"}}
    )

    # Send confirmation email to the patient
    send_appointment_confirmation_email(appointment)

    flash("Appointment accepted and confirmation email sent.", 'success')
    return redirect(url_for('doctor_dashboard'))

# Function to Send Appointment Confirmation Email to Patient
def send_appointment_confirmation_email(appointment):
    patient_email = appointment['patient_email']
    doctor_username = appointment['doctor_username']
    appointment_date = appointment['appointment_date']
    appointment_time = appointment['appointment_time']

    subject = f"Appointment Confirmation with Dr. {doctor_username}"
    body = f"""
    Dear Patient,

    Your appointment with Dr. {doctor_username} has been confirmed.
    Appointment Details:
    Date: {appointment_date}
    Time: {appointment_time}

    Please be present at the scheduled time.

    Best regards,
    Your Medical Service
    """

    # Send email using Flask-Mail
    msg = Message(subject, recipients=[patient_email])
    msg.body = body

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route('/view_appointments')
def view_appointments():
    if 'username' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    username = session['username']
    appointments = mongo.db.appointments.find({"patient_username": username})

    return render_template('view_appointments.html', appointments=appointments, translations=trans)

@app.route('/patient/profile', methods=['GET', 'POST'])
def patient_profile():
    if 'username' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        blood_group = request.form['blood_group']
        medical_history = request.form['medical_history']

        # Validate age (must be a positive integer)
        try:
            age = int(age)
            if age <= 0:
                flash(trans['age_error'], 'danger')
                return redirect(url_for('patient_profile', lang=lang))
        except ValueError:
            flash(trans['age_error'], 'danger')
            return redirect(url_for('patient_profile', lang=lang))

        # Validate phone number (must be numeric)
        if not phone_number.isdigit():
            flash(trans['phone_number_error'], 'danger')
            return redirect(url_for('patient_profile', lang=lang))

        # Update the database
        mongo.db.users.update_one(
            {"username": session['username']},
            {"$set": {
                "name": name,
                "age": age,
                "phone_number": phone_number,
                "blood_group": blood_group,
                "medical_history": medical_history
            }}
        )
        flash(trans['profile_update_success'], 'success')
        return redirect(url_for('patient_dashboard', lang=lang))

    patient = mongo.db.users.find_one({"username": session['username']})
    return render_template('patient_profile.html', patient=patient, translations=trans)


@app.route('/patient_dashboard')
def patient_dashboard():
    if 'username' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))

    lang = request.args.get('language', 'en')
    trans = get_translations(lang)
    username = session['username']
    
    # Fetch patient information
    patient = mongo.db.users.find_one({"username": username})
    
    # Fetch appointments for the patient
    appointments = mongo.db.appointments.find({"patient_username": username})
    
    # Fetch notifications for the patient
    notifications = mongo.db.notifications.find({"username": username, "read": False})

    # Convert notifications to a list
    notifications_list = list(notifications)

    return render_template(
        'patient_dashboard.html',
        translations=trans,
        language=lang,
        patient=patient,
        appointments=appointments,
        notifications=notifications_list
    )

@app.route('/admin/view_user/<username>')
def view_user(username):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    # Get the selected language from query parameters or default to 'en'
    lang = request.args.get('lang', 'en')
    
    # Get the translations for the selected language
    trans = translations.get(lang, translations['en'])

    user = mongo.db.users.find_one({"username": username})
    if not user:
        flash(trans['user_not_found'], 'danger')
        return redirect(url_for('manage_users', lang=lang))

    return render_template('view_user.html', user=user, translations=trans)


@app.route('/admin/view_feedback')
def view_feedback():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    feedback_data = load_feedback()
    return render_template('view_feedback.html', feedback=feedback_data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/maps', methods=['GET'])
def maps():
    return render_template('maps.html')




from datetime import datetime

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))

    # Fetch available doctors with additional information from MongoDB
    doctors = list(mongo.db.users.find({"role": "doctor"}, {"username": 1, "name": 1, "branch": 1, "available_time": 1, "_id": 0}))
    
    # Fetch transaction history from MongoDB for the logged-in patient
    transactions = list(mongo.db.payments.find({"patient_email": session.get('username')}, {
        "patient_name": 1, "patient_email": 1, "doctor_name": 1, "utr_number": 1, "paid_amount": 1, "payment_date": 1
    }).sort("payment_date", -1))  # Sort by payment date descending

    # Format the 'payment_date' to 'YYYY-MM-DD' before passing it to the template
    for transaction in transactions:
        if isinstance(transaction['payment_date'], datetime):
            transaction['payment_date'] = transaction['payment_date'].strftime('%Y-%m-%d')  # Format date

    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        patient_email = request.form.get('patientEmail')
        utr_number = request.form.get('utrNumber')
        paid_amount = request.form.get('paidAmount')
        doctor_username = request.form.get('doctorName')
        payment_date = request.form.get('paymentDate')

        # Validate inputs
        if not all([patient_name, patient_email, utr_number, paid_amount, doctor_username, payment_date]):
            flash("All fields are required", 'danger')
            return redirect(url_for('payment'))

        try:
            # Insert payment details into the database
            mongo.db.payments.insert_one({
                "patient_name": patient_name,
                "patient_email": patient_email,
                "doctor_name": doctor_username,
                "utr_number": utr_number,
                "paid_amount": paid_amount,
                "payment_date": payment_date
            })
            flash("Payment successful!", 'success')
            return redirect(url_for('payment'))

        except Exception as e:
            flash("An unexpected error occurred. Please try again.", 'danger')
            print(f"Error: {e}")
            return redirect(url_for('payment'))

    # Render the payment page with doctor list and transaction history
    return render_template('payment.html', doctors=doctors, transactions=transactions)



# @app.route('/doctor_dashboard')
# def doctor_dashboard():
#     if 'username' not in session or session['role'] != 'doctor':
#         return redirect(url_for('login'))

#     lang = request.args.get('language', 'en')
#     trans = get_translations(lang)
#     username = session['username']
#     doctor = mongo.db.users.find_one({"username": username})

#     if doctor is None:
#         return redirect(url_for('login'))

#     # Extract the doctor's name from the doctor object
#     doctor_name = doctor.get('name', 'Doctor')  # Default to 'Doctor' if name is not found

#     return render_template('doctor_dashboard.html', translations=trans, language=lang, doctor_name=doctor_name)


# donation_history = []
# @app.route('/blood_donation', methods=['GET'])
# def blood_donation():
#     """
#     Render the Blood Donation Management page with the updated history.
#     """
#     search_region = request.args.get('region', '').lower()  # Get the search term from the query string
#     if search_region:
#         # Filter the history by region (case-insensitive)
#         filtered_history = [donation for donation in donation_history if search_region in donation['region'].lower()]
#     else:
#         filtered_history = donation_history  # If no search term, show all history
    
#     return render_template('blood_donation.html', history=filtered_history, search_region=search_region)


# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['patient_queue'] 
notifications_collection = db['notifications']  

@app.route('/view_all_notification')
def view_all_notifications():
    lang = request.args.get('lang', 'en')
    notifications = list(notifications_collection.find({}))  # Fetch all notifications
    return render_template('notifications.html', notifications=notifications, translations=get_translations(lang))


if __name__ == '__main__':
    app.run(debug=True)

