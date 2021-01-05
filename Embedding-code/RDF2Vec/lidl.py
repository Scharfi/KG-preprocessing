import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.manifold import TSNE
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import SVC

from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.graphs import KG
from pyrdf2vec.samplers import UniformSampler
from pyrdf2vec.walkers import RandomWalker, Walker


DATASET = {
    "train": ["samples/products.csv", "product"],
}
LABEL_PREDICATES = ["http://dice-researcher.com/grocery-recommendation/recommendation#list"]
OUTPUT = "samples/dataset.owl"
WALKER = [RandomWalker(500, 4, UniformSampler())]

PLOT_SAVE = "embeddings-new.png"
PLOT_TITLE = "pyRDF2Vec"

warnings.filterwarnings("ignore")

def create_embeddings(kg, entities, split, walker=WALKER, sg=1):
    """Creates embeddings for a list of entities according to a knowledge
    graphs and a walking strategy.

    Args:
        kg (graph.KnowledgeGraph): The knowledge graph.
            The graph from which the neighborhoods are extracted for the
            provided instances.
        entities (array-like): The train and test instances to create the
            embedding.
        split (int): Split value for train and test embeddings.
        walker (walkers.Walker): The walking strategy.
            Defaults to RandomWalker(2, float("inf)).
        sg (int): The training algorithm. 1 for skip-gram; otherwise CBOW.
            Defaults to 1.

    Returns:
        array-like: The embeddings of the provided instances.

    """
    embedding = open("embeddingsR2V.csv","a", encoding="utf-8")
    embeddingId = open("embeddingsR2V_ID.csv","a", encoding="utf-8")
    transformer =  transformer = RDF2VecTransformer(sg=sg, walkers=walker)
    walk_embeddings = transformer.fit_transform(kg, entities)
    i=0
    for row in walk_embeddings:
        p = str(entities[i]) +','
        idp = str(i) +','
        embedding.write(p)
        embedding.write(",".join(str(item) for item in row))
        embedding.write("\n")
        embeddingId.write(idp)
        embeddingId.write(",".join(str(item) for item in row))
        embeddingId.write("\n")
        i+=1
    return (
        walk_embeddings[: len(train_entities)],
        walk_embeddings[len(train_entities) :],
    )


#create entities list and generate embeddings
train_data = pd.read_csv("samples/products.csv", sep="\n", header=0)
train_entities = [x for x in train_data['product']]
print(len(train_entities))

entities = train_entities

kg = KG(OUTPUT, label_predicates=LABEL_PREDICATES)

train_embeddings = create_embeddings(
    kg, entities, len(train_entities), WALKER
)

print("Embedding created")

