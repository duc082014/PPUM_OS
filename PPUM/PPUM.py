import numpy as np
from timeit import default_timer as timer
from Tools.Data import readData, readHset, u, uis
import math


def checkSubsetOfSensitive(data, uTable, 
                                            s_itemsets, s_utils, 
                                            tid, s_itemset, 
                                            changeItem, dec, dl=True):
    
    for i in range(len(s_itemsets)):  
        if s_itemsets[i] == s_itemset:
            s_utils[i]-=dec
            continue
        if changeItem in s_itemsets[i]: 
            if s_itemsets[i].issubset(set(data[tid].keys())):
                if dl:
                    dec=uis(s_itemsets[i], tid, data, uTable)
                s_utils[i]-=dec  
    return s_utils

def hideSIs(data, uTable, s_itemsets, s_utils, minUtil, func):
    changeItem, tid=None, None
    for i in range(len(s_itemsets)):
        s_itemset=s_itemsets[i]
        s_util=s_utils[i]
        dec=0
        diff = s_util - minUtil 
        while diff > 0 and len(s_itemset)>0:
            
            changeItem, tid = func(data, uTable,
                                    s_itemsets,s_utils, 
                                    s_itemset,changeItem, tid, 
                                    minUtil)
            if (tid is not None) and (changeItem is not None):
                
                total = u(tid, changeItem, data, uTable)
                if (total < diff):
                    uit =uis(s_itemset,tid,data,uTable)
                    dec=uit
                    s_utils=checkSubsetOfSensitive(data, uTable, 
                                            s_itemsets, s_utils, 
                                            tid, 
                                            s_itemset, changeItem, 
                                            dec, dl=True)
                    data[tid].pop(changeItem, None)
                    diff = diff - uit	
                    
                else:
                   
                    dec = math.ceil(diff / uTable[changeItem])
                    s_utils=checkSubsetOfSensitive(data, uTable, 
                                            s_itemsets,s_utils,
                                            tid, 
                                            s_itemset,changeItem, 
                                            dec*uTable[changeItem], False)
                    if data[tid].get(changeItem) is not None:
                        data[tid][changeItem]-=dec
                        if data[tid][changeItem]<1: 
                            # print(data[tid][changeItem])
                            data[tid].pop(changeItem, None)
                    
                    diff= 0
                      
                if len(data[tid].keys())==0: data.pop(tid)
               
            else: break
    return data
                    
          
            



