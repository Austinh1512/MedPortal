from utils import protected
from flask import Blueprint
import controllers.auth as auth
import controllers.patients as patients
import controllers.uploads as uploads
import controllers.dashboard as dashboard

#Dashboard
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
@dashboard_bp.route("/stats")
def getDashboardSummary():
   return dashboard.getDashboardSummary()

#Patients
patients_bp = Blueprint("patients", __name__, url_prefix="/patients")
@patients_bp.route("/")
@protected
def getPatients():
    return patients.getPatients()

@patients_bp.route("/<id>")
@protected
def getPatientById(id):
    return patients.getPatientById(id)

@patients_bp.route("/<id>/conditions")
@protected
def getPatientConditions(id):
    return patients.getPatientConditions(id)

@patients_bp.route("/<id>/medications")
@protected
def getPatientMedications(id):
    return patients.getPatientMedications(id)

@patients_bp.route("/<id>/observations")
@protected
def getPatientObservations(id):
    return patients.getPatientObservations(id)

@patients_bp.route("/<id>/encounters")
@protected
def getPatientEncounters(id):
    return patients.getPatientEncounters(id)

#Auth
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
@auth_bp.route("/register", methods=['POST'])
def register():
    return auth.register()

@auth_bp.route("/login", methods=["POST"])
def login():
    return auth.login()

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return auth.logout()

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    return auth.refresh()

#Uploads
upload_bp = Blueprint("upload", __name__, url_prefix="/upload")
@upload_bp.route("/patients", methods=["POST"])
def uploadPatients():
    return uploads.uploadPatients()

@upload_bp.route("/conditions", methods=["POST"])
def uploadConditions():
    return uploads.uploadConditions()

@upload_bp.route("/medications", methods=["POST"])
def uploadMedications():
    return uploads.uploadMedications()

@upload_bp.route("/observations", methods=["POST"])
def uploadObservations():
    return uploads.uploadObservations()

@upload_bp.route("/encounters", methods=["POST"])
def uploadEncounters():
    return uploads.uploadEncounters()
