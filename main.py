import os
import func_ind as ind
import commun as c
from uti import *
from datetime import date
import json

if __name__ == "__main__":

    diff_tout_PI = 3485

    Pi= {
        "20": {
            "debut": [2023, 2, 6],
            "fin": [2023, 6, 2]
        },
        "21": {
            "debut": [2023, 6, 5],
            "fin": [2023, 9, 29]
        },
        "22": {
            "debut": [2023, 10, 2],
            "fin": [2024, 2, 2]
        },
        "23": {
            "debut": [2024, 2, 5],
            "fin": [2024, 5, 31]
        },
    }
    names= [
        'kbelabbas', 'hbogdano', 'srichard',
        'rplainard', 'ibiderma','lpierson',
        'jdumarais', 'mvallee', 'ccadoret',
        'arossi', 'abuisset', 'jandrieu',
        'ehaenel', 'scauliez', 'jorozco',
        'gmosnier', 'dly'
        #'scabanne1', 'rplainar', 'scabanne'
            ]
    
    time_start=c.time.time()

    tickets_tout_PI = c.ThreadPool_reponses(diff_tout_PI, 10)
    data_tout_PI    = c.ThreadPool_Index(tickets_tout_PI)
    issues_by_pi    = ind.getPI(data_tout_PI, Pi)

    time_end=c.time.time()
    with open("data.json", "w", encoding="utf-8") as file:
        print(json.dumps(tickets_tout_PI), file = file)
    temps_trait = round(time_end-time_start, 2)
    min=0
    sec=temps_trait
    while(sec>=60):
        min+=1
        sec-=60
    print(f"Temps total: {min},{sec}")
    data_PI_courrant = issues_by_pi["23"]
    _, stats_pi_courant, nb_tickets_pi_courant = ind.num_of_worked_ticket_all(names, no_double=True, issues=data_PI_courrant)
    _, stats_tout_pi, _    = ind.num_of_worked_ticket_all(names, no_double=True, issues=data_tout_PI)
    tickets_par_groupe     = ind.num_of_ticket_by_group(issues=data_PI_courrant)
    nb_tickets_fini        = ind.count_nb_Status("Traite", data_PI_courrant) + ind.count_nb_Status("Clos", data_PI_courrant)
    nb_tickets_enCours     = ind.count_nb_Status("En cours", data_PI_courrant)
    nb_tickets_pi          = sort(ind.countPI(data_tout_PI))
    nb_ticket_pi_CPE       = ind.countCPE_by_PI(data_tout_PI)
    nb_ticket_CPE          = ind.countCPE(data_PI_courrant)

    print(f"{nb_ticket_pi_CPE}\n{nb_ticket_CPE}")
 
    tickets_par_jour_CGI = {}
    for name in names:
        tickets_par_jour_CGI.update(ind.num_worked_by_day(name, data_PI_courrant))

    group  = [keys for keys in tickets_par_groupe.keys()]
    totaux = []
    tickets_par_personne_pi_courant, tickets_par_personne_tout_pi = [], []
    pi, total, moy = [], [], []
    
    for _, nb_tickets in stats_pi_courant.items():
        tickets_par_personne_pi_courant.append(nb_tickets[0])

    for _, nb_tickets in stats_tout_pi.items():
        tickets_par_personne_tout_pi.append(nb_tickets[0])

    for label_groupe, val_group in tickets_par_groupe.items():
        totaux.append(tickets_par_groupe[label_groupe]["Total"])

    for label_pi, values in nb_tickets_pi.items():
        total.append(values["Total"])
        moy.append(values["Moyenne/Mois"])

    x=[key for key in sort(ind.countCPE_by_PI(data_tout_PI)).keys()]
    y=[value for value in sort(ind.countCPE_by_PI(data_tout_PI)).values()]
    
    label_etats = ["Signale", "A reprendre", "A traiter", "Transmis pour traitement", "Traite", "Clos", "En cours"]
    data_etats  = [
                ind.count_nb_Status("Signale", data_PI_courrant),
                ind.count_nb_Status("A reprendre", data_PI_courrant),
                ind.count_nb_Status("A traiter", data_PI_courrant),
                ind.count_nb_Status("Transmis pour traitement", data_PI_courrant),
                ind.count_nb_Status("Traite", data_PI_courrant), 
                ind.count_nb_Status("Clos", data_PI_courrant),
                ind.count_nb_Status("En cours", data_PI_courrant),
            ]

    details_ticket_colour = [
                "red",
                "purple",
                "pink",
                "orange",
                "grey",
                "black",
                "blue",
            ]
    details_ticket_en_attente_label = ["Signale", "A reprendre", "A traiter", "Transmis pour traitement"]
    details_ticket_en_attente_data = [
                ind.count_nb_Status("Signale", data_PI_courrant),
                ind.count_nb_Status("A reprendre", data_PI_courrant),
                ind.count_nb_Status("A traiter", data_PI_courrant),
                ind.count_nb_Status("Transmis pour traitement", data_PI_courrant),
            ]
    details_ticket_en_attente_colour = [
                "red",
                "purple",
                "pink",
                "orange",
            ]

    day = date.today();
    try:
        os.mkdir(f"./images/{day}")
    except FileExistsError as e:
        pass

    f1 = get_pie("Total tickets par groupe de diff\nPI courrant", group, totaux, 1)
    plt.savefig(f"images/{day}/ticketsParGroupePICourant.png")
    plt.close()

    f2 = get_pie("Total tickets par personne (CGI)\nPI courrant", names, tickets_par_personne_pi_courant, 2)
    plt.savefig(f"images/{day}/ticketsParPersonnePICourran.png")
    plt.close()

    f3 = get_pie("Total tickets par personne (CGI)\ntout PI", names, tickets_par_personne_tout_pi, 3, display_legend=False)
    plt.savefig(f"images/{day}/ticketsParPersonneToutPI.png")
    plt.close()

    f4 = get_pie("Repartition des tickets par états\nPI courrant", label_etats, data_etats, 4, color=details_ticket_colour)
    plt.savefig(f"images/{day}/ticketParEtatsPICourrant.png")
    plt.close()

    f5 = get_pie("Details sur les tickets 'En attente'\nPI courrant", details_ticket_en_attente_label, details_ticket_en_attente_data, 5, color=details_ticket_en_attente_colour)
    plt.savefig(f"images/{day}/detailsTicketsEnAttente.png")
    plt.close()

    f6 = plt.figure(6)
    plt.title("Ticket par PI\n(et nombre de ticket passé par le CPE)")
    plt.bar(x, total)
    plt.plot(x,y, 'py--')
    plt.bar(x, y, color="green")
    plt.savefig(f"images/{day}/ticketsParPI_EvolutionTicketsCPE.png")
    plt.close()

    with open(f'./images/{day}/data.json', "w+") as f:
        json.dump(tickets_par_jour_CGI, f)
