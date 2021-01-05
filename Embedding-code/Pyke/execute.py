from helper_classes import PYKE
from helper_classes import Parser
from helper_classes import DataAnalyser
from helper_classes import PPMI

import util as ut
import numpy as np
import random

random_state = 1
np.random.seed(random_state)
random.seed(random_state)

# DEFINE MODEL PARAMS
K = 100
num_of_dims = 50
bound_on_iter = 100
omega = 0.45557
e_release = 0.0414

kg_root = 'KGs/data'
kg_path = kg_root + '/dataset.nt'
# For N-Quads, please set ut.triple=4. By default ut.triple=3 as KG is N3.
ut.triple = 3


storage_path, experiment_folder = ut.create_experiment_folder()

print(storage_path)
parser = Parser(p_folder=storage_path, k=K)

parser.set_similarity_measure(PPMI)

model = PYKE()

analyser = DataAnalyser(p_folder=storage_path)

holder = parser.pipeline_of_preprocessing(kg_path)

vocab_size = len(holder)

embeddings = ut.randomly_initialize_embedding_space(vocab_size, num_of_dims)

learned_embeddings = model.pipeline_of_learning_embeddings(e=embeddings,
                                                           max_iteration=bound_on_iter,
                                                           energy_release_at_epoch=e_release,
                                                           holder=holder, omega=omega)

del holder
del embeddings

vocab = ut.deserializer(path=storage_path, serialized_name='vocabulary')

learned_embeddings.index=[ i.replace('https://lidl.de/de/','')for i in vocab]
learned_embeddings.to_csv(storage_path + '/embeddings.csv') 

#analyser.perform_clustering_quality(learned_embeddings)
#analyser.perform_type_prediction(learned_embeddings)

#analyser.plot2D(learned_embeddings)

#type_info = ut.deserializer(path=storage_path, serialized_name='type_info')
#len(type_info) # denoted as \mathcal{S} in the paper 

# get the index of objects / get type information =>>> s #type o
#all_types = sorted(set(*list(type_info.values())))
#len(all_types)# denoted as C in the paper