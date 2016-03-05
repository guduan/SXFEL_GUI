# -*- coding: utf-8 -*-

"""
Module implementing emit.
"""
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_emittance import Ui_Dialog
from util_gettransmat import util_gettransmat
from util_matplotlibwidget import MatplotlibWidget


from pylab import *
from PIL import Image

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import time

    
class emit(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Set up initial para.
#        self.mplwidget1.figure.set_facecolor('none')
#        self.mplwidget2.figure.set_facecolor('none')
#       
#        self.mplwidget1.figure.set_frameon(0)
#        self.mplwidget2.figure.set_frameon(0) 

#        self.mplwidget1 = MatplotlibWidget(self, hold=0)
#        self.mplwidget2 = MatplotlibWidget(self, hold=1)

        self.prof_select='PROF01L0'
        self.modeflag='simu'
#        self.pushButton_start.setEnabled(0)
        
        self.q1k_from=0 
        self.q1k_to=10 
        self.q2k_from=-10
        self.q2k_to=0
        self.q3k_from=0
        self.q3k_to=10
        
        self.use_q1=1
        self.use_q2=1
        self.use_q3=1
        
        self.steps=21
        self.samples=1
        
        self.planex=1
        self.planey=1
 


 
    @pyqtSignature("")
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
#        if not os.path.exists('profile_img'):
#            os.mkdir('profile_img')
        
        self.prof_select=self.comboBox_prof_select.currentText()
        
        self.use_q1=self.checkBox_q1.isChecked()
        self.use_q2=self.checkBox_q2.isChecked()
        self.use_q3=self.checkBox_q3.isChecked()
        
        self.q1k_from  =  float(self.lineEdit_q1k_from.text())
        self.q1k_to    =  float(self.lineEdit_q1k_to.text())
        self.q2k_from  =  float(self.lineEdit_q2k_from.text())
        self.q2k_to    =  float(self.lineEdit_q2k_to.text())
        self.q3k_from  =  float(self.lineEdit_q3k_from.text())
        self.q3k_to    =  float(self.lineEdit_q3k_to.text())

        self.steps     =  float(self.lineEdit_steps.text())
        self.samples   =  float(self.lineEdit_samples.text())
        
        self.planex=self.checkBox_x_plane.isChecked()
        self.planey=self.checkBox_x_plane.isChecked()
        
        
        #
        cmd='elegant v14bemit.ele -macro=use_beamline='+self.use_beamline+ \
            ' -macro=q1name='+self.q1name+ \
            ' -macro=q2name='+self.q2name+ \
            ' -macro=q3name='+self.q3name+ \
            ' -macro=q1k_from='+str(self.q1k_from)+' -macro=q1k_to='+str(self.q1k_to)+ \
            ' -macro=q2k_from='+str(self.q2k_from)+' -macro=q2k_to='+str(self.q2k_to)+ \
            ' -macro=q3k_from='+str(self.q3k_from)+' -macro=q3k_to='+str(self.q3k_to)+ \
            ' -macro=steps='+str(self.steps)+ \
            ' -rpnDefns=/Users/duan/software/notouch/defns.rpn '+ \
            ' > log.txt'

        os.system(cmd)
        
        cmd="sddscollapse -pipe=out v14bemit.fin | sddsprintout -pipe=in -col='("+self.q1name+'.K1,'+self.q2name+'.K1,'+self.q3name+".K1,Sx,Sy)' v14bemit.fit -width=100 -noTitle"

        os.system(cmd)
        
        
        data=np.loadtxt('v14bemit.fit',skiprows=3)

        k01=data[:,0]
        k02=data[:,1]
        k03=data[:,2]
        Sx=data[:,3]
        Sy=data[:,4]

        Sx2=Sx**2
        Sy2=Sy**2

        steps=k01.shape[0]

        Rq01=np.zeros((steps,6,6))
        Rd02=np.zeros((steps,6,6))
        Rq02=np.zeros((steps,6,6))
        Rd03=np.zeros((steps,6,6))
        Rq03=np.zeros((steps,6,6))
        Rd04=np.zeros((steps,6,6))
        R=np.zeros((steps,6,6))

        for i in range(steps):
            Rq01[i]=util_gettransmat('quad',[0.1,k01[i]])
            Rd02[i]=util_gettransmat('drift',[0.1])
            Rq02[i]=util_gettransmat('quad',[0.2,k02[i]])
            Rd03[i]=util_gettransmat('drift',[0.1])
            Rq03[i]=util_gettransmat('quad',[0.1,k03[i]])
            Rd04[i] =util_gettransmat('drift',[0.485])
            
            R[i]=reduce(np.dot,[Rd04[i],Rq03[i],Rd03[i],Rq02[i],Rd02[i],Rq01[i]])

        R11=R[:,0,0].reshape(steps,1)
        R12=R[:,0,1].reshape(steps,1)
        R33=R[:,2,2].reshape(steps,1)
        R34=R[:,2,3].reshape(steps,1)
            
        Tx=np.column_stack((R11**2,R11*R12,R12**2))
        Ty=np.column_stack((R33**2,R33*R34,R34**2))

        ax,bx,cx=np.linalg.lstsq(Tx,Sx2)[0]
        ay,by,cy=np.linalg.lstsq(Ty,Sy2)[0]


        ex=np.sqrt(ax*cx-bx**2/4)
        betax=ax/ex
        alphax=-bx/2/ex
        gammax=(1+alphax**2)/betax

        ey=np.sqrt(ay*cy-by**2/4)
        betay=ay/ey
        alphay=-by/2/ey
        gammay=(1+alphay**2)/betay


        if self.planex:
            self.lineEdit_ex.setText(str(round(ex*1e6, 5)))
            self.lineEdit_alphax.setText(str(round(alphax, 3)))
            self.lineEdit_betax.setText(str(round(betax, 3)))
            self.lineEdit_gammax.setText(str(round(gammax, 3)))
        
        if self.planey:
            self.lineEdit_ey.setText(str(round(ey*1e6, 5)))
            self.lineEdit_alphay.setText(str(round(alphay, 3)))
            self.lineEdit_betay.setText(str(round(betay, 3)))
            self.lineEdit_gammay.setText(str(round(gammay, 3)))
        
        self.mplwidget1.fig.axes
  
#        self.f=np.genfromtxt('linac.Scan.001')
#        self.imageNo=1
#        self.timer=QTimer(self)
#        self.connect(self.timer,SIGNAL("timeout()"),self.LoadImage) 
#        self.timer.start(1000) # ms
            
    def LoadImage(self):
        self.fname='./profile_img/img_%.2d.png' % self.imageNo
        print self.fname
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(QtGui.QPixmap(self.fname))
        self.graphicsView_prof.setScene(self.scene)
        self.graphicsView_prof.show()
        self.mplwidget1.axes.plot(self.f[0:self.imageNo, 0], self.f[0:self.imageNo, 4],'r-o',  ms=8, linewidth=2)
#        self.mplwidget1.axes.hold(True)
        self.mplwidget1.draw()
#        plt.pause(0.5)
        
        
        self.imageNo +=1
        if self.imageNo==11:
            self.timer.stop()


    @pyqtSignature("")
    def on_checkBox_onsite_clicked(self):
        """
        Slot documentation goes here.
        """
        self.modeflag='onsite'
        self.checkBox_simu.setChecked(False) 

    @pyqtSignature("")
    def on_checkBox_simu_clicked(self):
        """
        Slot documentation goes here.
        """
        self.modeflag='simu'
        self.checkBox_onsite.setChecked(False)

    @pyqtSignature("")
    def on_pushButton_pause_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
        
    @pyqtSignature("QString")
    def on_comboBox_prof_select_activated(self, p0):
        """
        Slot documentation goes here.
        """
        self.prof_select=self.comboBox_prof_select.currentText()
        
        if self.prof_select=='PROF01L0':
            self.use_beamline='blemit1'
            self.q1name='Q01L0'
            self.q2name='Q02L0'
            self.q3name='Q03L0'
        else:
            pass
            
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = emit()
    myapp.show()
    sys.exit(app.exec_())
    

