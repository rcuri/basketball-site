import requests
from bs4 import BeautifulSoup

base_url = 'https://www.basketball-reference.com/teams/'
year = 2018

team_list = [
    'ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN',
    'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
    'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX',
    'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]

for team in team_list:
    url = base_url + team + "/" + str(year) + ".html"
    bball_r = requests.get(url)
    bball_soup = BeautifulSoup(bball_r.text, 'html.parser')
    names = bball_soup.findAll(lambda tag: tag.name == 'a' and tag.findParent('td', 'left'))
    names = names[::2]
    position = bball_soup.findAll('td', 'center')
    height = bball_soup.findAll('td', attrs={'data-stat':'height'})
    weight = bball_soup.findAll('td', attrs={'data-stat':'weight'})
    born_on = bball_soup.findAll('td', attrs={'data-stat':'birth_date'})
    current_team = Team(team_name=team, season=year-1)
    current_team.save()
    for (player, pos, ht, wt, bday) in zip(names, position, height, weight, born_on):
        new_player = Player(
            team=current_team,
            player_name=player.getText(),
            position=pos.getText(),
            height=ht.getText(),
            weight=wt.getText(),
            birth_date=bday.getText()
            ).save()
