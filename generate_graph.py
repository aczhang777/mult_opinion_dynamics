import networkx as nx
import random as rand 

# probably turn this into a function so you can call it in other files

# create a list of nodes in dictionary format: keys are nodes (numbered), values are node attributes (political ideology, bilingual status, willingness to share and consume content in other languages, willingness to translate information before sharing)
G = nx.Graph()
n = 100 # number of nodes in G
p = 0.5 # probability of an edge between any pair (no self loops allowed)

### nodes!
# keys will be 0 through n-1, values dictionaries with 5 key value pairs, for now we'll draw nums randomly from uniform or gauss dist!
node_attributes_dictionary = {}

for i in range(0, n):
    # draw 5 random numbers 
    attributes = {}
    # first number is political ideology on [-1, 1]
    while len(attributes) < 1:
        num = rand.gauss(mu = 0.0, sigma = 0.33)
        if -1 <= num <= 1:
            attributes["Political Ideology"] = num
    
    # second is mother tongue, either 0 (English equivalent) or 1 (Chinese equivalent)
    num = rand.random()
    if num < 0.5:
        attributes["Mother Tongue"] = "English" 
    else:
        attributes["Mother Tongue"] = "Chinese"

    # third: if mother tongue is English, then all the rest are 0. If mother tongue is Chinese, then third is whether or not they are bilingual
    if attributes.get("Mother Tongue") == "English": 
        attributes["Bilingual Status"] = "Not Bilingual"
    else: 
        num = rand.random()
        if num < 0.5:
            attributes["Bilingual Status"] = "Not Bilingual" 
        else:
            attributes["Bilingual Status"] = "Bilingual"

    # fourth: if bilingual is 0, all the rest are 0. Otherwise, fourth is how willing they are to consume/receive content when it's not in their mother tongue
    if attributes.get("Bilingual Status") == "Not Bilingual": # if they are not bilingual
        attributes["Receive Foreign Info"] = 0
    else: # if they are bilingual
        while len(attributes) < 4:
            num = rand.gauss(mu = 0.5, sigma = 0.1667)
            if 0 <= num <= 1:
                attributes["Receive Foreign Info"] = num

    # fifth: if bilingual is 0, then this last one is also 0. Otherwise, fifth is how willing they are to translate and share content that's not in their mother tongue
    if attributes.get("Bilingual Status") == "Not Bilingual":
        attributes["Translate and Share"] = 0
    else:
        while len(attributes) < 5:
            num = rand.gauss(mu = 0.5, sigma = 0.1667)
            if 0 <= num <= 1:
                attributes["Translate and Share"] = num
    
    node_attributes_dictionary[i] = attributes

# add these nodes and node attributes to G
G.add_nodes_from(list(range(n)))
nx.set_node_attributes(G, node_attributes_dictionary, "Node Attributes")

print(G.nodes[0])
print(G.nodes[15])
print(G.nodes[46])

### edges!
edges = [] #fill in this list

for i in range(0, n-1): # yes this is correct, it's not n but n-1
    for j in range(i+1, n):
        num = rand.random()
        if num < p: # add an edge!
            edges.append((i, j))

G.add_edges_from(edges)

# then create the graph! how to visualize graphs?????