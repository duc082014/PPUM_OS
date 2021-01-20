import numpy as np
from timeit import default_timer as timer
from PPUM.PPUM import hideSIs
 
def addressTIDandItem(data, uTable,
                                    s_itemsets,s_utils, 
                                    s_itemset,changeItem, tid, 
                                    minUtil):
    max_util=0
    ic={}
    for i in range(len(s_itemsets)):
        sv=s_utils[i]
        itemset=s_itemsets[i]
        if sv > minUtil:
            for item in itemset:
                if ic.get(item) is None:
                    ic[item]=1
                else:
                    ic[item]+=1

    maxIC=-1
    for item in ic.keys():
        iic=ic[item]
        if iic > maxIC and item in s_itemset:
            maxIC=iic
            changeItem=item
   
    for transaction in data.keys():
        t=set(data[transaction].keys())
        if s_itemset.issubset(t):
            iq = data[transaction][changeItem]
            iu= iq * uTable[changeItem]
           
            if iu > max_util:
                max_util=iu
                tid=transaction
    return changeItem, tid

def runAlgorithm(data, uTable,s_itemsets, s_utils, minUtil=None, func=addressTIDandItem):
    
    start=timer()
    new_data=hideSIs(data, uTable, s_itemsets, s_utils, minUtil, func)
    end=timer()
    runtime=end-start
    print("MSICF runtime: ", runtime)
    return runtime, new_data


