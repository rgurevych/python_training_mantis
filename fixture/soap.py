from suds.client import Client
from suds import WebFault


class SoapHelper:

    def __init__(self, app):
        self.app = app


    def login_possible(self, username, password):
        client=Client("http://localhost/mantisbt-2.1.0/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False


    def get_projects_list(self, username, password):
        client = Client("http://localhost/mantisbt-2.1.0/api/soap/mantisconnect.php?wsdl")
        try:
            projects=client.service.mc_projects_get_user_accessible(username, password)
            project_names_list = [project["name"] for project in projects]
        except WebFault:
            project_names_list = []
        return project_names_list