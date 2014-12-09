# -*- coding: utf-8 -*-

"""
This script is to generate topology with link attributes, such as 
link weights, link capacity, etc.

The output is an matrix stored in a csv file, which can be imported to matlab
sample run: python topo_create.py -t 3 -n 10 -w full_10.csv

Author: Xuan Liu
Dec.15, 2013
"""

import networkx as nx
import random
import numpy
import sys
from optparse import OptionParser


def create_topo(topo_info=(0, 4)):
    """
    create a network based on a given topology type and size
    The default network is random topology, labeled as 0, and the default 
    number of nodes are 4. 
    random topology: (0, num_nodes)
    Grid topology: (1, dim_info)
    Ring topology: (2, num_nodes)
    Full Connected: (3, num_nodes)
    RocketFuel Topology: (4, num_nodes)
    The 
    """
    topo_type, topo_config = topo_info
    if topo_type == 0:
        ''' Random Topology '''
        new_topo = random_gen(topo_config)
    elif topo_type == 1:
        ''' 2D Grid Topology'''
        new_topo = grid_gen(topo_config)
    elif topo_type == 2:
        ''' Ring Topology'''
        new_topo = ring_gen(topo_config)
    elif topo_type == 3:
        ''' Fully Connected Topology '''
        new_topo = full_gen(topo_config)
    # add weights to links
    new_topo = add_weights(new_topo, 'equal')    
    return new_topo    
    
def random_gen(topo_config):
    """
    create a random topology
    the topo_config is a tuple: (num_nodes, prob)
    """
    num_nodes, prob = topo_config
    print("Create random topology of {0} with edge generating \
            probability of {1}".format(num_nodes, prob))
    G = nx.gnp_random_graph(num_nodes, prob)
    return G

def grid_gen(topo_config):
    """
    create a 2d-grid topology
    the topo_config is a tuple: (num_row, num_col)
    """
    num_row, num_col = topo_config
    print("Create a 2d-grid topology in dimention of \
            {0} by {1}".format(num_row, num_col))
    G = nx.grid_2d_graph(num_row, num_col)
    mapping = {}
    node_id = 0
    for index_row in range(0, num_row):
        for index_col in range(0, num_col):
            mapping[(index_row, index_col)] = node_id
            node_id += 1
    G_relabel = nx.relabel_nodes(G, mapping)
    return G_relabel

def ring_gen(topo_config):
    """
    create a ring topology
    the topo_config is num_nodes
    """
    num_nodes = topo_config
    print("Create a ring topology of {0} nodes".format(num_nodes))
    G = nx.cycle_graph(num_nodes)
    return G
    
def full_gen(topo_config):
    """
    create a fully connected topology
    the topo_config is num_nodes
    """
    num_nodes = topo_config
    print("Create a fully connected topology of {0} nodes".format(num_nodes))
    G = nx.complete_graph(num_nodes)
    return G

def add_weights(graph, weights='equal'):
    """
    add weight to the graph edges
    """
    edges = graph.edges()
    if weights == 'equal':
        ''' Equal weights on the links '''
        for link in edges:
            nodeA, nodeB = link
            graph.add_edge(nodeA, nodeB, weight=1)
    elif weights == 'random':
        ''' Random assigning weights between 1 and 4 '''
        for link in edges:
            nodeA, nodeB = link
            link_weight = random.choice(range(1,5))
            graph.add_edge(nodeA, nodeB, weight=link_weight)
    return graph

# Topo: Create functions to generate csv file
def topo_csv_gen(csv_filename, graph):
    """
    Create an csv file that presents the connectivity information in n-by-n
    matrix format, where n is the number of nodes in the network. If there
    is no link between node i and j, then the value is set as inf
    
    for example: a four node ring topology can be presented as
    inf 1   inf 1                   1 ----- 2
    1   inf 1   inf                 .       .
    inf 1   inf 1                   .       .
    1   inf 1   inf                 4 ----- 3
    """        
    # link weight information is in dict format
    link_weight = graph.edge
    num_nodes = len(graph.nodes())
    weight_matrix = []
    for index_i in range(0,num_nodes):
        sub_dict = link_weight[index_i]
        sub_matrix = []
        for index_j in range(0,num_nodes):
            if index_j in sub_dict.keys():
                sub_matrix.append(int(sub_dict[index_j]['weight']))
            else:
                sub_matrix.append(float("inf"))
            #print "sub", sub_matrix
        weight_matrix.append(sub_matrix)
        #print "total", weight_matrix
    numpy.savetxt(csv_filename, weight_matrix, delimiter=',')
    return weight_matrix
    
def create_option(parser):
    """
    add the options to the parser:
    takes arguments from commandline
    """
    parser.add_option("-v", action="store_true",
                      dest="verbose",
                      help="Print output to screen")
    parser.add_option("-n", dest="num_nodes",
                      type="int",
                      default=2,
                      help="The number of nodes in the network")
    parser.add_option("-t", dest="net_type",
                      type="int",
                      default=0,
                      help="""network type to be created 
                            0: random 
                            1: grid 
                            2: ring 
                            3: full 
                            4: rocketfuel""")
    parser.add_option("-p", dest="edge_prob",
                      type="float",
                      default=0.5,
                      help="""the probability of create edges from a node
                            when creating a random topology""")
    parser.add_option("--dim_m", dest="grid_dim_m",
                      type="int",
                      default=1,
                      help="2d grid graph of m*n nodes, m")
    parser.add_option("--dim_n", dest="grid_dim_n",
                      type="int",
                      default=2,
                      help="2d grid graph of m*n nodes, n")
    parser.add_option("-w", dest="csv_write",
                      type="str",
                      default="sample.csv",
                      help="write a csv file to store the link weight info")
                      
def run(argv=None):
    """
    Create network topology with weighted links, and write the connectivity 
    information as matrix into a csv file. Five types of topologies can be 
    created: 
    0: random
    1: 2d-grid
    2: ring
    3: full
    4: rocketfuel
    """
    # get arguments from command line
    if not argv:
        argv=sys.argv[1:]
    usage = ("""%prog [-v verbose] 
                    [-n num_nodes] 
                    [-t net_type] 
                    [--dim_m grid_dim_m] 
                    [--dim_n grid_dim_n] 
                    [-w csv_write] """)
    parser = OptionParser(usage=usage)
    create_option(parser)
    (options, _) = parser.parse_args(argv)
    num_nodes = options.num_nodes
    edge_prob = options.edge_prob
    net_type = options.net_type
    grid_dim_m = options.grid_dim_m
    grid_dim_n = options.grid_dim_n
    csv_write = options.csv_write
    
    if net_type == 0:
        topo_info = (net_type, (num_nodes, edge_prob))
        new_topo = create_topo(topo_info)
    elif net_type == 1:
        topo_info = (net_type, (grid_dim_m, grid_dim_n))
        new_topo = create_topo(topo_info)
    elif net_type == 2 or net_type == 3:
        topo_info = (net_type, num_nodes)
        new_topo = create_topo(topo_info)
    
    topo_csv_gen(csv_write, new_topo)

if __name__ == '__main__':
    sys.exit(run())                 