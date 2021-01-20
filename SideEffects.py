from Tools.Data import readHset
import numpy as np
def HF(s_path, h_path, new_h_path):
    #Hiding failure
    s_sets,_,_=readHset(s_path)
    h_sets,_,_=readHset(new_h_path)
    i_count=0
    for iset in s_sets:
        if iset in h_sets: i_count+=1
    return i_count/len(s_sets)

def MC(s_path, h_path, new_h_path): 
    s_sets ,_,_=readHset(s_path)
    h_sets,_,_=readHset(h_path)
    new_h_sets,_,_=readHset(new_h_path)
    remove=[]
    n_h_sets=len(h_sets)
    for i in range(n_h_sets):
        iset=h_sets[i]
        if iset in s_sets: 
            remove.append(i)
    h_sets=np.delete(h_sets,remove)
    n_h_sets=len(h_sets)
    count=0
   
    for i in range(len(new_h_sets)):
        if new_h_sets[i] in h_sets:
            count+=1
    return (n_h_sets-count)/n_h_sets

def AC(s_path, h_path, new_h_path): 

    h_sets,_,_=readHset(h_path)
    new_h_sets,_,_=readHset(new_h_path)


 
    n_h_sets=len(h_sets)

    n_new=len(new_h_sets)
    count=0
    for i in range(n_h_sets):
        if h_sets[i] in new_h_sets:
            count+=1
    return (n_new-count)/n_h_sets