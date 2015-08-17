#!/usr/bin/env python3
import re

from bs4 import BeautifulSoup
from itertools import combinations

def parse_players(afile):
    players = []
    data = open(afile).read()
    soup = BeautifulSoup(data, "html.parser")
    for player in soup.find_all("div", attrs={'class': "pli"}):
        name = player.a.text
        team = player.find_all("span")[0].text
        value = int(player.find_all("span")[1].b.text.replace(',', ''))
        pv = None
        for pv_span in player.find_all("span", attrs={'class': "pkt"}):
            try:
                pv = int(pv_span.b.text)
            except:
                continue

        players.append((name, team, value, pv))

    return players

goalies = parse_players('goalie.html')
defence = parse_players('defence.html')
middle = parse_players('middle.html')
offence = parse_players('offence.html')

min_value = 70
goalies = [p for p in goalies if p[3] and p[3] > min_value]
defence = [p for p in defence if p[3] and p[3] > min_value]
middle = [p for p in middle if p[3] and p[3] > min_value]
offence = [p for p in offence if p[3] and p[3] > min_value]

goalies.sort(key=lambda x: x[2])
defence.sort(key=lambda x: x[2])
middle.sort(key=lambda x: x[2])
offence.sort(key=lambda x: x[2])

num_goalies = 1
num_defence = 3
num_middle = 4
num_offence = 3

print((num_goalies, len(goalies)),
      (num_defence, len(defence)),
      (num_middle, len(middle)),
      (num_offence, len(offence)))

budget = 400

def sum_cost(players):
    return sum(p[2] for p in players)

def sum_value(players):
    return sum(p[3] for p in players)

offence_matrix = [0 for i in range(budget + 1)]
for i in range(budget + 1):
    best = (0, ())
    for ps in combinations(offence, num_offence):
        cost = sum_cost(ps)
        value = sum_value(ps)
        if cost > i:
            continue

        rest = i - cost
        current_value = value
        if current_value > best[0]:
            best = (current_value, ps)

    offence_matrix[i] = best

middle_matrix = [0 for i in range(budget + 1)]
for i in range(budget + 1):
    best = (0, ())
    for ps in combinations(middle, num_middle):
        cost = sum_cost(ps)
        value = sum_value(ps)
        if cost > i:
            continue

        rest = i - cost
        current_value = value + offence_matrix[rest][0]
        if current_value > best[0]:
            best = (current_value, ps + offence_matrix[rest][1])

    middle_matrix[i] = best

defence_matrix = [0 for i in range(budget + 1)]
for i in range(budget + 1):
    best = (0, ())
    for ps in combinations(defence, num_defence):
        cost = sum_cost(ps)
        value = sum_value(ps)
        if cost > i:
            continue

        rest = i - cost
        current_value = value + middle_matrix[rest][0]
        if current_value > best[0]:
            best = (current_value, ps + middle_matrix[rest][1])

    defence_matrix[i] = best


goalie_matrix = [0 for i in range(budget + 1)]
for i in range(budget + 1):
    best = (0, ())
    for ps in combinations(goalies, num_goalies):
        cost = sum_cost(ps)
        value = sum_value(ps)
        if cost > i:
            continue

        rest = i - cost
        current_value = value + defence_matrix[rest][0]
        if current_value > best[0]:
            best = (current_value, ps + defence_matrix[rest][1])

    goalie_matrix[i] = best

value, squad = goalie_matrix[budget]
print(value)
print(sum_cost(squad))
print(goalie_matrix[budget])
