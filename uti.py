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
    while(len(tickets_pi)>0):
        first = first_pi(tickets_pi)
        sorted_tickets[first] = tickets_pi.pop(first)
    return sorted_tickets

def get_pie(titre, legend, data, figure=1):
    f1 = plt.figure(figure)
    plt.title(titre)
    plt.pie(data, labels=legend, startangle=90, radius=1.2, autopct=lambda pct: func(pct, data), pctdistance=0.8)
    plt.legend(loc="lower left")
    return f1


