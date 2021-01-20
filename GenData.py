
import numpy as np
import matplotlib.pyplot as plt
from Datasets import mushrooms, foodmart, t20i6d100k, t25i10d10k, path, dataset
import pickle as cPickle
from Tools.GenSIs import genSI
def readData(dataset_path=None):
    data={}
    t=0 #transaction id
    items=set() #unique items
    with open(dataset_path,'r') as f:
        for line in f:
            line=line.rstrip('\n')
            line=line.rstrip(' ')
            # print(line.split(' '))
            lineSplitted=line.split(' ')
            # print(lineSplitted)
            itemset=np.array(lineSplitted).astype(int)
            items.update(lineSplitted)
            data[t]=itemset
            t+=1
    
    print("Number of items: ",len(items))     
    print("Number of transactions: ",t)    
    return data, items

   
def genInternalUtilities(data, path, uTable):
    t_utils=[]
    n_transactions=len(data.keys())
    with open (path,'wt') as f:
        for transaction in data.keys():
            t_len=len(data[transaction])
            t_util=0
            internalUtilities=np.random.randint(low=1,high=5, size=t_len)
            for i in range(t_len):
                item=data[transaction][i]
                inUtil=internalUtilities[i]
                f.write('%d:%d' % (item,inUtil))
                t_util+=uTable[item] * inUtil
                if i!= (t_len-1): f.write(' ')
            if transaction!= (n_transactions-1): f.write('\n')
            t_utils.append(t_util)
    totalUtil=np.sum(t_utils)
    return totalUtil

def genExternalUtilities(items, path):
    n_items=len(items)
    x=np.arange(1,1000,dtype=int)

    # if n_items<1000: 
    #     np.random.shuffle(x)
    #     externalUtilities=x
    # else:
    pdf=logNorm(x)
    pdf=pdf/np.sum(pdf)
    externalUtilities=np.random.choice(x,size=n_items, p=pdf)
    # plt.plot(x,pdf)
    # plt.savefig('foo.png')
   
    items=np.sort(np.array(list(items)).astype(int))
    uTable={}
    with open (path,'wt') as f:
        for i in range(n_items):
            item=items[i]
            exUtil=externalUtilities[i]
            uTable[item]=exUtil
            f.write("%d, %d"%(item, exUtil))
            if i!= n_items-1: f.write('\n')
    return uTable
    

def logNorm(x):

   
    mu=np.mean(np.log(x))
    sigma=np.std(np.log(x))
    
    pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi)))
    
    return pdf
  

def genData(dataset):
    print("==================================")
    print("Dataset name: ",dataset.name)
    data, items=readData(dataset.folder_path+dataset.name+'.txt')
    uTable=genExternalUtilities(items,path=dataset.uTable)
    totalUtil=genInternalUtilities(data=data,path=dataset.path, uTable=uTable)
    print("Total utility: ",totalUtil)
    
    return totalUtil



from Datasets import mushrooms, foodmart, t25i10d10k, t20i6d100k



# datasets=[mushrooms, foodmart, t25i10d10k, t20i6d100k]
datasets=[mushrooms, foodmart]

datasets_utils={}
for ds in datasets:
    ds_totalUtil = genData(ds)
    datasets_utils[ds.name]=ds_totalUtil
    ds.calMUTs(datasets_utils[ds.name])
with open(path + '/datasets.pkl','wb') as f:
    cPickle.dump(datasets, f)
with open(path + '/datasets_utils.pkl','wb') as f:
    cPickle.dump(datasets_utils, f)


#Load
datasets_utils=None
# datasets=[mushrooms, foodmart, t25i10d10k, t20i6d100k]
datasets=[mushrooms]

for ds in datasets:
    for SIP in ds.SIPs:
        genSI(SIP,ds)

with open(path + '/datasets_utils.pkl','rb') as f:
    datasets_utils=cPickle.load(f)
for ds in datasets:
    ds.calMUTs(datasets_utils[ds.name])
with open(path + '/datasets.pkl','wb') as f:
    cPickle.dump(datasets, f)