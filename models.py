from random import randint, choices

class Player:
    
    def __init__(self, full_name):
        self.full_name = full_name

    def __str__(self):
        return f'{self.full_name}'


class Team:
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Pair:

    def __init__(self, _id, player_1, player_2, team):
        self.id = _id
        self.player_1 = player_1
        self.player_2 = player_2
        self.team = team
 
    def __str__(self):
        return f'Pair[{self.id}] ({self.player_1} : {self.player_2}) // {self.team} //'


class RandomPairTable:
    
    def __init__(self, players, teams, is_pair):
        self.players = players
        self.teams = teams
        self.is_pair = is_pair
        self._pairs = []
        if self.players:
            self.create()
    
    @property
    def pairs(self):
        return self._pairs

    @pairs.deleter
    def pairs(self):
        self._pairs = []
    
    def add(self, pair):
        if isinstance(pair, Pair):
            self._pairs.append(pair)

    def remove(self, pair):
        if isinstance(pair, Pair):
            self._pairs.remove(pair)

    def create(self):

        if self.is_pair:
            table = RandomPairTable.random_by_pair_with_team(self.players, self.teams)
        else:
            table = RandomPairTable.random_by_player_to_team(self.players, self.teams)
        
        for i, player_1, player_2, team in table:
            self.add(Pair(i, player_1, player_2, team))

    @staticmethod
    def random_by_player_to_team(players, teams):
        seen = set()
        x, z = choices(players) + choices(teams)
        for i in range(1, len(players)+1):
            while x in seen or z in seen:
                x, z = choices(players) + choices(teams)
            seen.add(x)
            seen.add(z)
            yield (i, x, '', z)      

    @staticmethod
    def random_by_pair_with_team(players, teams):
        seen = set()
        item = len(players)//2+1
        teams = teams or list(range(1, item))
        x, y, z = choices(players, k=2) + choices(teams)
        for i in range(1, item):
            while x == y or x in seen or y in seen or z in seen:
                x, y, z = choices(players, k=2) + choices(teams)
            seen.add(x)
            seen.add(y)
            seen.add(z)
            yield (i, x, y, z)      

    def __str__(self):
        return '\n'.join([str(item) for item in self.pairs])
    

if __name__ == "__main__":
    
    players = [
        Player("Armen"),
        Player("Artur"),
        Player("Artyom"),
        Player("Garnik"),
        Player("Hayk M"),
        Player("Hayk G"),
        Player("Hayk A"),
        Player("Hamo"),
        Player("Mher"),
        Player("Narek"),
        Player("Razmik"),
        Player("Vache")
    ]

    teams = [
        Team("1"),
        Team("11"),
        Team("111"),
        Team("1111"),
        Team("11111"),
        Team("111111"),
    ]

    pair = RandomPairTable(players=players, teams=teams)

    print(pair)

    

    
