
import pickle as cPickle
from MiningAlgo.HUI_Miner import mining

datasets=None
with open('./Datasets/datasets.pkl', 'rb') as f:
        datasets=cPickle.load(f)

# datasets=[datasets[3]]
algorithms=['HHUIF','MSICF',
                'MSU_MAU', 'MSU_MIU']

def MineResults2():
        for ds in datasets:
                for SIP in ds.SIPs:
                        MUP=ds.MUPs[0]
                        MUT=ds.MUTs[MUP]
                        
                 
                        mining(ds.HHUIF[MUP][SIP], ds.uTable,MUT, ds.new_h_HHUIF[MUP][SIP])

                        mining(ds.MSICF[MUP][SIP], ds.uTable,MUT, ds.new_h_MSICF[MUP][SIP])
                        mining(ds.MSUMAU[MUP][SIP], ds.uTable,MUT, ds.new_h_MSUMAU[MUP][SIP])
                        mining(ds.MSUMIU[MUP][SIP], ds.uTable,MUT, ds.new_h_MSUMIU[MUP][SIP])

def MineResults1():
        for ds in datasets:
                for MUP in ds.MUPs:
                        SIP=ds.SIPs[-1]
                        MUT=ds.MUTs[MUP]
                        
                        mining(ds.new_c_paths[MUP][SIP], ds.uTable,  MUT, ds.new_h_c_paths[MUP][SIP])
                        mining(ds.new_g_paths[MUP][SIP], ds.uTable,MUT, ds.new_h_g_paths[MUP][SIP])

                        mining(ds.HHUIF[MUP][SIP], ds.uTable,MUT, ds.new_h_HHUIF[MUP][SIP])

                        mining(ds.MSICF[MUP][SIP], ds.uTable,MUT, ds.new_h_MSICF[MUP][SIP])
                        mining(ds.MSUMAU[MUP][SIP], ds.uTable,MUT, ds.new_h_MSUMAU[MUP][SIP])
                        mining(ds.MSUMIU[MUP][SIP], ds.uTable,MUT, ds.new_h_MSUMIU[MUP][SIP])

MineResults2()
MineResults1()

# ds=example1
# mining(ds,ds.MUTs[0], 'output.txt')