import numpy as np
import re

def readQuantiativeData(data_path):
    """
    Parameter:
    -----------------------------
    data_path: dataset 's path
    ----------------------------
    Return:
        data: dictionary
            each key is a transaction
            a transaction represented by a dictionary with 
                keys are items 
                values are internal utilities of items
        itemsets: numpy array
            each element contain a python set represented a transaction
    """
    data={}
    itemsets=[]
    t=0 #transaction
    with open(data_path,'r') as f:
        for line in f:
            row={}
            s=[]
            line=line.rstrip('\n')
            line=line.rstrip(' ')
            lineSplitted=line.split(' ')
            for e in lineSplitted:
                item, utility=e.split(':')
                item=int(item)
                s.append(item)
                s.sort()
                utility=int(utility)
                row[item]=utility
            itemsets.append(set(s))
            data[t]=row

            t+=1

    return data, np.array(itemsets)
def readUtable(table_path):
    '''Parameters
    ------------------------------
    table_path: external utility table 's path
    ------------------------------
    Return:
        uTable: a dictionary 
            each key is a item
            each value is external utility of item'''
   
    uTable={}
    with open(table_path) as f:
        for line in f:
            item,utility=line.split(', ')
            uTable[int(item)]=int(utility)
    return uTable

def readData(data_path=None,table_path=None):
    data, itemsets=readQuantiativeData(data_path)
    uTable=readUtable(table_path)
    
    return data, uTable, itemsets

def readHset(h_path=None):
    ''' Read utility mining result
    Parameters
    ------------------------------
    h_path: mining result 's path
    ------------------------------
    Return 
        numpy array contains high utility itemsets (pythonset)
        numpy array contains utilites of high utility itemsets
        numpy array contains sizes if high utility itemsets
    '''
    itemsets=[]
    sizes=[]
    utilities=[]
    with open(h_path,'r') as f:
       
        for line in f:
            line=line.rstrip('\n')
            line=line.rstrip(' ')
            lineSplitted=line.split(' ')
            utility=int(float(lineSplitted[1]))
            itemset=set(map(int,lineSplitted[0].split(':')))
            size=len(itemset)
        
            itemsets.append(itemset)
            utilities.append(utility)
            sizes.append(size)
    return np.array(itemsets), np.array(utilities).astype(np.int32), np.array(sizes).astype(np.uint8)

def savData(path, data):
    with open(path,"wt") as f:
        transactions=list(data.keys())
        for transaction in transactions:
            items =  list(data[transaction].keys())
            for item in items:
                f.write("%d:%d" % (item,data[transaction][item]))
                if item != items[-1]: 
                    f.write(' ')   
            if transaction!= transactions[-1]:
                f.write("\n")
def uis(itemset, tid, data, uTable):
    '''Parameters
    -------------------------------
    itemset: pythonset
    uTable: external utilities table
    -------------------------------
    Return utility of itemset in transaction

    '''
    util=0
    for item in itemset:
        v=u(item, tid, data, uTable)
        if v==0: return 0
        util+= v
    return util
def u(item, tid, data, uTable):
    '''Parameters
    -------------------------------
    uTable: external utilities table
    -------------------------------
    Return utility of item in transaction
    '''
    inU=data[tid].get(item) 
    if  inU is not None:
        return inU*uTable[item]
    else:
         return 0  

def totalUtil(item, data, uTable):
    total=0
    for transaction in data.keys():
        total += u(transaction, item, data, uTable)
    return total