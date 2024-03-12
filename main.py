import commun as c
import func_ind as ind
import matplotlib.pyplot as plt
import numpy as np

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d})"

def normalize_date(date):
        day = date[0]
        month = date[1]
        year = date[2]
        while day>30:
            month+=1
            day-=30
        while month>12:
            year+=1
            month-=12
        return [day, month, year]

def first_pi(tickets_pi):
    first="1000"
    for key in tickets_pi:
        if(int(first) > int(key)):
            first=key
    return first

def sort(tickets_pi):
    sorted_tickets = {}
    first = first_pi(tickets_pi)
    while(len(tickets_pi)>0):
        sorted_tickets[first] = tickets_pi.pop(first)
        first = first_pi(tickets_pi)
    return sorted_tickets

def get_pie(legend, data):
    f1 = plt.figure(1)
    plt.title("Ticket par Groupe de Diffusion")
    plt.pie(data, labels=legend, startangle=90, radius=1.2, autopct=lambda pct: func(pct, data), pctdistance=0.8)
    plt.legend(loc="lower left")
    return f1


if __name__ == "__main__":

    filter=3245
    ticket_diff = 2974
    diff_tout_PI = 3244
    diff_pi_23 = 3254
    tour_controle_PCI = 2918
    Pi= {
        "20": {
            "debut": [2023, 3, 6],
            "fin": [2023, 5, 28]
        },
        "21": {
            "debut": [2023, 6, 12],
            "fin": [2023, 9, 24]
        },
        "22": {
            "debut": [2023, 10, 2],
            "fin": [2024, 1, 14]
        },
        "23": {
            "debut": [2024, 2, 5],
            "fin": [2024, 5, 19]
        }
    }
    names= [
        'kbelabbas', 'hbogdano', 'srichard',
        'rplainard', 'ibiderma','scabanne',
        'jdumarais', 'mvallee', 'ccadoret',
        'arossi', 'abuisset', 'jandrieu',
        'ehaenel', 'scauliez', 'jorozco',
        'gmosnier',
        #'scabanne1', 'rplainar',
            ]

    time_start=c.time.time()

    #responses
    tickets_tout_PI = c.ThreadPool_reponses(diff_tout_PI, 10)

    #responses_pi
    tickets_PI_courrant = c.ThreadPool_reponses(diff_pi_23, 10)

    #issues
    data_tout_PI = c.ThreadPool_Index(tickets_tout_PI)

    #issues_pi
    data_PI_courrant = c.ThreadPool_Index(tickets_PI_courrant)

    _, stats, _ =ind.num_of_worked_ticket_all(names, no_double=False, issues=data_PI_courrant)
    tickets_par_groupe = ind.num_of_ticket_by_group(issues=data_PI_courrant)
    ind.getPI(data_tout_PI, Pi)
    nb_tickets_pi = sort(ind.countPI(data_tout_PI))

    time_end=c.time.time()

    temps_trait= round(time_end-time_start, 2)

    min=0
    sec=temps_trait

    while(sec>=60):
        min+=1
        sec-=60

    print(f"Temps total: {min},{sec}")

    group, totaux = [], []
    names, tickets = [], []
    pi, total, moy = [], [], []

    for name, nb_tickets in stats.items():
        names.append(name)
        tickets.append(nb_tickets[0])

    for label_groupe, val_group in tickets_par_groupe.items():
        group.append(label_groupe)
        totaux.append(tickets_par_groupe[label_groupe]["Total"])

    for label_pi, values in nb_tickets_pi.items():
        pi.append(label_pi)
        total.append(values["Total"])
        moy.append(values["Moyenne/Mois"])

    x=[key for key in sort(ind.countCPE_by_PI(data_tout_PI)).keys()]
    y=[value for value in sort(ind.countCPE_by_PI(data_tout_PI)).values()]

    f1=get_pie(group, totaux)

    f2 = plt.figure(2)
    plt.title("Ticket par Personne (CGI)")
    plt.pie(tickets, labels=names, startangle=90, radius=1.2, autopct=lambda pct: func(pct, tickets), pctdistance=0.8)
    plt.legend(loc="lower left")

    f3 = plt.figure(3)
    plt.title("Ticket par PI\n(et nombre de ticket passé par le CPE)")
    plt.bar(pi, total)
    plt.plot(x,y, 'py--')
    plt.bar(pi, y, color="green")

    plt.show()