"""
Fun��es da triple store
"""
from graphviz import Source  
import csv

class simpleGraph:
    # Indices
    def __init__(self):
        self._spo = {}  # spo é o sujeito, predicado e object
        self._pos = {}  # pos é o predicado, object e sujeito
        self._osp = {}  # osp é o object, sujeito e predicado

    # Inserir Triplos
    def _inserirToIndex(self, index, subject, predicate, object):
        if subject not in index:  # se o sujeito nao se encontra no indice
            index[subject] = {predicate: set([object])}  # na lista do subject que nao esteja no indice cria-se uma lista com id predicado cujo valor é object
        elif predicate not in index[subject]:  # se o sujeito nao se encontra no indice sujeito
            index[subject][predicate] = set([object])
        else:  # se o sujeito e o predicato estiverem na lista
            index[subject][predicate].add(object)

    def add(self, subject, predicate, object):  # para inserir nos indices usando a função inserirToIndex
        self._inserirToIndex(self._spo, subject, predicate, object);
        self._inserirToIndex(self._pos, predicate, object, subject);
        self._inserirToIndex(self._osp, object, subject, predicate);

    # Remover Triplos
    def remove(self, subject, predicate, object):
        triples = list(self.triples(subject, predicate, object))
        for (delsubject, delpredicate, delobject) in triples:
            self._removeFromIndex(self._spo, delsubject, delpredicate, delobject)
            self._removeFromIndex(self._pos, delpredicate, delobject, delsubject)
            self._removeFromIndex(self._osp, delobject, delsubject, delpredicate)

    def _removeFromIndex(self, index, subject, predicate, object):
        try:
            bs = index[subject]  # bs = sera o indice do subjeito (incluindo os predicados e os obejctos)
            cset = bs[predicate]  # cset = sera o objecto relaciodo com o predicado que por sua vez é relacionado pelo sujeito
            cset.remove(object)  # remove o objecto
            if len(cset) == 0:  # Verifica se o existe objectos, se nao existir apagase o predicado
                del bs[predicate]
            if len(bs) == 0:  # Verifica se existe predicados, se nao existir apagase o sujeito
                del index[subject]
        except KeyError:
            pass

    # Pesquisar
    def triples(self, sub, pred, obj):
        try:
            if sub != None:
                if pred != None:
                    # sub pred obj
                    if obj != None:
                        if obj in self._spo[sub][pred]:
                            yield (sub, pred, obj)
                        # sub pred None
                        else:
                            for retObj in self._spo[sub][pred]:
                                yield (sub, pred, retObj)
                else:
                    # sub None obj
                    if obj != None:
                        for retPred in self._osp[obj][sub]:
                            yield (sub, retPred, obj)
                    # sub None None
                    else:
                        for retPred, objSet in self._spo[sub].items():
                            for retObj in objSet:
                                yield (sub, retPred, retObj)
            else:
                if pred != None:
                    # None pred obj
                    if obj != None:
                        for retSub in self._pos[pred][obj]:
                            yield (retSub, pred, obj)
                    # None pred None
                    else:
                        for retObj, subSet in self._pos[pred].items():
                            for retSub in subSet:
                                yield (retSub, pred, retObj)
                else:
                    # None None obj
                    if obj != None:
                        for retSub, predSet in self._osp[obj].items():
                            for retPred in predSet:
                                yield (retSub, retPred, obj)
                    # None None None
                    else:
                        for retSub, predSet in self._spo.items():
                            for retPred, ObjSet in predSet.items():
                                for retObj in ObjSet:
                                    yield (retSub, retPred, retObj)
        except KeyError:
            pass
        
    def listaTriplos(self):
        for sub in self.triples(None, None, None):
            yield (sub)
            #print(sub)

    #def __init__(self):
    #    self._spo = []  # subject � predicate - object
    #    self._pos = []
    #    self._osp = []

    #Adcionar novos triplos na tripleStore
    #def add(self, sub, pred, obj):
    #    self._addToIndex(self._spo, sub, pred, obj)
    #    self._addToIndex(self._pos, pred, obj, sub)
    #    self._addToIndex(self._osp, obj, sub, pred)

    #def _addToIndex(self, index, a, b, c):
    #    if a not in index:
    #        index.append(a)
    #        index.append([b, {c}])
    #    else:
    #        tmp = []
    #        for i in index:
    #            if str(type(i)) == "<class 'list'>":
    #                tmp.append(i[0])
    #                if b in i:
    #                    i[1].add(c)
    #        if b not in tmp:
    #                    index.append([b, {c}])

    # Remover Triplos da tripleStore
    #def remove(self, subject, predicate, object):
    #    triples = list(self.triples(subject, predicate, object))
    #    print("Tamanho do triple: " + str(len(triples)))
    #    for i in range(len(triples)):
    #        print("resultado dos triplos: ")
    #        print(triples[i])
    #    for (delsubject, delpredicate, delobject) in triples:
    #        print ("testeeeee")
    #        self._removeFromIndex(self._spo, delsubject, delpredicate, delobject)
        #    self._removeFromIndex(self._pos, delpredicate, delobject, delsubject)
         #   self._removeFromIndex(self._osp, delobject, delsubject, delpredicate)

    #def _removeFromIndex(self, index, subject, predicate, object):
    #    print("index: " + str(index))
    #    print("subject: " + str(subject))
    #    print("0: " + str(index[0]))
    #    print("00: " + str(index[subject:]))
    #    print("1: " + str(index[1]))
    #    print("1:0 : " + str(index[1][0]))
    #    print("1:1 : " + str(index[1][1]))
        #try:
            #bs = index[subject]  # bs = sera o indice do subjeito (incluindo os predicados e os obejctos)
            #print ("index: " + str(bs))
            #cset = bs[predicate]  # cset = sera o objecto relaciodo com o predicado que por sua vez é relacionado pelo sujeito
            #cset.remove(object)  # remove o objecto
            #if len(cset) == 0:  # Verifica se o existe objectos, se nao existir apagase o predicado
                #del bs[predicate]
            #if len(bs) == 0:  # Verifica se existe predicados, se nao existir apagase o sujeito
                #del index[subject]
        #except KeyError:
            #pass
        
    # Pesquisa de triples
    #def triples(self, sub, pred, obj):
    #    if sub != None:
    #        if pred != None:
    #            if obj != None:
    #                #print(self._spo)
    #                tmp = []
    #                for i in self._spo:
    #                    if str(type(i)) == "<class 'str'>":
    #                        if i == sub:
    #                            tmp.append(i)
    #                    elif str(type(i)) == "<class 'list'>":
    #                        if i[0] == pred:
    #                            tmp.append(i[0])
    #                            for j in i[1]:
    #                                if j == obj:
    #                                    tmp.append(j)
    #                yield tuple(tmp) # FEITO (sub,pred,obj)
    
    #Inserir ficheiros csv para a triplestore
    def load(self, filename):
        aux = 0
        f = open(filename, "r", newline="", encoding="utf-8")
        print("Nome do ficheiro inserido: " + filename)
        reader = csv.reader(f);
        for subject, predicate, object in reader:
            aux = aux + 1
            if aux % 5000 == 0:
                print("Foi inserido " + str(aux) + " triplos")
            self.add(subject, predicate, object)
        print("Total de triplos na triple store: " + str(aux))
        f.close()

    #Salvar ficheiros csv em base dos triplos
    #def save(self, filename):
    #    f = open(filename, "w", newline="", encoding="utf-8")
    #    writer = csv.writer(f)
    #    for subject, predicate, obj in self.triples(None, None, None):
    #        writer.writerow([subject, predicate, obj])
    #    f.close()
    
    #Mostrar a lista de triplos na triple store
    #def listaTriplos(self):
    #    for sub in self.triples(None, None, None):
    #       print(sub)
