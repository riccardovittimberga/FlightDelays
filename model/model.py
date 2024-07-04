import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allAirports = DAO.getAllAirports()
        self._idMapA = {}
        self._bestPath = []
        self._bestObjFun = 0
        for a in self._allAirports:
            self._idMapA[a.ID] = a

    def buildGraph(self, InNumC):
        self._nodi = DAO.getAllNodes(InNumC, self._idMapA)
        self._grafo.add_nodes_from(self._nodi)
        self._addEdgesV1()

    def _addEdgesV1(self):
        allConnessioni = DAO.getAllEdgesV1(self._idMapA)
        for c in allConnessioni:
            v0 = c.V0
            v1 = c.V1
            peso = c.N
            if v0 in self._grafo and v1 in self._grafo:
                if self._grafo.has_edge(v0, v1):
                    self._grafo[v0][v1]['weight'] += peso
                else:
                    self._grafo.add_edge(v0, v1, weight=peso)

    def getSortedVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple

    def esistePercorso(self,v0,v1):
        connessa=nx.node_connected_component(self._grafo,v0)
        if v1 in connessa:
            return True

    def trovaCamminoDijkstra(self,v0,v1):
        return nx.dijkstra_path(self._grafo,v0,v1)

    def trovaCamminoBFS(self,v0,v1):
        tree=nx.bfs_tree(self._grafo,v0)
        if v1 in tree:
            print(f"{v1} è presente")
        path=[v1]
        while path[-1]!=v0:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse()
        return path
    def trovaCamminoDFS(self,v0,v1):
        tree=nx.dfs_tree(self._grafo,v0)
        if v1 in tree:
            print(f"{v1} è presente")
        path=[v1]
        while path[-1]!=v0:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse()
        return path

    def getCamminoOttimo(self,v0,v1, t):
        self._bestPath=[]
        self._bestObjFun=0
        parziale=[v0]
        self.ricorsione(parziale, v1,t)
        return self._bestPath,self._bestObjFun


    def ricorsione(self, parziale, target,t):
        if self.getObjFun(parziale) > self._bestObjFun and parziale[-1]==target:
            self._bestObjFun=self.getObjFun(parziale)
            self._bestPath = copy.deepcopy(parziale)
            return
        if len(parziale) == t + 1:
            return

        else:
            for n in self._grafo.neighbors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    self.ricorsione(parziale,target,t)
                    parziale.pop()


    def getObjFun(self, listOfNodes):
        objVal=0
        for i in range(0,len(listOfNodes)-1):
            objVal+=self._grafo[i][i+1]["weight"]
        return objVal
    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getAllNodes(self):
        return self._nodi