"""
Fun��es da triple store
"""
from graphviz import Source  
import csv

class simpleGraph:
    def __init__(self):
        self._spo = []  # subject – predicate - object
        self._pos = []
        self._osp = []

        self._spx = []
        # self._spo = (subject:[predicate:set([object])])
        # self._spo = (subject,[predicate,{object}])

        # self._pos = (predicate:[object:set([subject])])
        # self._pos = (predicate,[object,{subject}])

        # self._osp = (object:[subject:set([predicate])])
        # self._osp = (object,[subject,{predicate}])

    def add(self, sub, pred, obj):
        self._addToIndex(self._spo, sub, pred, obj)  # SPO SPO
        self._addToIndex(self._pos, pred, obj, sub)  # POS POS
        self._addToIndex(self._osp, obj, sub, pred)  # OSP OSP

        self._addAll(self._spx, sub, pred, obj)
        """ índice com listas (lista de listas) em que cada lista dentro do 
        índice é um triplo"""

    def _addToIndex(self, index, s, p, o):

        if s not in index:
            index.append(s)
            index.append([p, {o}])
        else:
            tmp = []
            for i in index:
                if str(type(i)) == "<class 'list'>":
                    tmp.append(i[0])
                    if p in i:
                        i[1].add(o)
            if p not in tmp:
                        index.append([p, {o}])

    def _addAll(self, index, s, p, o):
        index.append([s, p, o]) # adiciona triplos ao índice

    def remove(self, sub, pred, obj):

        """Remover tríplices com qualquer variação (sub, pred, obj ou None)"""

        for i in reversed(range(len(self._spx))):
            # print("removing", self._spx[i], "at position", i)
            if sub == None and pred == None and obj == None:  # None None None
                del self._spx[i]
            if sub == None and pred == None and obj == self._spx[i][2]:  # None None Obj
                del self._spx[i]
            if sub == self._spx[i][0] and pred == None and obj == None:  # Sub None None
                del self._spx[i]
            if sub == None and pred == self._spx[i][1] and obj == None:  # None Pred None
                del self._spx[i]
            if sub == self._spx[i][0] and pred == self._spx[i][1] and obj == None:  # Sub Pred None
                del self._spx[i]
            if sub == None and pred == self._spx[i][1] and obj == self._spx[i][2]:  # None Pred Obj
                del self._spx[i]
            if sub == self._spx[i][0] and pred == None and obj == self._spx[i][2]:  # Sub None Obj
                del self._spx[i]
            if sub == self._spx[i][0] and pred == self._spx[i][1] and obj == self._spx[i][2]:
                del self._spx[i]

    def triples(self, sub, pred, obj):

        """verificar antes de tudo se sub, pred e obj são None, como estava no código do professor na última condição 
        aquilo fazia sempre yield de todos os tuplos mesmo que a função triples não fosse chamada 
        x.triples(None, None, None)
        
        Para todos os casos nesta função é apenas comparado dentro do índice self._spx, dentro de cada lista, 
        se qualquer variante de sub, pred, obj é igual a i[0], i[1] ou i[2], respetivamente"""

        if sub == None and pred == None and obj == None:
            #print(self._spx)
            for i in self._spx:
                yield tuple(i)  # None None None

        else:

            if sub != None:
                if pred != None:
                    if obj != None:
                        #print(self._spo)
                        tmp = self._spx.copy()
                        # print(tmp)
                        for i in tmp:
                            if i[0] == sub and i[1] == pred and i[2] == obj:
                                yield tuple(i)  # FEITO (Sub Pred Obj)
                    else:
                        # print(self._spo)
                        tmp = self._spx.copy()
                        # print(tmp)
                        for i in tmp:
                            if i[0] == sub and i[1] == pred:
                                yield tuple(i)  # FEITO (Sub Pred None)
                else:
                    if obj != None:
                        # print(self._osp)
                        # for retPred in self._osp[obj][sub]:
                        # yield (sub, retPred, obj)  # sub None obj
                        tmp = self._spx.copy()
                        # print(tmp)
                        for i in tmp:
                            if i[0] == sub and i[2] == obj:
                                yield tuple(i)  # FEITO (Sub None Obj)
                    else:
                        # for retPred, objSet in self._spo[sub].items():
                        # for retObj in objSet:
                        # yield (sub, retPred, retObj)  # sub None None
                        #print(self._osp)
                        tmp = self._spx.copy()
                        # print(tmp)
                        for i in tmp:
                            if i[0] == sub:
                                yield tuple(i)  # FEITO (Sub None None)
            else:
                if pred != None:
                    if obj != None:
                        tmp = self._spx.copy()
                        # print(tmp)
                        for i in tmp:
                            if i[1] == pred and i[2] == obj:
                                yield tuple(i)  # FEITO (None Pred Obj)
                    else:
                        tmp = self._spx.copy()
                        #print(tmp)
                        for i in tmp:
                            if i[1] == pred:
                                yield tuple(i) # FEITO (None Pred None)
                else:
                    tmp = self._spx.copy()
                    #print(tmp)
                    for i in tmp:
                        if i[2] == obj:
                            yield tuple(i) # FEITO (None None obj)
    
    #Listar todos os tiplos em memoria
    def listaTriplos(self):
        for sub in self.triples(None, None, None):
            yield (sub)
            #print(sub)

     #Inserir ficheiros csv para a triplestore
    def load(self, filename):
        aux = 0
        f = open(filename, "r", newline="", encoding="utf-8")
        print("Nome do ficheiro inserido: " + filename)
        reader = csv.reader(f);
        for subject, predicate, object in reader:
            aux = aux + 1
            if aux % 500 == 0:
                print("Foi inserido " + str(aux) + " triplos")
            self.add(subject, predicate, object)
        print("Total de triplos na triple store: " + str(aux))
        f.close()

    # faz um query ao grafo,
    # passando-lhe uma lista de tuplos (triplos restrição)
    # devolve uma lista de dicionarios (var:valor)
    def query(self, clauses):
        bindings = None                      # resultado a devolver
        for clause in clauses:               # para cada triplo
            bpos = {}                        # dicionário que associa a variável à sua posição no triplo de pesquisa
            qc = []                          # lista de elementos a passar ao método triples
            for pos, x in enumerate(clause): # enumera o triplo, para poder ir buscar cada elemento e sua posição
                if x.startswith('?'):        # para as variáveis
                    qc.append(None)          # adiciona o valor None à lista de elementos a pssar ao método triples
#                    bpos[x] = pos            # guarda a posição da variável no triplo (0,1 ou 2)
                    bpos[x[1:]]=pos          # linha de cima re-escrita porque é necessário guardar o nome da variável, mas sem o ponto de interrogação (?)
                else:
                    qc.append(x)             # adiciona o valor dado à lista de elementos a passar ao método triples

            rows = list(self.triples(qc[0], qc[1], qc[2])) # faz a pesquisa com o triplo acabado de construir

            # primeiro triplo pesquisa, todos os resultados servem
            # para cada triplo resultado, cria um dicionario de variaveis (1 a 3 variaveis)
            # em cada dicionario, as variaveis tomam o valor devolvido pelo elemento na mesma posicao da variavel
            if bindings == None:
                bindings = []                # cria a lista a devolver
                for row in rows:             # para cada triplo resultado
                    binding = {}             # cria um dicionario
                    for var, pos in bpos.items(): # para cada variável e sua posição
                        binding[var] = row[pos] # associa à variável o valor do elemento do triplo na sua posição
                    bindings.append(binding) # adiciona o dicionario à lista

            else:                            # triplos pesquisa seguintes, eliminar resultados que não servem
                # In subsequent passes, eliminate bindings that don't work
                # Retira da lista dicionários, aqueles que
                newb = []                    # cria nova lista a devolver
                for binding in bindings:     # para cada dicionario da lista de dicionarios
                    for row in rows:         # para cada triplo resultado
                        validmatch = True    # começa por assumir que o dicionario serve
                        tempbinding = binding.copy() # faz copia temporaria do dicionario
                        for var, pos in bpos.items(): # para cada variavel em sua posição
                            if var in tempbinding: # caso a variavel esteja presente no dicionario
                                if tempbinding[var] != row[pos]: # se o valor da variavel diferente do valor na sua posicao no triplo
                                    validmatch = False # o dicionário não serve
                            else:
                                tempbinding[var] = row[pos] # associa à variável o valor do elemento do triplo na sua posição
                        if validmatch:
                            newb.append(tempbinding) # se dicionario serve, inclui-o na nova lista
                bindings = newb              # sbstituiu lista por nova
        return bindings

    # aplica inferencia ao grafo
    def applyinference(self,rule):
        queries = rule.getqueries()
        bindings=[]
        for query in queries:            
            bindings += self.query(query)
        for b in bindings:
            new_triples = rule.maketriples(b)
            for s, p, o in new_triples:
                if s!=None and p!=None and o!=None:
                    self.add(s, p, o)