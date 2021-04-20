from player import Player


def numeric_stat(stat):
    if stat.isnumeric():
        return int(stat)
    else:
        return 0


def import_team_data(team_id, start_pid, end_pid):
    data = [[] for _ in range(start_pid, end_pid + 1)]
    for day in range(start_pid, end_pid + 1):
        file = open(f'./team_stats/team_{team_id}/day_{day}', 'r')
        file_data = file.readlines()
        file.close()
        for line in file_data:
            data[day - start_pid].append(line.split(','))
    return data


def import_league_data(num_teams, start_pid, end_pid):
    data = []
    for team_id in range(1, num_teams + 1):
        data.append(import_team_data(team_id, start_pid, end_pid))
    return data


def parse_team_data(data):
    parsed_data = []
    for day in range(len(data)):
        parsed_data.append([])
        for player in data[day]:
            player_obj = Player(player[1])
            player_obj.position = player[0]
            hits_and_ab = player[2].split('/')
            player_obj.add_basic_hitting_stats(numeric_stat(hits_and_ab[0]), numeric_stat(hits_and_ab[1]),
                                               numeric_stat(player[3]), numeric_stat(player[4]),
                                               numeric_stat(player[5]), numeric_stat(player[6]))
            parsed_data[day].append(player_obj)
    return parsed_data


def parse_league_data(data):
    parsed_data = []
    for team in data:
        parsed_data.append(parse_team_data(team))
    return parsed_data


def process_team_data(data):
    processed_data = dict()
    for day in data:
        for player in day:
            if player.position not in {'Bench', 'IL'}:
                if player.name not in processed_data.keys():
                    processed_data[player.name] = Player(player.name)
                processed_data[player.name].add_basic_hitting_stats(player.hits, player.ab, player.r,
                                                                    player.hr, player.rbi, player.sb)
    return processed_data


def process_league_data(data):
    processed_data = []
    for team in data:
        processed_data.append(process_team_data(team))
    return processed_data


def display_team_data(data):
    team = list(data.values())
    team.sort(key=lambda x: x.hr, reverse=True)
    total = Player('Total Stats:')
    for player in team:
        total.add_basic_hitting_stats(player.hits, player.ab, player.r, player.hr, player.rbi, player.sb)
        player.print_basic_hitting_stats()
    total.print_basic_hitting_stats()


def display_league_data(data):
    for team in data:
        display_team_data(team)
        print()


if __name__ == "__main__":
    display_league_data(process_league_data(parse_league_data(import_league_data(4, 10, 16))))
