

class InferenceRule:
    """
    Implementa a regra base para as inefrencias
    """
    def getqueries(self):
        return None 

    def maketriples(self,binding):        
      
        return self._maketriples(**binding)

#goleadas
class routRule(InferenceRule):
    def getqueries(self):
        jogos_golos = [('?jogo', 'FTHG', '?golosH'),
                         ('?jogo', 'FTAG', '?golosA')]       
        return [jogos_golos]

    def _maketriples(self, jogo, golosA, golosH):        
        if int(golosA)-int(golosH)>2 :
            return [(jogo, "Goleada", "AwayTeam")]
        elif int(golosH)-int(golosA)>2:
            return [(jogo, "Goleada", "HomeTeam")]
        return [(None, None, None)]