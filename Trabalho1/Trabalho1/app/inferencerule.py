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