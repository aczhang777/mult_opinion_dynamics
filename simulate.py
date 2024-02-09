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
# do we allow for overlap - as in, can nodes hear > 1 message? yes! maybe? maybe read paper...

# English speaking nodes can only share English messages with other English speaking nodes (mother tongue + bilingual), and only with bilingual nodes when we pick a rand number less than their "Receive Foreign Info"
# Chinese speaking nodes who are NOT BILINGUAL can only share Chinese messages with other Chinese speaking nodes
# Chinese speaking nodes who are BILINGUAL can share messages with anyone!!!! But again, we must meet probability conditions of both the sharing node and their neighbor!!!
# just make a fucking tree diagram

import networkx as nx
import random as rand
import numpy as np 
import generate_graph

# first create the social network and initialize parameters
social_network = generate_graph.generate_graph_from_parameters(3, 3, 0, 0.5, 0.5, 0.5)
social_network_nodes = list(social_network) # just nodes, no node attributes!
social_network_edges = list(social_network.edges())
print(social_network_edges)
adj_mat = nx.adjacency_matrix(social_network).toarray() # this is of class ndarray, which is from numpy!
print(adj_mat)

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
for node, i in zip(starters, range(0, len(starters))): # node cycles through the list "starters", while i cycles through 0, 1, 2, 3 or 0, 1
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

# maybe some kind of while loop goes here? like every time you pass a message onto a node, you add that node to a list of vectors, as long as that list is nonempty you keep going through this for loop?
# or maybe it should be a while loop that starts after the for loop? either could work (though one might be faster than the other...)
# replace the ideology of each starting node with the ideology of the message
    
# social_network.nodes[node].political_ideology
for node, i in zip(starters, range(0, len(message_ideologies))):
    social_network.nodes[node]["Node Attributes"]["Political Ideology"] = message_ideologies[i]
    node_neighbors = np.nonzero(adj_mat[node])[0] 
    # print("The neighbors of node " + str(node) + " are " + str(node_neighbors))
    neighbors_to_share_with = []
    bil_stat = social_network.nodes[node]["Node Attributes"]["Bilingual Status"]
    prob_share = rand.random() # should this be drawn from the normal distribution instead since "Translate and Share" is drawn from the normal distribution?
    for neighbor in node_neighbors:
        if abs(social_network.nodes[neighbor]["Node Attributes"]["Political Ideology"] - message_ideologies[i]) <= c:
            if bil_stat == "Not Bilingual" and social_network.nodes[node]["Node Attributes"]["Mother Tongue"] == social_network.nodes[neighbor]["Node Attributes"]["Mother Tongue"]: # we gotta add extra if statements to account for their bilingual neighbors!!!!!
                neighbors_to_share_with.append(neighbor)
            elif bil_stat == "Bilingual" and message_ideologies[i]["Message Language"] == "English": # if the sharing node is bilingual and the message is in English
                if social_network.nodes[neighbor]["Node Attributes"]["Mother Tongue"] == "English": # share the message with any of their English speaking neighbors
                    neighbors_to_share_with.append(neighbor)
                elif social_network.nodes[neighbor]["Node Attributes"]["Receive Foreign Info"] > 0: # share the message with their Chinese speaking neighbors, but only if we pick a random number that's less than their willingness to receive foreign content
                    num = rand.random() # what prob dist should this come from?
                    if num <= social_network.nodes[neighbor]["Node Attributes"]["Receive Foreign Info"]:
                        neighbors_to_share_with.append(neighbor)
                elif social_network.nodes[neighbor]["Node Attributes"]["Mother Tongue"] == "Chinese": # lastly, sahre the message with their Chinese neighbors if they're willing to translate it into Chinese for them
                    if prob_share <= social_network.nodes[node]["Node Attributes"]["Translate and Share"]:
                        neighbors_to_share_with.append(neighbor) # so now there's a copy of the message floating around in Chinese????? and we gotta account for this??????
            elif bil_stat == "Bilingual" and message_ideologies[i]["Message Language"] == "Chinese": # repeat this whole. fucking. process!!!!!
                if social_network.nodes[neighbor]["Node Attributes"]["Mother Tongue"] == "Chinese":




# then filter for all the neighbors who speak the appropriate language

# then filter for all the neighbors who are within c
    
# then share the message!

# now run the simulation: create a new graph for each message and compute network statistics at each step


        

