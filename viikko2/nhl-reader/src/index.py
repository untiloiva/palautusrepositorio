import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = [Player(player_dict) for player_dict in response]

    finns = filter(lambda p: p.nationality == "FIN", players)
    finns = sorted(finns, key=lambda p: p.points, reverse=True)

    print("Players from FIN")
    print()

    for player in finns:
        print(player)

if __name__ == "__main__":
    main()