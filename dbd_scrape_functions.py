import time
from bs4 import BeautifulSoup
from selenium import webdriver
from player import Player
from datetime import timedelta, date


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def parse_stat(name, stat):
    stat = stat.replace(name, '')
    if len(stat) == 0:
        return 1
    else:
        return int(stat)


def parse_player_data(player):
    player_name = player[3:24]
    player_name = player_name.split(', ')
    player_name = player_name[1].strip() + ' ' + player_name[0]

    player_stats = player[45:]
    if ')' in player_stats:
        player_stats = player_stats.split(')')[1][2:]
    player_stats = player_stats.split()
    player_obj = Player(player_name)
    for stat in player_stats:
        if '/' in stat:
            stat = stat.split('/')
            player_obj.hits = int(stat[0])
            player_obj.ab = int(stat[1])
        elif 'HR' in stat:
            player_obj.hr = parse_stat('HR', stat)
        elif 'RBI' in stat:
            player_obj.rbi = parse_stat('RBI', stat)
        elif 'R' in stat:
            player_obj.r = parse_stat('R', stat)
        elif 'SB' in stat:
            player_obj.sb = parse_stat('SB', stat)
        elif 'BB' in stat:
            player_obj.bb = parse_stat('BB', stat)
        elif 'SO' in stat:
            player_obj.so = parse_stat('SO', stat)
        elif 'HBP' in stat:
            player_obj.hbp = parse_stat('HBP', stat)
        elif 'SF' in stat:
            player_obj.sf = parse_stat('SF', stat)
        elif 'CS' in stat:
            player_obj.cs = parse_stat('CS', stat)
        elif 'E' in stat:
            player_obj.e = parse_stat('E', stat)
        elif '2B' in stat:
            player_obj.doubles = parse_stat('2B', stat.replace('-', ''))
        elif '3B' in stat:
            player_obj.triples = parse_stat('3B', stat.replace('-', ''))

    return player_obj


def parse_data(soup):
    player_data = soup.findAll('pre')[0].text.split('\n')[1:]
    parsed_data = []
    for player in player_data:
        if len(player) == 0:
            break
        parsed_data.append(parse_player_data(player))
    return parsed_data


def export_data(data, file_name):
    out = open(file_name, 'w')
    for player in data:
        print(f'{player.name},{player.hits},{player.ab},{player.r},{player.hr},{player.rbi},{player.sb},'
              f'{player.bb},{player.so},{player.hbp},{player.sf},{player.cs},{player.e},{player.doubles},'
              f'{player.triples}', file=out)
    out.close()


def scrape_daily_stats(date, web_driver):
    url = f'http://dailybaseballdata.com/cgi-bin/getstats.pl?date={date.month}' + '{:02d}'.format(date.day)
    web_driver.get(url)
    time.sleep(2)
    html = web_driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    export_data(parse_data(soup), f'./mlb_stats/{date.month}_{date.day}')


def scrape_data(start_date, end_date):
    web_driver = webdriver.Chrome('./chromedriver.exe')
    for date in date_range(start_date, end_date + timedelta(days=1)):
        scrape_daily_stats(date, web_driver)
    web_driver.close()


if __name__ == "__main__":
    scrape_data(date(2021, 4, 17), date(2021, 4, 17))
