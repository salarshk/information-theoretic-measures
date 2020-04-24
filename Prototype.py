import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def mi_df(a,b):
    eps=0.0000000000001
    unia=a.unique()
    unib=b.unique()
    pa=np.histogram(a,np.size(unia))
    pa=np.array(pa[0]/len(a) +eps)
    ha=sum((-np.log2(pa))*pa)
    pb=np.histogram(b,np.size(unib))
    pb=np.array(pb[0]/len(b) +eps)
    hb=sum((-np.log2(pb))*pb)
    pab=np.histogram2d(a,b,[np.size(unia),np.size(unib)])
    pab=np.array(pab[0]/len(a) +eps)
    hab=sum(sum((-np.log2(pab))*pab))
    iab=ha+hb-hab
    return iab
def mi_df_cat_val(a,b):
    eps=0.0000000000001
    unia=a.unique()
    unib=b.unique()
    pa=a.value_counts()
    pa=pa/sum(pa)
    ha=sum((-np.log2(pa))*pa)
    pb=np.histogram(b,np.size(unib))
    pb=np.array(pb[0]/len(b) +eps)
    hb=sum((-np.log2(pb))*pb)
    pab=np.zeros([np.size(unia),np.size(unib)])
    z,t=0,0
    for i in unia:
        for j in unib:
            pab[z,t]=sum((a==i)&(b==j))
            t=t+1
        z=z+1
        t=0
    pab=pab/sum(sum(pab)) +eps
    hab=sum(sum((-np.log2(pab))*pab))
    iab=ha+hb-hab
    return iab
def entr(a):
    eps=0.0000000000001
    unia=a.unique()
    pa=np.histogram(a,np.size(unia))
    pa=np.array(pa[0]/len(a) +eps)
    ha=sum((-np.log2(pa))*pa)
    return ha
def entr_cat(a):
    eps=0.0000000000001
    pa=a.value_counts()
    pa=pa/sum(pa) +eps
    ha=sum((-np.log2(pa))*pa)
    return ha 
def entr_cont(a):
    eps=0.0000000000001
    import math
    nbin=math.ceil(len(a)/20)
    pa=np.histogram(a,nbin)
    pa=np.array(pa[0]/len(a) +eps)
    ha=sum((-np.log2(pa))*pa)
    return ha
def cond_entr(a,b):
    eps=0.0000000000001
    unia=a.unique()
    unib=b.unique()
    pa=np.histogram(a,np.size(unia))
    pa=np.array(pa[0]/len(a) +eps)
    ha=sum((-np.log2(pa))*pa)
    pb=np.histogram(b,np.size(unib))
    pb=np.array(pb[0]/len(b) +eps)
    hb=sum((-np.log2(pb))*pb)
    pab=np.histogram2d(a,b,[np.size(unia),np.size(unib)])
    pab=np.array(pab[0]/len(a) +eps)
    hab=sum(sum((-np.log2(pab))*pab))
    h_a_cond_b=hab-hb;
    return h_a_cond_b
df=pd.read_csv('Flags.csv')
df1=df.iloc[:,5:16]
#df1=df1[df1["colours"]>4]
#df1=df1.loc[(df1["colours"]>5) & (df1["stripes"]<=3)]
#df1=df1[df1["gold"]==1]
#df1=df1[df1["blue"]==1]
#df1=df1[df1["colours"]>5]
mival=np.zeros([np.shape(df1)[1],np.shape(df1)[1]])
hconval=np.zeros([np.shape(df1)[1],np.shape(df1)[1]])
entrval=np.zeros([np.shape(df1)[1],1])
for i in range(np.shape(df1)[1]):
    entrval[i]=entr(df1.iloc[:,i])
    for j in range(np.shape(df1)[1]):
        mival[i,j]=mi_df(df1.iloc[:,i],df1.iloc[:,j])/entr(df1.iloc[:,i])
        hconval[i,j]=cond_entr(df1.iloc[:,i],df1.iloc[:,j])
dev=np.zeros([7,1])
for i in range(2,9):
    dev[i-2]=(entr(df[df.colours<i].colours)+entr(df[df.colours>=i].colours))
devcat=np.zeros([len(df.topleft.unique()),1])
t=0
for i in df.topleft.unique():
    devcat[t]=entr_cat(df.topleft)-entr_cat(df[df.topleft!=i].topleft)
    t=t+1
devcat_main=np.zeros([len(df.mainhue.unique()),1])
t=0
for i in df.mainhue.unique():
    devcat_main[t]=entr_cat(df.mainhue)-entr_cat(df[df.mainhue!=i].mainhue)
    t=t+1
t2=np.linspace(1,max(df.area),10000)
dev_cont=np.zeros([len(t2),1])
t3=0
for i in t2:
    dev_cont[t3]=(entr_cont(df[df.area>=i].area)+entr_cont(df[df.area<i].area))
    t3=t3+1
    
    