from player import Player
from dbd_scrape_functions import date_range
from datetime import timedelta, date
from espn_fantasy_data_functions import process_team_data, display_team_data


def import_mlb_data(start_date, end_date):
    data = []
    for date in date_range(start_date, end_date + timedelta(days=1)):
        file_name = f'{date.month}_' + '{:02d}'.format(date.day)
        file = open(f'./mlb_stats/{file_name}', 'r')
        file_data = file.readlines()
        file.close()
        data.append([])
        for line in file_data:
            data[int((date - start_date).days)].append(line.strip().split(','))
    return data


def parse_mlb_data(data):
    parsed_data = []
    for day in range(len(data)):
        parsed_data.append([])
        for player in data[day]:
            player_obj = Player(player[0])
            player_obj.add_basic_hitting_stats(int(player[1]), int(player[2]),
                                               int(player[3]), int(player[4]),
                                               int(player[5]), int(player[6]))
            parsed_data[day].append(player_obj)
    return parsed_data


def process_mlb_data(data):
    return process_team_data(data)


def display_mlb_data(data):
    display_team_data(data)


if __name__ == '__main__':
    display_mlb_data(process_mlb_data(parse_mlb_data(import_mlb_data(date(2021, 4, 1), date(2021, 4, 18)))))