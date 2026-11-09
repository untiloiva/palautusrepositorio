class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players = filter(lambda p: p.nationality == nationality, self.players)
        return sorted(players, key=lambda p: p.points, reverse=True)
