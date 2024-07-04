import networkx as nx

def creaGrafo():
    myGraph=nx.Graph()
    myGraph.add_node(1) #1 è il nome del nodo, quindi se scrivessi a avrei il nodo a

    mynodes=[1,2,3,4,5,6,7,8,9,10]
    myGraph.add_nodes_from(mynodes) #aggiunge in ordine e se un nodo c'è già non lo riaggiunge

    edgeList=[(1,2),(1,3),(3,4),(2,5),(5,6)]

    myGraph.add_edges_from(edgeList)
    myGraph.add_edge(1,2,weight=4) #come se il grafo fosse un dizionario con chiave il nodo e valore gli archi


    myDiGraph=nx.DiGraph()
    myDiGraph.add_nodes_from(mynodes)
    myDiGraph.add_edges_from(edgeList)
    #myDiGraph.in_edges stampa gli archi entranti mentre out_edges quelli uscenti

    multiGraph=nx.MultiGraph()
    multiGraph.add_nodes_from(mynodes)
    multiGraph.add_edges_from(edgeList)
    multiGraph.add_edge(1,2,attr="foo") #negli altri casi non aggiungeva archi uguali mentre nel multi lo fa

if __name__=='__main__':
    creaGrafo()