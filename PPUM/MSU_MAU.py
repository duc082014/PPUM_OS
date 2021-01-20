import numpy as np
from timeit import default_timer as timer
from PPUM.PPUM import hideSIs, uis, u
  
def addressTIDandItem(data, uTable,
                        s_itemsets,s_utils, 
                        s_itemset,changeItem, tid, 
                        minUtil):
    maxMSU = 0
    maxUtil=0
    changeItem, tid=None, None
    for transaction in data.keys():
        if s_itemset.issubset(set(data[transaction].keys())):
            msu=0
            for item in s_itemset:
                iq=data[transaction][item]
                if iq<1:
                    msu= 0 
                    break
                iu= iq * uTable[item]
                msu+=iu
            if msu> maxMSU :
                maxMSU=msu
                tid=transaction
   
    for item in s_itemset:
            iu =  u(item, tid, data, uTable)
            if iu > maxUtil:
                maxUtil=iu
                changeItem=item
    return changeItem, tid
    
def runAlgorithm(data, uTable,s_itemsets, s_utils, minUtil=None, func=addressTIDandItem):
    
    start=timer()
    new_data=hideSIs(data, uTable, s_itemsets, s_utils, minUtil, func)
    end=timer()
    runtime=end-start
    print("MSU_MAU runtime: ", runtime)
    return runtime, new_data


