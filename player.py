
class Player(object):
    def __init__(self, name=''):
        self.name = name

        self.hits = 0
        self.ab = 0
        self.r = 0
        self.hr = 0
        self.rbi = 0
        self.sb = 0
        self.ba = 0

        self.bb = 0
        self.so = 0
        self.sf = 0
        self.hbp = 0
        self.e = 0
        self.cs = 0
        self.doubles = 0
        self.triples = 0

        self.pr = 0
        self.pr_r = 0
        self.pr_hr = 0
        self.pr_rbi = 0
        self.pr_sb = 0
        self.pr_ba = 0

        self.position = ''

    def add_basic_hitting_stats(self, hits, ab, r, hr, rbi, sb):
        self.hits += hits
        self.ab += ab
        self.r += r
        self.hr += hr
        self.rbi += rbi
        self.sb += sb
        if self.ab > 0:
            self.ba = self.hits / self.ab

    def print_basic_hitting_stats(self):
        print(self.name.ljust(30), f'{self.hits}/{self.ab}'.ljust(10), f'{self.r}'.ljust(10), f'{self.hr}'.ljust(10),
              f'{self.rbi}'.ljust(10), f'{self.sb}'.ljust(10), '{:.3f}'.format(self.ba))

    def print_player_rater_stats(self):
        print(self.name.ljust(30), '{:.3f}'.format(self.pr_r).ljust(10), '{:.3f}'.format(self.pr_hr).ljust(10),
              '{:.3f}'.format(self.pr_rbi).ljust(10), '{:.3f}'.format(self.pr_sb).ljust(10),
              '{:.3f}'.format(self.pr_ba).ljust(10), '{:.3f}'.format(self.pr))
