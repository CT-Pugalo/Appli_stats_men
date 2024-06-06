import requests, time
import threading as th
from datetime import date
from urllib3.exceptions import InsecureRequestWarning
from dotenv import dotenv_values

config = dotenv_values(".env")
token = config["Token"]

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ResponseThread(th.Thread):

    def __init__(self, page, filtre):
        self.page=page
        self.filtre=filtre
        self.page_size = r'?page_size=250'
        self.project_id= r'&project_id=10,12'
        self.url= r'https://assistance-semsirh.in.phm.education.gouv.fr/sam-public/'
        self.api= r'api/rest/issues'
        self.uri= f'{self.url}{self.api}'
        self.headers = {"Authorization": token}
        self.response = None
        th.Thread.__init__(self)

    def run(self,):
        self.filtre_id= r'&filter_id='
        self.page_nb= r'&page='
        self.response = requests.get(f"{self.uri}{self.page_size}{self.page_nb}{self.page}{self.project_id}{self.filtre_id}{self.filtre}", verify=False, headers=self.headers).json()

class IndexingThread(th.Thread):
    def __init__(self, response):
        self.responsejson = response
        self.issues = {}
        th.Thread.__init__(self)
    def run(self):
        length = len(self.responsejson["issues"])
        for i in range( 0, length ):
            id=self.responsejson["issues"][i]["id"]
            issue={}
            notes=[]
            groupe=""
            cpe=False

            if "notes" in self.responsejson["issues"][i] :
                for j in range(0, len(self.responsejson["issues"][i]["notes"])):
                    note={}
                    note["id"]=self.responsejson["issues"][i]["notes"][j]["id"]
                    note["reporter"]=self.responsejson["issues"][i]["notes"][j]["reporter"]
                    note["text"]=self.responsejson["issues"][i]["notes"][j]["text"]
                    note["state"]=self.responsejson["issues"][i]["notes"][j]["view_state"]["label"]
                    note_created_at=[int(val) for val in self.responsejson["issues"][i]["notes"][j]["created_at"][:10].split('-')]
                    note_created_at=date(note_created_at[0], note_created_at[1], note_created_at[2])
                    note["created_at"]=note_created_at
                    notes.append(note)
            issue["notes"]=notes

            issue["status"] = self.responsejson["issues"][i]["status"]["label"]

            created_at = [int(val) for val in self.responsejson["issues"][i]["created_at"][:10].split('-')]
            created_at=date(created_at[0], created_at[1], created_at[2])
            updated_at = [int(val) for val in self.responsejson["issues"][i]["updated_at"][:10].split('-')]
            updated_at=date(updated_at[0], updated_at[1], updated_at[2])
            issue["created_at"]=created_at
            issue["updated_at"]=updated_at

            issue["pi"]=None

            for filed in self.responsejson["issues"][i]["custom_fields"]:
                if filed["field"]["id"] == 31:
                    groupe=filed["value"]
            issue["diff"]=groupe

            for filed in self.responsejson["issues"][i]["custom_fields"]:
                            if filed["field"]["id"] == 47:
                                cpe=filed["value"]
            issue["cpe"] = cpe
            self.issues[id]=issue
