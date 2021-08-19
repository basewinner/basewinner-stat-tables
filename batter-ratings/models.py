import peewee

db = peewee.SqliteDatabase('batters.db')

class Team(peewee.Model):
    name = peewee.CharField(max_length=100)
    abbr = peewee.CharField(max_length=10)

    class Meta:
        database = db

    def __str__(self):
        return self.name


class Batter(peewee.Model):
    name = peewee.CharField(max_length=100)
    fangraphs_id = peewee.CharField(max_length=25)
    date = peewee.DateField()
    team = peewee.ForeignKeyField(Team)
    at_bats = peewee.IntegerField()
    plate_appearances = peewee.IntegerField()
    hits = peewee.IntegerField()
    single = peewee.IntegerField()
    doubles = peewee.IntegerField()
    triples = peewee.IntegerField()
    home_runs = peewee.IntegerField()
    runs = peewee.IntegerField()
    runs_batted_in = peewee.IntegerField()
    walks = peewee.IntegerField()
    intentional_walks = peewee.IntegerField()
    strikeouts = peewee.IntegerField()
    hit_by_pitches = peewee.IntegerField()
    sacrifice_flys = peewee.IntegerField()
    sacrifice_hits = peewee.IntegerField()
    grounded_double_play = peewee.IntegerField()
    stolen_bases = peewee.IntegerField()
    caught_stealings = peewee.IntegerField()
    hard_hits = peewee.IntegerField()
    balls = peewee.IntegerField()
    strikes = peewee.IntegerField()
    pitches = peewee.IntegerField()
    swinging_strike_pct = peewee.FloatField()
    swings_and_misses = peewee.IntegerField()
    wins_above_replacement = peewee.FloatField()
    weighted_runs_created = peewee.IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.connect()
    db.create_tables([Team, Batter], safe=True)
