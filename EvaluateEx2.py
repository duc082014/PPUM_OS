
from SideEffects import HF, MC, AC
import pickle as cPickle

datasets=None
with open('./Datasets/datasets.pkl','rb') as f:
    datasets=cPickle.load(f)

ex2_performances={}
for ds in datasets:
    ex2_performances[ds.name]={}
    al_paths={'HHUIF':{'s': ds.s_paths, 
                                'nh' :ds.new_h_HHUIF},
                                
                        'MSU_MAU': {'s': ds.s_paths, 
                                    'nh' :ds.new_h_MSUMAU}, 
                        'MSU_MIU': {'s': ds.s_paths, 
                                    'nh' :ds.new_h_MSUMIU},
                        'MSICF':  {'s': ds.s_paths, 
                                    'nh' :ds.new_h_MSICF}}
   
    criteria={'HF': HF, 'MC':MC, 'AC': AC}

    print("===================================================================================")
    print("===============================================================")
    print("Dataset: ",ds.name)
    MUP=ds.MUPs[0]
    # print(SIP)
    for SIP in ds.SIPs:
        h_path=ds.h_paths[MUP]
        ex2_performances[ds.name][MUP] = {}
        print("MUP: ",MUP,"%")
        print("MUT: ",ds.MUTs[MUP])
        for al in al_paths:
        
            
            
            ex2_performances[ds.name][MUP][al] = {}
            print("---------------------------------------------------")
            for c in criteria:
                print("%s %s: "%(al,c), end='')
                ret=criteria[c](al_paths[al]['s'][MUP][SIP],h_path,al_paths[al]['nh'][MUP][SIP])
                ex2_performances[ds.name][MUP][al][c] = ret
                print(ret)
        print("=======================================================================")

with open('performance2.pkl','wb') as f:
    cPickle.dump(ex2_performances,f)