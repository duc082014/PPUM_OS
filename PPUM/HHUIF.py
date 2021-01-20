import numpy as np
from timeit import default_timer as timer
from PPUM.PPUM import hideSIs, u


  
def addressTIDandItem(data, uTable,
                                    s_itemsets,s_utils, 
                                    s_itemset,changeItem, tid, 
                                    minUtil):
    max_util=0
    for transaction in data.keys():
        t=set(data[transaction].keys())
        if s_itemset.issubset(t):
            for item in s_itemset:
                util = u(transaction,item, data, uTable)
                
                if max_util<util:
                    max_util=util
                    changeItem=item 
                    tid=transaction
    return changeItem, tid

def runAlgorithm(data, uTable,s_itemsets, s_utils, minUtil=None, func=addressTIDandItem):
    
    start=timer()
    new_data=hideSIs(data, uTable, s_itemsets, s_utils, minUtil, func)
    end=timer()
    runtime=end-start
    print("HHUIF runtime: ", runtime)
    return runtime, new_data


