# pick 2 or 4 starting nodes
# set a confidence threshold, c
# for these starting nodes: if they are an English (Chinese) speaker, then the language of their piece of content will be in English (Chinese). If they are bilingual, then randomize it (but have it more likely be in their mother tongue, maybe?).
# for each English node, they will share the content with the nodes they are connected to provided that:
# a) political ideology is within c
# b) speak English
# for each native Chinese node, they will share the content provided:
# a) political ideology is within c
# b) if the sharing node is not bilingual, then they will only pick their Chinese speaking neighbors. If the sharing node is bilingual, then:
# if the message is in Chinese, they will share with all their Chinese speaking neighbors. For their English speaking neighbors, they will share it with all their English speaking neighbors with probability "Translate and Share" for that node.
# if the message is in English, they will share with all their English speaking neighbors. For their Chinese speaking neighbors, they will share it with all their Chinese speaking neighbors with probability "Translate and Share" for that node!

import networkx as nx
import random as rand
import generate_graph

# first create the social network and initialize parameters
social_network = generate_graph.generate_graph_from_parameters(8, 8, 5, 0.5, 0.5, 0.5)
social_network_nodes = list(social_network) # just nodes, no node attributes!
social_network_edges = list(social_network.edges())

num_starters = 2 # number of nodes that will start with a message
c = 0.29 # confidence bound
d = 0.5 # for bilingual nodes, this is the probability that the message they start off will be in Chinese
message_zero_ideology = 0.13
message_one_ideology = 0.5
message_two_ideology = 0.58
message_three_ideology = 0.9

message_ideologies = [message_zero_ideology, message_one_ideology, message_two_ideology, message_three_ideology]

# then pick the starting nodes and fill in the 'messages' dictionary: key = which message it is [0, 1, 2, or 3], values = {degree of starting node, ideology of content, language of starting node, bilingual or not}
starters = rand.sample(social_network_nodes, num_starters)
messages = {}
for (node, i) in (starters, range(0, len(starters))): # node cycles through the list "starters", while i cycles through 0, 1, 2, 3 or 0, 1
    message_attrs = {}

    # get the degree of the starting node
    message_attrs["Starting Node Degree"] = social_network.degree[node]

    # get the bilingual status of the starting node
    message_attrs["Starting Node Bilingual Status"] = social_network.nodes[node]["Node Attributes"]["Bilingual Status"]

    # ideology of starting nodes
    message_attrs["Message Ideology"] = message_ideologies[i]
    
    # get the language of the node: if English, then message is in English; if Chinese and not bilingual, then message is in Chinese; if Chinese and bilingual, then flip the weighted coin
    if social_network.nodes[node]["Node Attributes"]["Mother Tongue"] == "English":
        message_attrs["Message Language"] = "English"
    elif social_network.nodes[node]["Node Attributes"]["Mother Tongue"] == "Chinese" and social_network.nodes[node]["Node Attributes"]["Bilingual Status"] == "Not Bilingual":
        message_attrs["Message Language"] = "Chinese"
    elif social_network.nodes[node]["Node Attributes"]["Mother Tongue"] == "Chinese" and social_network.nodes[node]["Node Attributes"]["BIlingual Status"] == "Bilingual":
        num = rand.uniform(a = 0.0, b = 1.0)
        if num <= d:
            message_attrs["Message Language"] = "Chinese"
        else:
            message_attrs["Message Language"] = "English"

    messages[i] = message_attrs

# replace the ideology of each starting node with the ideology of the message
    
# now run the simulation: create a new graph for each message and compute network statistics at each step


#for node in starters:
    # get the node's language status
    #if social_network.nodes[node]["Node Attributes"]["Mother Tongue"] == "English":
        

