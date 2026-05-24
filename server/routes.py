from utils import protected
from flask import Blueprint
import controllers.auth as auth
import controllers.patients as patients

#Dashboard
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
@dashboard_bp.route("/stats")
def getDashboardSummary():
   return "Dashboard stats"

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
def getPatientMedications(id):
    return f"Patient <{id}> medications"

@patients_bp.route("/<id>/observations")
def getPatientObservations(id):
    return f"Patient <{id}> observations"

@patients_bp.route("/<id>/encounters")
def getPatientEncounters(id):
    return f"Patient <{id}> encounters"

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