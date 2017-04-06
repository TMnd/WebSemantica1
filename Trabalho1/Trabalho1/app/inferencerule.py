class InferenceRule:
    """
    Implementa a regra base para as inefrencias
    """
    def getqueries(self):
        return None 

    def maketriples(self,binding):
        return self.createTriples(**binding)

#goleadas
class routRule(InferenceRule):
    def getqueries(self):
        gameGols = [('?game', 'FTHG', '?HomeGols'), #golosH
                         ('?game', 'FTAG', '?AwayGols')]       
        return [gameGols]

    def createTriples(self, game, AwayGols, HomeGols):        
        if int(AwayGols)-int(HomeGols)>3 :
            return [(game, "G", "AwayTeam")] #G means that the AwayTeam "Trashed" the home team (Trashed = Goleada)
        elif int(HomeGols)-int(AwayGols)>3:
            return [(game, "G", "HomeTeam")]
        return [(None, None, None)]

class benficaSporting(InferenceRule):
    def getqueries(self):
        q = [('?game', 'HomeTeam', 'Benfica'),('?game', 'AwayTeam', 'Sp Lisbon')]
        return [q]

    def createTriples(self, game):
        return [(game, "Derby", "Benfica"), (game, "Derby", "Sp Lisbon")]

class sportingBenfica(InferenceRule):
    def getqueries(self):
        q = [('?game', 'HomeTeam', 'Sp Lisbon'),('?game', 'AwayTeam', 'Benfica')]
        return [q]

    def createTriples(self, game):
        return [(game, "Derby", "Sp Lisbon"), (game, "Derby", "Benfica")]

class benficaPorto(InferenceRule):
    def getqueries(self):
        q = [('?game', 'HomeTeam', 'Benfica'),('?game', 'AwayTeam', 'Porto')]
        return [q]

    def createTriples(self, game):
        return [(game, "Derby", "Benfica"), (game, "Derby", "Porto")]

class portoBenfica(InferenceRule):
    def getqueries(self):
        q = [('?game', 'HomeTeam', 'Porto'),('?game', 'AwayTeam', 'Benfica')]
        return [q]

    def createTriples(self, game):
        return [(game, "Derby", "Porto"), (game, "Derby", "Benfica")]

class portoSporting(InferenceRule):
    def getqueries(self):
        q = [('?game', 'HomeTeam', 'Porto'),('?game', 'AwayTeam', 'Sp Lisbon')]
        return [q]

    def createTriples(self, game):
        return [(game, "Derby", "Porto"), (game, "Derby", "Sp Lisbon")]

class sportingPorto(InferenceRule):
    def getqueries(self):
        q = [('?game', 'HomeTeam', 'Sp Lisbon'),('?game', 'AwayTeam', 'Porto')]
        return [q]

    def createTriples(self, game):
        return [(game, "Derby", "Sp Lisbon"), (game, "Derby", "Porto")]