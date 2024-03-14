from datetime import date

def worked_on(issue, name):
    as_worked = False
    notes = issue['notes']
    for item in notes:
        if "name" in item["reporter"]:
            reporter = item["reporter"]["name"]
            if(reporter == name):
                as_worked = True
    return as_worked

def num_of_worked_ticket(name, issues={}):
    id_worked=[]
    counter=0
    if(len(issues)==0):
        return
    for key, values in issues.items():
        if(worked_on(key, values,name)):
            counter+=1
            id_worked.append(key)
    return id_worked, counter, len(issues)

def num_of_worked_ticket_all(names, no_double=False, issues={}):
    id_worked=[]
    id_doubled=[]
    name_counter= dict.fromkeys(names)
    if(len(issues)==0):
        return
    counter=0
    for name_index in range(0, len(names)):
        name=names[name_index]
        counter=0
        id_worked_on = []
        for key, values in issues.items():
            status = issues[key]["status"]
            group=issues[key]["diff"]
            if(worked_on(values,name)):
                if( no_double==True ):
                    if(not key in id_worked):
                        counter+=1
                        id_worked.append(key)
                        id_worked_on.append((key, status, group))
                    elif(not key in id_doubled):
                        id_doubled.append(key)
                else:
                    counter+=1
                    id_worked_on.append((key, status, group))
                    id_worked.append(key)
        name_counter[name] = [counter, id_worked_on]
    return (id_worked, id_doubled), name_counter, len(issues)

def num_of_ticket_by_group(issues={}):
    num_ticket={
        'Diffusion-GA': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-PCI': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-Paye': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-Remplacement': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-Transverse': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-CPE': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-Mouvement': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        'Diffusion-Budget-Moyen': {
            "Etats": {
            "Signale": 0,
            "Premiere prise en charge": 0,
            "En cours": 0,
            "Connu": 0,
            "Transmis pour traitement": 0,
            "A traiter": 0,
            "A reprendre": 0,
            "A completer": 0,
            },
            "Total": 0},
        }
    if(len(issues)==0):
        return
    for issue_id in issues.keys():
        status = issues[issue_id]["status"]
        groupe=issues[issue_id]["diff"]
        for diff_groupe, value in num_ticket.items():
            if( groupe == diff_groupe):
                num_ticket[diff_groupe]["Total"]+=1
                for label_etat, num_etat in value["Etats"].items():
                    if(status == label_etat):
                        num_ticket[diff_groupe]["Etats"][label_etat] = num_etat+1
    return num_ticket

def getPI(issues ={}, pi={"23": {"debut": [2024, 2, 5],"fin": [2024, 4, 29]}} ):
    if(len(issues) == 0):
        return
    for issue_id, issue in issues.items():
        created_at = issue["created_at"]
        for numero_pi, dates_pi in pi.items():
            deb=date(dates_pi["debut"][0], dates_pi["debut"][1], dates_pi["debut"][2])
            fin=date(dates_pi["fin"][0], dates_pi["fin"][1], dates_pi["fin"][2])
            if(created_at>=deb and created_at<=fin):
                issues[issue_id]["pi"]=numero_pi
def countPI(issues= {}):
    pi_counter = {}
    if(len(issues) == 0):
        return
    for issue_id, issue in issues.items():
        # issue["pi"] => {"23"}
        if(issue["pi"] != None):
            if issue["pi"] in pi_counter:
                pi_counter[issue["pi"]]["Total"] = pi_counter[issue["pi"]]["Total"]+1
            else:
                pi_counter[issue["pi"]] = {"Total": 0}
    for pi in pi_counter.keys():
        pi_counter[pi]["Moyenne/Mois"] = pi_counter[pi]["Total"]/3
    return pi_counter

def countCPE(issues={}):
    if(len(issues) == 0):
        return
    count=0
    for _, issue in issues.items():
        if issue["cpe"]:
            count+=1
    return count

def countCPE_by_PI(issues={}):
    if(len(issues) == 0):
        return
    counter = {}
    for _, issue in issues.items():
        if not issue["pi"] == None:
            if not issue["pi"] in counter:
                counter[issue["pi"]] = 0
            else:
                if issue["cpe"]:
                    counter[issue["pi"]] = counter[issue["pi"]]+1
    return counter

def count_nb_Status(status, issues={}):
    if len(issues)==0 :
        return
    count=0
    for _, issue in issues.items():
        if issue["status"]==status:
            count+=1    
    return count
