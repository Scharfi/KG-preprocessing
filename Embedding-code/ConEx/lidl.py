from collections import defaultdict
import numpy as np
import torch
from models import ConEx
from helper_classes import Data

kg_path = 'KGs/Lidl'
data_dir = "%s/" % kg_path

model_path = 'conex.pt'
d = Data(data_dir=data_dir, reverse=False)


class Reproduce:

    def __init__(self):
        self.cuda = False

        self.batch_size = 256

    def get_data_idxs(self, data):
        data_idxs = [(self.entity_idxs[data[i][0]], self.relation_idxs[data[i][1]], self.entity_idxs[data[i][2]]) for i
                     in range(len(data))]
        return data_idxs

    def get_er_vocab(self, data):
        er_vocab = defaultdict(list)
        for triple in data:
            er_vocab[(triple[0], triple[1])].append(triple[2])
        return er_vocab

    def get_batch(self, er_vocab, er_vocab_pairs, idx):
        batch = er_vocab_pairs[idx:idx + self.batch_size]
        targets = np.zeros((len(batch), len(d.entities)))
        for idx, pair in enumerate(batch):
            targets[idx, er_vocab[pair]] = 1.
        targets = torch.FloatTensor(targets)
        if self.cuda:
            targets = targets.cuda()
        return np.array(batch), targets

    
    def reproduce(self):

        self.entity_idxs = {d.entities[i]: i for i in range(len(d.entities))}
        self.relation_idxs = {d.relations[i]: i for i in range(len(d.relations))}
        
        params = {'num_entities': len(self.entity_idxs),
                  'num_relations': len(self.relation_idxs),
                  'embedding_dim': 20,
                  'input_dropout': 0.1,
                  'hidden_dropout': 0.1,
                  'projection_size': 1088,
                  'conv_out': 64,
                  'feature_map_dropout': 0.1}

        model = ConEx(params)

        model.load_state_dict(torch.load(model_path))
        embedding = open("embeddings.csv","a", encoding="utf-8")
        liste = d.entities
        
        for i in range(len(liste)):
            prod = liste[i]+','
            embedding.write(prod)
            x = model.emb_e_real.weight[i].data
            embedding.write(",".join(str(item)[7:13] for item in x))
            embedding.write(",")
            w = model.emb_e_img.weight[i].data
            embedding.write(",".join(str(item)[7:13] for item in w))
            embedding.write("\n")
        
Reproduce().reproduce()
