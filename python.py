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

responses = c.ThreadPool_reponses(diff_tout_PI, 10)
responses_pi = c.ThreadPool_reponses(diff_pi_23, 10)
issues = c.ThreadPool_Index(responses)
issues_pi = c.ThreadPool_Index(responses_pi)

_, stats, _ =ind.num_of_worked_ticket_all(names, no_double=False, issues=issues_pi)
tickets_par_groupe = ind.num_of_ticket_by_group(issues=issues_pi)
ind.getPI(issues, Pi)
tickets_pi = sort(ind.countPI(issues))

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

for label_pi, values in tickets_pi.items():
    pi.append(label_pi)
    total.append(values["Total"])
    moy.append(values["Moyenne/Mois"])

f1 = plt.figure(1)
plt.pie(totaux, labels=group, startangle=90, radius=1.2, autopct=lambda pct: func(pct, tickets), pctdistance=0.8)
plt.legend(loc="lower left")

f2 = plt.figure(2)
plt.pie(tickets, labels=names, startangle=90, radius=1.2, autopct=lambda pct: func(pct, tickets), pctdistance=0.8)
plt.legend(loc="lower left")

f3 = plt.figure(3)
plt.bar(pi, total)

x=[key for key in sort(ind.countCPE_by_PI(issues)).keys()]
y=[value for value in sort(ind.countCPE_by_PI(issues)).values()]
plt.plot(x,y, 'py--')

plt.bar(pi, y, color="green")

plt.show()

#print("en comptant tout")
#for name, total in stats.items():
#    print(f"\t{name}: {total[0]}")
#    for issue in total[1]:
#        print(f"\t\t{issue}")


#for groupe_diff, items in tickets_par_groupe.items():
#    print(f"{groupe_diff}:")
#    total = tickets_par_groupe[groupe_diff]["Total"]
#    for label_etat, value_etat in items["Etats"].items():
#        print(f"\t{label_etat}: {value_etat}")
#    print(f"\tTotal: {total}")