from MiningAlgo.HUI_Miner import mining
from PPUM import HHUIF, MSICF, MSU_MAU, MSU_MIU
from Tools.Data import readData, readHset, savData
import numpy as np
import _pickle as cPickle
from Datasets import mushrooms,foodmart, t20i6d100k, t25i10d10k
from copy import deepcopy
                
def getResult(HHUIF_temp, MSICF_temp, MSU_MAU_temp, MSU_MIU_temp):  
    HHUIF_temp=np.array(HHUIF_temp)
    MSICF_temp=np.array(MSICF_temp)
    MSU_MAU_temp=np.array(MSU_MAU_temp)
    MSU_MIU_temp=np.array(MSU_MIU_temp)
    return (np.mean(HHUIF_temp,axis=0), np.mean(MSICF_temp,axis=0),
            np.mean(MSU_MAU_temp, axis=0), np.mean(MSU_MIU_temp, axis=0)) 

def Experiments(path, times):
    datasets=None
    with open('./Datasets/datasets.pkl', 'rb') as f:
        datasets=cPickle.load(f)

    algorithms=['HHUIF','MSICF',
                'MSU_MAU', 'MSU_MIU']
    datasets_runtimes={}
    

    for ds in datasets:
        #################################

        datasets_runtimes[ds.name]={}
        for al in algorithms:
            datasets_runtimes[ds.name][al]={}
        #################################
        print("=================================================================================================================")
        print("Dataset: ",ds.name)
        for MUP in ds.MUPs:
            MUT=ds.MUTs[MUP]
            print("Dataset MUP: ",MUP)
            print("Dataset MUT: ",MUT)
            
            h_path=ds.h_paths[MUP]
            SIP=ds.SIPs[-1]
            s_path=ds.s_paths[MUP][SIP]
            print("Dataset SIP: %.2f%%"%(SIP))
            print("==============================================================================================")
                
                

            HHUIF_temp=[]
            MSICF_temp=[]
            MSU_MAU_temp=[]
            MSU_MIU_temp=[]
                #read CPU data:
            data, uTable, _ =  readData(data_path=ds.path, table_path=ds.uTable)
            s_itemsets, s_utils,_=readHset(h_path=s_path)
    
            for j in range(0, times):
                print("=================================================================================")
                order=str(j)+"th"
                if (j==0): order="1st"
                if (j==1): order="2nd"
                if (j==2): order="3rd"
                if (j>2): order="%dth"%(j+1)

                print("Running algorithm %s times"%(order))
                    
                print("---------------------------------------------------------------------------------")
                HHUIF_runtime, HHUIF_new_data = HHUIF.runAlgorithm(deepcopy(data), uTable,
                                                deepcopy(s_itemsets),deepcopy(s_utils) ,
                                                minUtil=ds.MUTs[MUP])
                HHUIF_temp.append(HHUIF_runtime)
                
                
                print("---------------------------------------------------------------------------------")
                MSICF_runtime, MSICF_new_data = MSICF.runAlgorithm(deepcopy(data), uTable,
                                                deepcopy(s_itemsets),deepcopy(s_utils) ,
                                                minUtil=ds.MUTs[MUP])
                MSICF_temp.append(MSICF_runtime)    

                print("---------------------------------------------------------------------------------")
                MSU_MAU_runtime, MSU_MAU_new_data = MSU_MAU.runAlgorithm(deepcopy(data), uTable,
                                                deepcopy(s_itemsets),deepcopy(s_utils) ,
                                                minUtil=ds.MUTs[MUP])
                MSU_MAU_temp.append(MSU_MAU_runtime)
                print("---------------------------------------------------------------------------------")
                MSU_MIU_runtime, MSU_MIU_new_data = MSU_MIU.runAlgorithm(deepcopy(data), uTable,
                                                deepcopy(s_itemsets),deepcopy(s_utils) ,
                                                minUtil=ds.MUTs[MUP])
                MSU_MIU_temp.append(MSU_MIU_runtime)
                print("==============================================================================================")
                
                # print("Diff in %d positions: "%len(compareData(c_new_data,g_new_data)))
                
                
                
                savData(ds.HHUIF[MUP][SIP], HHUIF_new_data)
                savData(ds.MSICF[MUP][SIP], MSICF_new_data)
                savData(ds.MSUMAU[MUP][SIP], MSU_MAU_new_data)
                savData(ds.MSUMIU[MUP][SIP], MSU_MIU_new_data)
                
            
                
                
            runtimes=getResult(HHUIF_temp, MSICF_temp, MSU_MAU_temp, MSU_MIU_temp)  
            for i in range(len(algorithms)):
                al=algorithms[i]
                datasets_runtimes[ds.name][al][MUP]=runtimes[i]           
                
    return datasets_runtimes
    


def Ex1():
    path=r'./'
    dpath=r'./Datasets'
    
    datasets_runtimes=Experiments(path=dpath, times=1)
    # print(c_runtimes, g_runtimes)
    runtimes_path=path+'/runtimes1.pkl'

    with open(runtimes_path, 'wb') as f:
        cPickle.dump(datasets_runtimes, f)


  