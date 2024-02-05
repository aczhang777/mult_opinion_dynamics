import networkx as nx
import random as rand 

# when you do this, remember to implement a check that b <= n2
# also remember to allow for changes in whether we draw from normal or uniform distribution
# also at one point consider allowing for drawing opinions from a 2D space

# WHAT IF WE ALLOW FOR ABCS AND CREATE A THIRD GROUP OF INDIVIDUALS
# could be a good follow up / extension!
# WHAT IF WE ALLOW FOR MULTIPLE LAYERED GRAPHS TO ACCOUNT FOR DIVERSE SOCIAL MEDIA USAGE
# again could be a great follow up / extension!

def generate_graph_from_parameters(n1: int, n2: int, b: int, p1: float, p2: float, p3: float):

    # First we create a list of nodes in dictionary format: keys are nodes (numbered), values are node attributes (political ideology, bilingual status, willingness to share and consume content in other languages, willingness to translate information before sharing)
    G = nx.Graph()
    n1 = n1 # number of English speakers, int
    n2 = n2 # number of Chinese speakers, int
    n = n1 + n2 # number of nodes in G, int
    b = b # number of bilingual Chinese speakers, b < n2, int
    p1 = p1 # probability of an edge between any two English speakers, float
    p2 = p2 # probability of an edge between any two Chinese speakers, float
    p3 = p3 # probability of an edge between any English speaker and any Chinese speaker, float

    # Here we create the node attributes, first for all the English speakers and then the Chinese speaakers

    # keys will be 0 through n-1, values will be dictionaries with 5 key value pairs, for now we'll draw nums randomly from uniform or gauss dist!
    node_attributes_dictionary = {}

    for i in range(0, n1):
        attributes = {} # fill in this dictionary with each English speaker's attributes

        # first is political ideology
        while len(attributes) < 1:
            num = rand.gauss(mu = 0.0, sigma = 0.33)
            if -1 <= num <= 1:
                attributes["Political Ideology"] = num
    
        # second is their mother tongue
        attributes["Mother Tongue"] = "English"

        # third is the fact that they are not bilingual
        attributes["Bilingual Status"] = "Not Bilingual"

        # fourth is the fact that they are not willing to receive foreign info
        attributes["Receive Foreign Info"] = 0

        # fifth is the fact that they are not going to translate and share any information
        attributes["Translate and Share"] = 0

        # now we add this dictionary to our larger dictionary
        node_attributes_dictionary[i] = attributes

    # from the list of Chinese speakers we are going to uniformly at random pick b of them to be bilingual
    chinese_speakers = list(range(n1, n))
    bilinguals = rand.sample(chinese_speakers, b)

    # now we create and add attributes for each Chinese speaker
    for i in range(n1, n):
        attributes = {} # fill in this dictionary with each Chinese speaker's attributes
        # first number is political ideology on [-1, 1]
        while len(attributes) < 1:
            num = rand.gauss(mu = 0.0, sigma = 0.33)
            if -1 <= num <= 1:
                attributes["Political Ideology"] = num
        
        # mother tongue is Chinese
        attributes["Mother Tongue"] = "Chinese"

        # must specify bilingual status for each Chinese speaking node
        if i in bilinguals:
            attributes["Bilingual Status"] = "Bilingual"
        else:
            attributes["Bilingual Status"] = "Not Bilingual"

        # fourth: if not bilingual, then this attribute is 0. Otherwise, fourth is how willing they are to consume/receive content when it's not in their mother tongue
        if attributes.get("Bilingual Status") == "Not Bilingual": # if they are not bilingual
            attributes["Receive Foreign Info"] = 0
        else: # if they are bilingual
            while len(attributes) < 4:
                num = rand.gauss(mu = 0.5, sigma = 0.1667)
                if 0 <= num <= 1:
                    attributes["Receive Foreign Info"] = num

        # fifth: if not bilingual, then this attribute is 0. Otherwise, fifth is how willing they are to translate and share content that's not in their mother tongue
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

    #print(bilinguals)
    #for i in bilinguals:
        #print(G.nodes[i]["Node Attributes"]["Bilingual Status"])
    #print(list(G.nodes(data = True)))
    #for node in list(G.nodes(data = True)):
        #print(node)

    # Here is where we create our list of edges
    edges = [] #fill in this list

    # first we will add in the edges between the English speaking nodes
    for i in range(0, n1-1): # starts at 0 and ends at 4
        for j in range(i+1, n1): # starts at 1 and ends at 5
            num = rand.random()
            if num < p1:
                edges.append((i, j))

    # now we'll add in the edges between the Chinese speaking nodes
    for i in range(n2, n-1): # starts at 6 and ends at 10
        for j in range(i+1, n): # starts at 7 and ends at 11
            num = rand.random()
            if num < p2:
                edges.append((i, j))

    # lastly we add in the edges between English and Chinese speaking nodes
    for i in range(0, n1): # starts at 0 and ends at 5
        for j in range(n2, n): # starts at 6 and ends at 11
            num = rand.random()
            if num < p3:
                edges.append((i, j))

    G.add_edges_from(edges)

    #print(edges)

    return G

# then create the graph! how to visualize graphs?????

social_network = generate_graph_from_parameters(8, 8, 5, 0.2, 0.5, 0.8)
for node in list(social_network.nodes(data = True)):
    print(node)
for edge in list(social_network.edges):
    print(edge)

# source venv/bin/activate