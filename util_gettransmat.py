# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 10:48:26 2016

@author: Administrator
"""
import numpy as np


def util_gettransmat(type,para):
#    R=np.zeros([6,6])
    R=np.eye(6)

    if type=='quadrupole' or type=='quad':
        L=para[0]
        K1=para[1]
        if K1>0:
            kq=np.sqrt(K1)
            
            R[0,0]=np.cos(kq*L)         #R11
            R[0,1]=1/kq*np.sin(kq*L)    #R12
            R[1,0]=-kq*np.sin(kq*L)     #R21
            R[1,1]=np.cos(kq*L)         #R22
            
            R[2,2]=np.cosh(kq*L)         #R33
            R[2,3]=1/kq*np.sinh(kq*L)    #R34
            R[3,2]=kq*np.sinh(kq*L)      #R43
            R[3,3]=np.cosh(kq*L)         #R44
        elif K1<0:
            kq=-np.sqrt(-K1)
            R[0,0]=np.cosh(kq*L)         #R11
            R[0,1]=1/kq*np.sinh(kq*L)    #R12
            R[1,0]=kq*np.sinh(kq*L)      #R21
            R[1,1]=np.cosh(kq*L)         #R22
            
            R[2,2]=np.cos(kq*L)         #R33
            R[2,3]=1/kq*np.sin(kq*L)    #R34
            R[3,2]=-kq*np.sin(kq*L)     #R43
            R[3,3]=np.cos(kq*L)         #R44
            
        else:    #kq == 0:   # if kq~0, set as drift
            R[0,1]=L 
            R[2,3]=L

#            R[4,5]=L/gamma**2            #R56
            
    elif type=='drift' or type=='drif':
        L=para[0]
        R[0,1]=L              #R12
        R[2,3]=L              #R34
        
#        R[4,5]=L/gamma**2            #R56

    else:
        print 'ERROR'

    return R
        
        
        
        