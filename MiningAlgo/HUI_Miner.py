from Tools.Data import readData, u, uis
import numpy as np 
from collections import defaultdict

  
def gen_K_itemset(a, b):
    #Generate new itemset by 2 k-1 itemsets: a and b 
    ret=list(a)
    ret.append(b[-1])
    return tuple(ret)

def intersectTrans(t1, t2):
    '''Find the intersection of two transactions t1 and t2'''
    t1=set(t1)
    t2=set(t2)
    t12=t1.intersection(t2)
    if len(t12) > 0: return t12
    return None
### Only for debugging
def showUl(utilityList):
    for item, value in utilityList.items():
        print(item, ': ', value)

def initUtilityList(utilityList, item):
    '''Init utility list
    ------------------------
    itemset: represented by tuple
    iutils: itemset iutils in transactions
    rutils: itemset rutils in transaction 
    tidset: a python set of tids of transactions support itemset'''
    utilityList[item]={}
    utilityList[item]['itemset']=tuple([item])
    utilityList[item]['iutils']={}
    utilityList[item]['rutils']={}
    utilityList[item]['t_iutils']=0  #total iutil
    utilityList[item]['t_rutils']=0  #total rutil
    utilityList[item]['tidset']=set()
    utilityList[item]['prune']=False
    return utilityList

def prune(utilityList, tree, h_sets, minUtil):
    '''
    Prune search space and store high utility itemsets
    Parameters
    ----------------------------------
    h_sets: high-utility itemsets
    minUtil: minimum utility threshold
    '''

    for item in tree.keys():
        t_iutils= utilityList[item]['t_iutils']
        t_rutils= utilityList[item]['t_rutils']
 
        if t_iutils > (minUtil -1):
            h_sets[utilityList[item]['itemset']]=t_iutils
        if t_iutils + t_rutils < minUtil:
            # remove.append(item)
            utilityList[item]['prune']=True
    return 1

def construct_1_utilityList(data_path, table_path):
    '''Paramters
    ------------------------
    '''
    data, uTable, _=readData(data_path, table_path)
    twu = defaultdict(lambda: 0) #transaction weighted utility 

    TU={} #transaction utility 

    tw={} #utility of item in transaction
    for tid in data.keys():
        t_utils=0 
        tw[tid]={}
        for item in data[tid].keys():
            util = u(item, tid, data, uTable)
            tw[tid][item]=util
            t_utils+= util
            twu[item]+=util
        TU[tid]=t_utils
    
    tree={} #search spaces
    utilityList={}
    #init search space
    for key, _ in sorted(twu.items(), key= lambda item: item[1], reverse=False):
        tree[key]={}
        initUtilityList(utilityList, key)

    
    #construct 1-utility-list
    for tid in data.keys():
        t_utils=0
        for item in sorted(data[tid].keys(), key = lambda item: twu[item], reverse=False):
                   
            iutils = tw[tid][item]
            t_utils+=iutils

            rutils= TU[tid] - t_utils

            utilityList[item]['iutils'][tid]=iutils
            utilityList[item]['rutils'][tid]=rutils
            utilityList[item]['t_iutils']+=iutils
            utilityList[item]['t_rutils']+=rutils
            utilityList[item]['tidset'].add(tid)
    return utilityList, tree, TU

def construct_K_utilityList(utilityList, tree, minUtil, TU, h_sets, k):
    '''Contruct k-utilityList from k-1 - utilityList'''
    
    items=list(tree.keys())
    n=len(items)
    prune(utilityList,tree,h_sets,minUtil)
    if n==0: return
    
    for i in range(n-1):
        a=items[i] 
        if utilityList[a]['prune']: continue
        for j in range(i+1,n):
            
            b=items[j] 
            t_a=utilityList[a]['tidset']
            t_b=utilityList[b]['tidset']
                    
            trans=intersectTrans(t_a, t_b) # transactions that support both a and b
           
            if trans is None: continue
            utilityList[a][b] = {}
            tree[a][b]={}
            
            new_itemset= gen_K_itemset(utilityList[a]['itemset'], utilityList[b]['itemset'])
            utilityList[a][b]['itemset']= new_itemset
            utilityList[a][b]['iutils']={}
            utilityList[a][b]['rutils']={}
            utilityList[a][b]['tidset']=trans
            t_iutils=0
            t_rutils=0
            for t in trans:
                iutils=utilityList[a]['iutils'][t] + utilityList[b]['iutils'][t]
                
                if k>2: iutils-= utilityList['iutils'][t]
                
                

                rutils = utilityList[b]['rutils'][t] #rutils definitely is the rutils of itemset b
    
                utilityList[a][b]['iutils'][t]= iutils
                utilityList[a][b]['rutils'][t]= rutils
                t_iutils+=iutils
                t_rutils+=rutils
            utilityList[a][b]['t_iutils']=t_iutils
            utilityList[a][b]['t_rutils']=t_rutils
            utilityList[a][b]['prune']=False
            # print(new_itemset, iutil)
        construct_K_utilityList(utilityList[a], tree[a], minUtil,TU,h_sets,k+1)
        
    return 1

def mining(data_path, table_path, minUtil, output):
    h_sets={}
    utilityList, tree, TU=construct_1_utilityList(data_path,table_path)
    k=2
    construct_K_utilityList(utilityList,tree,minUtil,TU,h_sets,k)
    itemsets=list(h_sets.keys())
    n_huis=len(h_sets)
    if n_huis==0: return
    with open(output, 'wt') as f:
        last=itemsets[-1]
        for itemset in itemsets:
            util=h_sets[itemset]
            for item in itemset:
                f.write(str(item))
                if item!=itemset[-1]: f.write(':')
            f.write(" %.1f"% util)
            if itemset!=last: f.write('\n')
    return True