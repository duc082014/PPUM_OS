import os


class dataset:
    def __init__ (self, name, path, n_transactions, n_items, minUtils, sensitive_percentages, totalUtil=0):
        self.name=name
        self.n_transactions=n_transactions
        self.n_items=n_items
        self.totalUtil=totalUtil
        self.path=path+'q_'+name+'.txt'
        self.uTable=path+'u_'+name+'.txt'
        self.folder_path=path
        self.h_paths={}
        self.s_paths={}

        self.HHUIF={}
        self.MSUMIU={}
        self.MSUMAU={}
        self.MSICF={}

        self.MUTs={}
        self.MUPs=minUtils
        self.SIPs=sensitive_percentages
        

        self.new_h_HHUIF={}
        self.new_h_MSUMIU={}
        self.new_h_MSUMAU={}
        self.new_h_MSICF={}
        #for evaluation
        for i in range (0,len(self.MUPs)):
            MUP=self.MUPs[i]
            dir= path+str(MUP)
            if not os.path.exists(dir):
                    os.mkdir(dir)
            
            
            h=path+'q_'+name+'_h_'+str(MUP)+'.txt'
                
            self.h_paths[MUP]=h
            self.s_paths[MUP]={}

            ############################################
            self.HHUIF[MUP]={}
            self.MSUMIU[MUP]={}
            self.MSUMAU[MUP]={}
            self.MSICF[MUP]={}

        
            #############################################
            self.new_h_HHUIF[MUP]={}
            self.new_h_MSUMIU[MUP]={}
            self.new_h_MSUMAU[MUP]={}
            self.new_h_MSICF[MUP]={}
            ###########################################

            
            for j in range (0, len(self.SIPs)):
                SIP=self.SIPs[j]
                # print(h)
                s=h[:-4]+'_si_'+ '%.1f'%(SIP) +'.txt'
                self.s_paths[MUP][SIP]=s

                new_HHUIF=path+str(MUP)+'/q_'+name+'_HHUIF_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'.txt'
                new_MSICF=path+str(MUP)+'/q_'+name+'_MSICF_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'.txt'
                new_MSUMAU=path+str(MUP)+'/q_'+name+'_MSU_MAU_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'.txt'
                new_MSUMIU=path+str(MUP)+'/q_'+name+'_MSU_MIU_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'.txt'
        
                

                ############################################
                self.HHUIF[MUP][SIP]=new_HHUIF
                self.MSICF[MUP][SIP]=new_MSICF
                self.MSUMAU[MUP][SIP]=new_MSUMAU
                self.MSUMIU[MUP][SIP]=new_MSUMIU
                ############################################
                
                
                self.new_h_HHUIF[MUP][SIP]=path+str(MUP)+'/q_'+name+'_HHUIF'+'_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'_h_new.txt'
                self.new_h_MSUMIU[MUP][SIP]=path+str(MUP)+'/q_'+name+'_MSU_MIU'+'_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'_h_new.txt'
                self.new_h_MSUMAU[MUP][SIP]=path+str(MUP)+'/q_'+name+'_MSU_MAU'+'_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'_h_new.txt'
                self.new_h_MSICF[MUP][SIP]=path+str(MUP)+'/q_'+name+'_MSICF'+'_h_'+str(MUP)+"_si_" + '%.1f'%(SIP) +'_h_new.txt'

    def calMUTs(self, totalUtil=None):
        if totalUtil is not None:
            self.totalUtil=totalUtil
            for i in range (0,len(self.MUPs)):
                MUP=self.MUPs[i]
                self.MUTs[MUP]=int((self.totalUtil*MUP)/100)
    def setMUT(self, MUP, MUT):
        self.MUTs[MUP]=MUT
        # print(self.MUTs)
        

path=r'./Datasets'
foodmart_path=path+ '/foodmart/'
foodmart_n_transactions=4141
foodmart_n_items=1559

foodmart_minUtils=[0.061, 0.062, 0.063, 0.064]
foodmart_sensitive_percentages=[2, 4, 6, 8]
foodmart=dataset('foodmart', foodmart_path, foodmart_n_transactions, foodmart_n_items, foodmart_minUtils, foodmart_sensitive_percentages)


mushrooms_path=path+'/mushrooms/'
mushrooms_n_transactions=8416
mushrooms_n_items=128
mushrooms_minUtils=[10.0, 10.5, 11.0, 11.5]
mushrooms_sensitive_percentages= [6, 7, 8 , 9]
mushrooms=dataset('mushrooms', mushrooms_path, mushrooms_n_transactions, mushrooms_n_items, mushrooms_minUtils, mushrooms_sensitive_percentages)

    

t25i10d10k=path+'/t25i10d10k/'
t25i10d10k_n_transactions=10000
t25i10d10k_n_items=1000
t25i10d10k_minUtils=[0.35, 0.36, 0.37, 0.38]
t25i10d10k_sensitive_percentages=[0.2, 0.4, 0.6, 0.8]
t25i10d10k=dataset('t25i10d10k',t25i10d10k, t25i10d10k_n_transactions, t25i10d10k_n_items, 
                     t25i10d10k_minUtils, t25i10d10k_sensitive_percentages)

t20i6d100k=path+'/t20i6d100k/'
t20i6d100k_n_transactions=100000
t20i6d100k_n_items=1000

t20i6d100k_minUtils=[0.31,0.32,0.33,0.34]
t20i6d100k_sensitive_percentages=[2, 4, 6, 8]
t20i6d100k=dataset('t20i6d100k',t20i6d100k, t20i6d100k_n_transactions, t20i6d100k_n_items, 
                     t20i6d100k_minUtils, t20i6d100k_sensitive_percentages)




