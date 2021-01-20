from Tools.Data import readHset
import numpy as np
import _pickle as cPickle
def savHSet(itemsets, utilities, path):
    with open(path, "wt") as f:
        n_itemsets=len(itemsets)
        for i in range(n_itemsets):
       
            itemset=tuple(itemsets[i])
            for item in itemset:
                f.write(str(item))
                if item != itemset[-1]:
                    f.write(':')
                   
            f.write(" %.1f"%utilities[i])
          
            if i!=(n_itemsets-1):
                f.write("\n")
    return 1
def genSI(SIP, ds):
    # print("==============================================")
    # print("Dataset name: ",ds.name)
    
    for MUP in ds.MUPs:
        # print("------------------------------------------")
        # print("Total utility: ", ds.totalUtil)
        # print("Min utility percentage: ",MUP)
        # print("Sensitive percentage: ", SIP)
        h_itemsets, h_utilities, _ = readHset(ds.h_paths[MUP])
        n_h=len(h_itemsets)
        n_s=int(SIP*n_h/100)

        idxs=list(range(n_s))
        np.random.shuffle(idxs)
        
        s_idxs=idxs[:n_s]

        s_itemsets=h_itemsets[s_idxs]
        s_utilities=h_utilities[s_idxs]
        
        savHSet(s_itemsets, s_utilities, ds.s_paths[MUP][SIP])
    
