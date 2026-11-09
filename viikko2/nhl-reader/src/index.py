from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console

from player_reader import PlayerReader
from player_stats import PlayerStats

SEASONS = [
    "2018-19", "2019-20", "2020-21", "2021-22",
    "2022-23", "2023-24", "2024-25", "2025-26",
]


def main():
    console = Console()

    season = Prompt.ask("Season", choices=SEASONS, default="2024-25")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    stats = PlayerStats(PlayerReader(url))
    nationalities = stats.nationalities()

    while True:
        nationality = Prompt.ask("Nationality", choices=nationalities)
        players = stats.top_scorers_by_nationality(nationality)

        table = Table(title=f"Season {season} players from {nationality}",
                      title_style="italic")
        table.add_column("name", style="cyan")
        table.add_column("teams", style="magenta")
        table.add_column("goals", justify="right", style="green")
        table.add_column("assists", justify="right", style="green")
        table.add_column("points", justify="right", style="green")

        for player in players:
            table.add_row(player.name, player.team, str(player.goals),
                          str(player.assists), str(player.points))

        console.print(table)


if __name__ == "__main__":
    main()