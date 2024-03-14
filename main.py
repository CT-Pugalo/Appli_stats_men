from uti import *
import json

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

    tickets_tout_PI     = c.ThreadPool_reponses(diff_tout_PI, 10)
    tickets_PI_courrant = c.ThreadPool_reponses(diff_pi_23, 10)
    data_tout_PI        = c.ThreadPool_Index(tickets_tout_PI)
    data_PI_courrant    = c.ThreadPool_Index(tickets_PI_courrant)

    time_end=c.time.time()
    temps_trait = round(time_end-time_start, 2)
    min=0
    sec=temps_trait
    while(sec>=60):
        min+=1
        sec-=60
    print(f"Temps total: {min},{sec}")
    
    _, stats_pi_courant, _ = ind.num_of_worked_ticket_all(names, no_double=False, issues=data_PI_courrant)
    _, stats_tout_pi, _    = ind.num_of_worked_ticket_all(names, no_double=False, issues=data_tout_PI)
    tickets_par_groupe     = ind.num_of_ticket_by_group(issues=data_PI_courrant)
    nb_tickets_fini        = ind.count_nb_Status("Traite", data_PI_courrant) + ind.count_nb_Status("Clos", data_PI_courrant)
    nb_tickets_enCours     = ind.count_nb_Status("En cours", data_PI_courrant)
    ind.getPI(data_tout_PI, Pi)
    nb_tickets_pi = sort(ind.countPI(data_tout_PI))
 
    tickets_par_jour_Hugo = ind.num_worked_by_day("hbogdano", data_PI_courrant)
    with open('data.json', 'w') as f:
        json.dump(tickets_par_jour_Hugo, f)

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
    
    label_etats = ["Ticket en attente", "ticket traité", "ticket en cours"]
    data_etats  = [
            len(data_PI_courrant)-nb_tickets_fini-nb_tickets_enCours,
            nb_tickets_fini,nb_tickets_enCours,
            ]

    details_ticket_en_attente_label = ["Signale", "A reprendre", "A traiter", "Transmis pour traitement"]
    details_ticket_en_attente_data = [
                ind.count_nb_Status("Signale", data_PI_courrant),
                ind.count_nb_Status("A reprendre", data_PI_courrant),
                ind.count_nb_Status("A traiter", data_PI_courrant),
                ind.count_nb_Status("Transmis pour traitement", data_PI_courrant),
            ]

    f1 = get_pie("Total tickets par groupe de diff\nPI courrant", group, totaux, 1)
    f2 = get_pie("Total tickets par personne (CGI)\nPI courrant", names, tickets_par_personne_pi_courant, 2)
    f3 = get_pie("Total tickets par personne (CGI)\ntout PI", names, tickets_par_personne_tout_pi, 3)
    f4 = get_pie("Repartition des tickets par états", label_etats, data_etats, 4)
    f5 = get_pie("Details sur les tickets 'En attente'", details_ticket_en_attente_label, details_ticket_en_attente_data, 5)
    f6 = plt.figure(6)
    plt.title("Ticket par PI\n(et nombre de ticket passé par le CPE)")
    plt.bar(x, total)
    plt.plot(x,y, 'py--')
    plt.bar(x, y, color="green")

    # plt.show()
