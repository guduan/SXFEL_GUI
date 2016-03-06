# -*- coding: utf-8 -*-

"""
Module implementing emit.
"""
import sys, os, time, platform
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_emittance import Ui_Dialog
from util_gettransmat import util_gettransmat
from util_matplotlibwidget import MatplotlibWidget

from pylab import *

import numpy as np

    
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
        self.mplwidget1.figure.set_facecolor('none')
        self.mplwidget2.figure.set_facecolor('none')
        self.pushButton_start.setEnabled(0)
        self.pushButton_stop.setEnabled(0)
        
        self.mplwidget1.axes.hold(False)
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

        self.clear_previous()
        self.pushButton_stop.setEnabled(1)

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

        self.steps     =  int(self.lineEdit_steps.text())
        self.samples   =  int(self.lineEdit_samples.text())
        
        self.planex=self.checkBox_x_plane.isChecked()
        self.planey=self.checkBox_y_plane.isChecked()
        
        
        #
        sysstr=platform.system()
        
        if sysstr=='Windows' or sysstr=='Linux':
            cmd='elegant v14bemit.ele -macro=use_beamline='+self.use_beamline+ \
                ' -macro=q1name='+self.q1name+ \
                ' -macro=q2name='+self.q2name+ \
                ' -macro=q3name='+self.q3name+ \
                ' -macro=q1k_from='+str(self.q1k_from)+' -macro=q1k_to='+str(self.q1k_to)+ \
                ' -macro=q2k_from='+str(self.q2k_from)+' -macro=q2k_to='+str(self.q2k_to)+ \
                ' -macro=q3k_from='+str(self.q3k_from)+' -macro=q3k_to='+str(self.q3k_to)+ \
                ' -macro=steps='+str(self.steps)+ \
                ' > log.txt'
        else:
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
        
#        cmd="sddscollapse -pipe=out v14bemit.fin | sddsprintout -pipe=in -col='("+self.q1name+'.K1,'+self.q2name+'.K1,'+self.q3name+".K1,Sx,Sy)' v14bemit.fit -width=150 -noTitle"
        cmd='sddscollapse -pipe=out v14bemit.fin | sddsprintout -pipe=in'+ \
        ' -col='+self.q1name+'.K1 '+ \
        ' -col='+self.q2name+'.K1 '+ \
        ' -col='+self.q3name+'.K1 '+ \
        ' -col=Sx -col=Sy v14bemit.fit -width=150 -noTitle'

        os.system(cmd)
        
        # show images on profiles. plot on mplwidget1
        cmd="sddssplit v14bemit.out -digits=2 -rootname='img' -extension='out'"
        os.system(cmd)
        
        img=np.zeros((self.steps,100,100))

        for i in range(1, self.steps+1):
            cmd='sddshist2d -pipe=out img%.2d.out -col=x,y -xparam=100 -yparam=100 -smooth \
            | sddsprintout -col=frequency -pipe=in img%.2d.h2d -noTitle' %(i, i)
            os.system(cmd)
   
        self.imageNo=1
        self.timer=QTimer(self)
        self.connect(self.timer,SIGNAL("timeout()"),self.Getprofileimg) 
        self.timer.start(1000) # ms


        # -------------------
        data=np.loadtxt('v14bemit.fit',skiprows=3)

        self.k01=data[:,0]
        self.k02=data[:,1]
        self.k03=data[:,2]
        self.Sx=data[:,3]
        self.Sy=data[:,4]

        self.Sx2=self.Sx**2
        self.Sy2=self.Sy**2

        Rq01=np.zeros((self.steps,6,6))
        Rd02=np.zeros((self.steps,6,6))
        Rq02=np.zeros((self.steps,6,6))
        Rd03=np.zeros((self.steps,6,6))
        Rq03=np.zeros((self.steps,6,6))
        Rd04=np.zeros((self.steps,6,6))
        R=np.zeros((self.steps,6,6))

        for i in range(self.steps):
            Rq01[i]=util_gettransmat('quad',[0.1,self.k01[i]])
            Rd02[i]=util_gettransmat('drift',[0.1])
            Rq02[i]=util_gettransmat('quad',[0.2,self.k02[i]])
            Rd03[i]=util_gettransmat('drift',[0.1])
            Rq03[i]=util_gettransmat('quad',[0.1,self.k03[i]])
            Rd04[i] =util_gettransmat('drift',[0.485])
            
            R[i]=reduce(np.dot,[Rd04[i],Rq03[i],Rd03[i],Rq02[i],Rd02[i],Rq01[i]])

        R11=R[:,0,0].reshape(self.steps,1)
        R12=R[:,0,1].reshape(self.steps,1)
        R33=R[:,2,2].reshape(self.steps,1)
        R34=R[:,2,3].reshape(self.steps,1)
            
        self.Tx=np.column_stack((R11**2,R11*R12,R12**2))
        self.Ty=np.column_stack((R33**2,R33*R34,R34**2))

        ax,bx,cx=np.linalg.lstsq(self.Tx,self.Sx2)[0]
        ay,by,cy=np.linalg.lstsq(self.Ty,self.Sy2)[0]


        self.ex=np.sqrt(ax*cx-bx**2/4)
        self.betax=ax/self.ex
        self.alphax=-bx/2/self.ex
        self.gammax=(1+self.alphax**2)/self.betax

        self.ey=np.sqrt(ay*cy-by**2/4)
        self.betay=ay/self.ey
        self.alphay=-by/2/self.ey
        self.gammay=(1+self.alphay**2)/self.betay

        self.mplwidget2.axes.set_xlabel('Q01L0.K1 [$m^{-1}$]', fontsize=12)
        self.mplwidget2.axes.set_ylabel('$\sigma$ [m]', fontsize=12)
        self.mplwidget2.axes.set_yscale('log', basey=10)
#        self.mplwidget2.axes.legend(['$\sigma_x$','$\sigma_y$' ], fontsize=9, frameon=0, loc='best')
      
        self.mplwidget2.figure.tight_layout()
        self.mplwidget2.axes.hold(True)
#        self.mplwidget2.draw()  

    def Getprofileimg(self):
#        self.mplwidget1.axes.cla()
#        self.mplwidget1.figure.clf()
        filestr='img%.2d.h2d' %self.imageNo
        data=np.loadtxt(filestr, skiprows=2)
        img=data.reshape([100,100])
        ax=self.mplwidget1.axes.imshow(img)
#        self.mplwidget1.figure.colorbar(ax)
        self.mplwidget1.axes.imshow(img)
        self.mplwidget1.draw()
#        self.mplwidget1.show()
        
        self.mplwidget2.axes.plot(self.k01[self.imageNo-1], self.Sx[self.imageNo-1], 'ro', self.k01[self.imageNo-1], self.Sy[self.imageNo-1], 'bo', linewidth=1)
        self.mplwidget2.draw()
        
        # progress bar
        val=float(self.imageNo)/self.steps*100
        self.progressBar.setValue(val)
        self.label_progress.setText(str(int(val)))
        
        self.imageNo=self.imageNo+1
        if self.imageNo==self.steps:
            self.timer.stop()
            self.progressBar.setValue(100)
            self.label_progress.setText(str(100))
            
            self.mplwidget2.axes.plot(self.k01, self.Sx, '-ro', self.k01, self.Sy, '-bo', linewidth=1)
            self.mplwidget2.axes.legend(['$\sigma_x$','$\sigma_y$' ], fontsize=9, frameon=0, loc='best')
            self.mplwidget2.draw()
            
            if self.planex:
                self.lineEdit_ex.setText(str(round(self.ex*1e6, 5)))
                self.lineEdit_alphax.setText(str(round(self.alphax, 3)))
                self.lineEdit_betax.setText(str(round(self.betax, 3)))
                self.lineEdit_gammax.setText(str(round(self.gammax, 3)))
            
            if self.planey:
                self.lineEdit_ey.setText(str(round(self.ey*1e6, 5)))
                self.lineEdit_alphay.setText(str(round(self.alphay, 3)))
                self.lineEdit_betay.setText(str(round(self.betay, 3)))
                self.lineEdit_gammay.setText(str(round(self.gammay, 3)))


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
    def on_pushButton_stop_clicked(self):
        """
        Slot documentation goes here.
        """
        self.timer.stop()
        
        
    @pyqtSignature("QString")
    def on_comboBox_prof_select_activated(self, p0):
        """
        Slot documentation goes here.
        """
        self.prof_select=self.comboBox_prof_select.currentText()
        self.pushButton_start.setEnabled(1)
        
        if self.prof_select=='PROF01L0':
            self.use_beamline='blemit1'
            self.q1name='Q01L0'
            self.q2name='Q02L0'
            self.q3name='Q03L0'
        else:
            pass

    def clear_previous(self):
        # clear previous informations
        self.mplwidget1.axes.cla()
        self.mplwidget2.axes.cla()
        
        self.lineEdit_ex.setText('')
        self.lineEdit_alphax.setText('')
        self.lineEdit_betax.setText('')
        self.lineEdit_gammax.setText('')

        self.lineEdit_ey.setText('')
        self.lineEdit_alphay.setText('')
        self.lineEdit_betay.setText('')
        self.lineEdit_gammay.setText('')
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = emit()
    myapp.show()
    sys.exit(app.exec_())
    

