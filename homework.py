'''
Your government has lost track of a high profile foreign spy, and they have requested your help to track him down. 
As part of his attempts to evade capture, he has employed a simple strategy. Each day the spy moves from the country 
that he is currently in to a neighboring country. The spy cannot skip over a country (for example, he cannot go from 
Chile to Ecuador in one day). The movement probabilities are equally distributed amongst the neighboring countries. 
For example, if the spy is currently in Ecuador, there is a 50% chance he will move to Colombia and a 50% chance 
he will move to Peru. The spy was last seen in Chile and will only move about countries that are in South America. 
He has been moving about the countries for several weeks.
'''


from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import random
import warnings
import matplotlib.cbook
import networkx as nx

# Create the dictionary adj_liist


# Create the dictionary probabilities

probabilities = {'ecuador': {'colombia': 0.5, 'peru': 0.5},
                 'peru': {'ecuador': 0.2, 'colombia': 0.2, 'bolivia': 0.2, 'chile': 0.2, 'brazil': 0.2},
                 'colombia': {'ecuador' : .25, 'peru': .25, 'venezuela': .25, 'brazil': .25},
                 'chile': {'peru' : .33, 'bolivia': .33, 'argentina': .33},
                 'argentina': {'chile': .2, 'bolivia': .2, 'brazil': .2, 'uruguay': .2, 'paraguay': .2},
                 'uruguay': {'argentina': .5, 'brazil': .5},
                 'paraguay': {'argentina': .33, 'brazil': .33, 'bolivia': .33},
                 'bolivia' : {'brazil' : .2, 'paraguay': .2, 'argentina': .2, 'chile': .2, 'peru': .2},
                 'brazil' : {'bolivia' : .1, 'paraguay' : .1, 'argentina' : .1, 'uruguay' : .1, 'peru' : .1, 'colombia' : .1, 'venezuela' : .1, 'french guyana' : .1, 'suriname' : .1, 'guyana' : .1},
                 'venezuela' : {'colombia' : .33, 'brazil' : .33, 'guyana' : .33},
                 'guyana' : {'venezuela' : .33, 'brazil' : .33, 'suriname' : .33},
                 'suriname' : {'guyana' : .33, 'french guyana' : .33, 'brazil' : .33},
                 'french guyana' : {'suriname' : .33, 'brazil' : .33}
                 }


def move_spy(G, start, num_moves):
    current_location = start
    locations = [current_location]

    for _ in range(num_moves):
        potential_locations = list(G[current_location])
        transition_probs = [G[current_location][country]['weight'] for country in potential_locations]
        next_location = random.choices(potential_locations, weights=transition_probs, k=1)[0]
        locations.append(next_location)
        current_location = next_location

    return locations


# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph
for country in probabilities:
    G.add_node(country)

# Add edges with probabilities (weights) to the graph
for country in probabilities:
    for neighbour, prob in probabilities[country].items():
        G.add_edge(country, neighbour, weight=prob)

nx.draw(G, with_labels=True)
plt.show()


# Simulate the spy's movement for 30 days, starting from Chile
spy_movement = move_spy(G, 'chile', 30)

print(spy_movement)

stationary_distribution = nx.pagerank(G, alpha=1, tol=1e-6, weight='weight')
print(stationary_distribution)
