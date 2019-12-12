import os
import csv
import networkx as nx
import math
import numpy as np

DATA_DIR = os.path.join('data', 'deputies_words')
DICT_DIR = os.path.join('data', 'common_dict.txt')
CSV_GRAPH_DIR = os.path.join('data', 'bipartite_graph.csv')
GEXF_GRAPH_DIR = os.path.join('data', 'bipartite_graph.gexf')


def load_dict(size=math.inf):
    dictionary = set()
    nb_words = 0
    with open(DICT_DIR, 'r') as f:
        for row in f.readlines():
            nb_words += 1
            if nb_words <= size:
                dictionary.add(row.strip('\n'))
    return dictionary


def graph_build_csv(dictionary):
    file_num = 0
    with open(CSV_GRAPH_DIR, 'w', encoding="utf-8") as graph:
        graph.write("Source,Target,Weight\n")
        for filename in os.listdir(DATA_DIR):
            file_num += 1
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                reader = csv.reader(f)
                for word in reader:
                    if word[0] in dictionary:
                        source = filename.split('.')[0]
                        target = word[0]
                        weight = word[1]
                        graph.write(source + "," + target +
                                    "," + weight + "\n")


def graph_build_gexf(dictionary, nb_dep=None, graph_filename=GEXF_GRAPH_DIR, dep_words=None):
    nb_files = sum([len(files) for r, d, files in os.walk(DATA_DIR)])
    G = nx.Graph()
    added_deputies = set()
    added_words = set()
    file_num = 0
    nb_words = len(dictionary)
    word_num = 0
    if nb_dep is None:
        nb_dep = nb_files
    else:
        nb_files = nb_dep
    if not dep_words:
        dep_words = nb_words
    for filename in os.listdir(DATA_DIR):
        file_num += 1
        if file_num <= nb_dep:
            dep_word_num = 0
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                reader = csv.reader(f)
                for word in reader:
                    dep_word_num += 1
                    if dep_word_num < dep_words:
                        if word[0] in dictionary:
                            source = filename.split('.')[0]
                            target = word[0]
                            weight = word[1]
                            deputy_latitude = 360*file_num/nb_files
                            G.add_node(source, type="deputado",
                                       longitude=0.0, latitude=deputy_latitude)
                            added_deputies.add(source)
                            if not target in added_words:
                                word_num += 1
                                word_latitude = 360*word_num/nb_words
                                G.add_node(target, type="word",
                                           longitude=300.0, latitude=word_latitude)
                                added_words.add(target)
                            G.add_edge(source, target, weight=weight)
    nx.write_gexf(G, graph_filename)
    return G


def generate_adjacency_matrix(G, dictionary):
    # for node in list(G):
    #     if nx.get_node_attributes(G,
    i = 0
    word_map = dict()
    for i in len(dictionary):
        word_map[dictionary[i]] = i
    for i in len(list(G)):

    print(nx.get_node_attributes(G, 'id'))


def main():
    dictionary = load_dict()
    G = graph_build_gexf(dictionary)
    generate_adjacency_matrix(G, dictionary)


if __name__ == '__main__':
    main()
