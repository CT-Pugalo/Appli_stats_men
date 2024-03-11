import requests, time
import threading as th
from datetime import date
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ResponseThread(th.Thread):

    def __init__(self, page, filtre):
        self.page=page
        self.filtre=filtre
        self.page_size = r'?page_size=50'
        self.project_id= r'&project_id=10,12'
        self.url= r'https://assistance-semsirh.in.phm.education.gouv.fr/sam-public/'
        self.api= r'api/rest/issues'
        self.uri= f'{url}{api}'
        self.headers = {"Authorization": "IFHLjxZMapaYVb7aFyhVA03iq4MyfhYr"}
        self.response = None
        th.Thread.__init__(self)

    def run(self,):
        self.filtre_id= r'&filter_id='
        self.page_nb= r'&page='
        self.response = requests.get(f"{self.uri}{self.page_size}{self.page_nb}{self.page}{self.project_id}{self.filtre_id}{self.filtre}", verify=False, headers=self.headers).json()

headers = {"Authorization": "IFHLjxZMapaYVb7aFyhVA03iq4MyfhYr"}
page_size = r'?page_size=250'
project_id= r'&project_id=10,12'
url= r'https://assistance-semsirh.in.phm.education.gouv.fr/sam-public/'
api= r'api/rest/issues'
uri= f'{url}{api}'

def getResponse(page, filtre):
    global headers
    global uri
    global page_size
    global project_id

    filtre_id= r'&filter_id='
    page_nb= r'&page='

    print(f"getting page: {page}")
    time_start=time.time()
    response = requests.get(f"{uri}{page_size}{page_nb}{page}{project_id}{filtre_id}{filtre}", verify=False, headers=headers)
    time_end=time.time()
    time_diff = time_end - time_start
    print(f'retrived in: {round(time_diff, 2)}s\n', end='\r', flush=True)

    return response

class ResponseThread(th.Thread):

    def __init__(self, page, filtre):
        self.page=page
        self.filtre=filtre
        self.page_size = r'?page_size=250'
        self.project_id= r'&project_id=10,12'
        self.url= r'https://assistance-semsirh.in.phm.education.gouv.fr/sam-public/'
        self.api= r'api/rest/issues'
        self.uri= f'{url}{api}'
        self.headers = {"Authorization": "IFHLjxZMapaYVb7aFyhVA03iq4MyfhYr"}
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
                    notes.append(note)
            issue["notes"]=notes
            issue["status"] = self.responsejson["issues"][i]["status"]["label"]
            created_at = [int(val) for val in self.responsejson["issues"][i]["created_at"][:10].split('-')]
            created_at=date(created_at[0], created_at[1], created_at[2])
            issue["created_at"]=created_at
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

def ThreadPool_reponses(filtre, depth=5):
    threads = []
    responses = []
    page=0
    end=False
    while(not end):
        for i in range(0, depth):
            threads.append(ResponseThread(page+i, filtre))
        for i in threads:
            i.start()
        while(anyThreadAlive(threads)):
            for i in ["|", '/', '-', '\\']:
                print(f"Pagination en cours {i}", end='\r', flush=True)
                time.sleep(0.1)
        print( "                       ", end='\r', flush=True)
        for i in threads:
            i.join()
        for i in threads:
            responses.append(i.response)
            if(len(i.response["issues"]) == 0):
                end=True
        page+=depth
        threads = []
    return responses

def ThreadPool_Index(responses):
    index={}
    threads = []
    max=len(responses)
    for response in responses:
        threads.append(IndexingThread(response))
    for i in range(0, max):
        if(i%5==0):
            for thread in range(i, i+5):
                threads[thread].start()
            while(anyThreadAlive(threads)):
                for t in ["|", '/', '-', '\\']:
                    print(f"Indexation en cours {t}", end='\r', flush=True)
                    time.sleep(0.1)
            print( "                       ", end='\r', flush=True)
            for thread in range(i, i+5):
                threads[thread].join()
            for thread in range(i, i+5):
                index.update(threads[thread].issues)
    return index


def anyThreadAlive(Threads):
    anyAlive=False
    for i in Threads:
        if i.is_alive():
            anyAlive=True
    return anyAlive