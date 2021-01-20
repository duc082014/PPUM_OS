
import Sys
from MiningAlgo.HUI_Miner import mining
import pickle as cPickle
with open('./Datasets/datasets.pkl', 'rb') as f:
        datasets=cPickle.load(f)

datasets=[datasets[0]]
for ds in datasets:
    for MUP in ds.MUPs:
        mining(ds.path,ds.uTable,ds.MUTs[MUP],ds.h_paths[MUP])