import time
from bs4 import BeautifulSoup
from selenium import webdriver


def parse_roster_data(soup):
    table_entries = soup.findAll('tr', class_='Table__TR Table__TR--lg Table__odd')
    categorized_entries = [[] for _ in range(4)]
    ndx = -1
    for entry in table_entries:
        if 'bg-clr-gray-08' not in entry.td['class']:
            continue
        if entry['data-idx'] == '0':
            ndx += 1
        categorized_entries[ndx].append(entry)
    return tuple(zip(categorized_entries[0], categorized_entries[1])), tuple(
        zip(categorized_entries[2], categorized_entries[3]))


def export_hitting_stats(data, file_name):
    out = open(file_name, 'w')
    for hitter in data:
        print(hitter[0].select('div')[0].text, end=',', file=out)
        print(hitter[0].select('div')[1]['title'], end=',', file=out)
        for div in hitter[1].select('div'):
            print(div.text, end=',', file=out)
        print(file=out)


def scrape_daily_team_stats(team_id, period_id, web_driver):
    url = f'https://fantasy.espn.com/baseball/team?leagueId=59180231&teamId={team_id}&scoringPeriodId=' \
          f'{period_id}&statSplit=singleScoringPeriod'
    web_driver.get(url)
    time.sleep(2)
    html = web_driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    hitting, pitching = parse_roster_data(soup)
    export_hitting_stats(hitting, f'./team_stats/team_{team_id}/day_{period_id}')


def scrape_league_data(num_teams, start_pid, end_pid):
    driver = webdriver.Chrome('./chromedriver')
    for team_id in range(1, num_teams + 1):
        for period_id in range(start_pid, end_pid + 1):
            scrape_daily_team_stats(team_id, period_id, driver)
    driver.close()
