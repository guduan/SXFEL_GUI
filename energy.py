# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import sys, os, time
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature

from Ui_energy import Ui_MainWindow

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.pushButton_start.setEnabled(0)
        self.pushButton_pause.setEnabled(0)
        
        self.amp_a2=40
        self.amp_a3=40
        self.amp_a4=46.5
        self.amp_a5=46.5
        self.amp_a6=46.5
        self.amp_a7=46.5
        
        self.pha_a2=90
        self.pha_a3=90
        self.pha_a4=90
        self.pha_a5=90
        self.pha_a6=90
        self.pha_a7=90
        
        self.B_select='B2'
        self.use_beamline='bl_energy_b2';
        self.prof_name='Prof B2';
        self.designed_energy=92.99; #design Value when Acc2 on crest.MeV
        self.designed_etax=9.877890e-001;
        self.L_bend=0.3;
        
        self.create_mpl_frame()
        
        
    def create_mpl_frame(self):
        self.widget1=QtGui.QWidget()
        self.fig1 = Figure((4, 4))
        self.fig1.set_facecolor('none')
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.setParent(self.widget1)
        self.canvas1.setFocusPolicy(Qt.StrongFocus)
        self.canvas1.setFocus()
        self.mpl_toolbar1 = NavigationToolbar(self.canvas1, self.widget1)
        
        
        self.widget2=QtGui.QWidget()
        self.fig2 = Figure((4, 3.5))
        self.fig2.set_facecolor('none')
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas2.setParent(self.widget2)
#        self.mpl_toolbar2 = NavigationToolbar(self.canvas2, self.widget2)

        self.vbox_mpl1.addWidget(self.widget1)
        self.vbox_mpl1.addWidget(self.mpl_toolbar1)
        self.vbox_mpl2.addWidget(self.widget2)
#        self.vbox_mpl2.addWidget(self.mpl_toolbar2)

        
        self.axes1 = self.fig1.add_subplot(111)
        self.axes2 = self.fig2.add_subplot(211)
        self.axes3 = self.fig2.add_subplot(212)
        
        
    @pyqtSignature("QString")
    def on_comboBox_b_select_activated(self, p0):
        """
        Slot documentation goes here.
        """
        self.B_select=self.comboBox_b_select.currentText()
        
        if self.B_select=='B2':
                self.use_beamline='bl_energy_b2';
                self.prof_name='Prof B2';
                self.designed_energy=92.99; #design Value when Acc2 on crest.MeV
                self.designed_etax=9.877890e-001;
                self.L_bend=0.3;
        elif self.B_select=='B3':
                self.use_beamline='bl_energy_b3';
                self.prof_name='Prof B3';
                self.designed_energy=301.332;#design Value when A2~A7 on crest.MeV
                self.designed_etax=1.064551;
                self.L_bend=0.6;

        self.lineEdit_profile.setText(self.prof_name)
        self.lineEdit_designed_energy.setText(str(self.designed_energy))
        self.lineEdit_designed_dispersion.setText(str(self.designed_etax))
    
    @pyqtSignature("")
    def on_lineEdit_amp_a2_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.amp_a2=float(self.lineEdit_amp_a2.text())
        self.horizontalScrollBar_amp_a2.setValue(self.amp_a2*10)

    @pyqtSignature("int")
    def on_horizontalScrollBar_amp_a2_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.amp_a2=self.horizontalScrollBar_amp_a2.value()/10.0
        self.lineEdit_amp_a2.setText(str(self.amp_a2))
        
    @pyqtSignature("int")
    def on_horizontalScrollBar_pha_a2_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.pha_a2=self.horizontalScrollBar_pha_a2.value()/10.0
        self.lineEdit_pha_a2.setText(str(self.pha_a2))
    

    @pyqtSignature("")
    def on_lineEdit_amp_a3_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.amp_a3=float(self.lineEdit_amp_a3.text())
        self.horizontalScrollBar_amp_a3.setValue(self.amp_a3*10)
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_amp_a3_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.amp_a3=self.horizontalScrollBar_amp_a3.value()/10.0
        self.lineEdit_amp_a3.setText(str(self.amp_a3))
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_pha_a3_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.pha_a3=self.horizontalScrollBar_pha_a3.value()/10.0
        self.lineEdit_pha_a3.setText(str(self.pha_a3))
    
    @pyqtSignature("")
    def on_lineEdit_amp_a4_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.amp_a4=float(self.lineEdit_amp_a4.text())
        self.horizontalScrollBar_amp_a4.setValue(self.amp_a4*10)
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_amp_a4_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.amp_a4=self.horizontalScrollBar_amp_a4.value()/10.0
        self.lineEdit_amp_a4.setText(str(self.amp_a4))
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_pha_a4_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.pha_a4=self.horizontalScrollBar_pha_a4.value()/10.0
        self.lineEdit_pha_a4.setText(str(self.pha_a4))
    
    @pyqtSignature("")
    def on_lineEdit_amp_a5_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.amp_a5=float(self.lineEdit_amp_a5.text())
        self.horizontalScrollBar_amp_a5.setValue(self.amp_a5*10)
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_amp_a5_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.amp_a5=self.horizontalScrollBar_amp_a5.value()/10.0
        self.lineEdit_amp_a5.setText(str(self.amp_a5))
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_pha_a5_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.pha_a5=self.horizontalScrollBar_pha_a5.value()/10.0
        self.lineEdit_pha_a5.setText(str(self.pha_a5))
    
    @pyqtSignature("")
    def on_lineEdit_amp_a6_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.amp_a6=float(self.lineEdit_amp_a6.text())
        self.horizontalScrollBar_amp_a6.setValue(self.amp_a6*10)
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_amp_a6_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.amp_a6=self.horizontalScrollBar_amp_a6.value()/10.0
        self.lineEdit_amp_a6.setText(str(self.amp_a6))
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_pha_a6_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.pha_a6=self.horizontalScrollBar_pha_a6.value()/10.0
        self.lineEdit_pha_a6.setText(str(self.pha_a6))
    
    @pyqtSignature("")
    def on_lineEdit_amp_a7_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.amp_a7=float(self.lineEdit_amp_a7.text())
        self.horizontalScrollBar_pha_a7.setValue(self.amp_a7*10)
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_amp_a7_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.amp_a7=self.horizontalScrollBar_amp_a7.value()/10.0
        self.lineEdit_amp_a7.setText(str(self.amp_a7))
    
    @pyqtSignature("int")
    def on_horizontalScrollBar_pha_a7_actionTriggered(self, action):
        """
        Slot documentation goes here.
        """
        self.pha_a7=self.horizontalScrollBar_pha_a7.value()/10.0
        self.lineEdit_pha_a7.setText(str(self.pha_a7))

    @pyqtSignature("")
    def on_lineEdit_pha_a2_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.pha_a2=float(self.lineEdit_pha_a2.text())
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
    
    @pyqtSignature("")
    def on_lineEdit_pha_a3_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.pha_a3=float(self.lineEdit_pha_a3.text())
        self.horizontalScrollBar_pha_a3.setValue(self.pha_a3)
    
    @pyqtSignature("")
    def on_lineEdit_pha_a4_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.pha_a4=float(self.lineEdit_pha_a4.text())
        self.horizontalScrollBar_pha_a4.setValue(self.pha_a4)
    
    @pyqtSignature("")
    def on_lineEdit_pha_a5_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.pha_a5=float(self.lineEdit_pha_a5.text())
        self.horizontalScrollBar_pha_a5.setValue(self.pha_a5)
    
    @pyqtSignature("")
    def on_lineEdit_pha_a6_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.pha_a6=float(self.lineEdit_pha_a6.text())
        self.horizontalScrollBar_pha_a6.setValue(self.pha_a6)
    
    @pyqtSignature("")
    def on_lineEdit_pha_a7_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.pha_a7=float(self.lineEdit_pha_a7.text())
        self.horizontalScrollBar_pha_a7.setValue(self.pha_a7)
        
    @pyqtSignature("")
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """ 
        
        self.energy=[]
        self.energy_spread=[]
        self.volt_error=0.4e6  # in MeV
        
        self.timer=QTimer(self)
        self.connect(self.timer,SIGNAL("timeout()"),self.show_profile) 
        self.timer.start(1000) # ms
        
        
    @pyqtSignature("")
    def on_pushButton_pause_clicked(self):
        """
        Slot documentation goes here.
        """
        self.timer.stop()
        
        self.axes1.cla()
        self.axes2.cla()
        self.axes3.cla()

    @pyqtSignature("")
    def on_pushButton_set_clicked(self):
        """
        Slot documentation goes here.
        """
        self.amp_a2=float(self.lineEdit_amp_a2.text())
        self.amp_a3=float(self.lineEdit_amp_a3.text())
        self.amp_a4=float(self.lineEdit_amp_a4.text())
        self.amp_a5=float(self.lineEdit_amp_a5.text())
        self.amp_a6=float(self.lineEdit_amp_a6.text())
        self.amp_a7=float(self.lineEdit_amp_a7.text())

        self.pha_a2=float(self.lineEdit_pha_a2.text())
        self.pha_a3=float(self.lineEdit_pha_a3.text())
        self.pha_a4=float(self.lineEdit_pha_a4.text())
        self.pha_a5=float(self.lineEdit_pha_a5.text())
        self.pha_a6=float(self.lineEdit_pha_a6.text())
        self.pha_a7=float(self.lineEdit_pha_a7.text())
        
        self.pushButton_start.setEnabled(1)
        self.pushButton_pause.setEnabled(1)
        
    def show_profile(self):
        if self.B_select=='B2':
            amp_a2=self.amp_a2*1e6
            pha_a2=self.pha_a2
            volt_error=self.volt_error*np.random.rand()
            
            cmd='elegant dalian_energy_b2.ele -macro=use_beamline='+self.use_beamline+' '\
            +'-macro=volt_error='+str(volt_error)+' '\
            +'-macro=a2amp='+str(amp_a2)+' '\
            +'-macro=a2pha='+str(pha_a2)+' '\
#            +'-rpnDefns=/Users/duan/software/notouch/defns.rpn> log.txt' # only need in MAC OS
            os.system(cmd)
            print cmd
            os.system('sdds2plaindata -noRowCount -parameter=Sx -parameter=Sy -para=Cx -para=Cy \
            -para=pCentral dalian_energy_b2.fin dalian_energy_b2.profile.txt')
            
            self.profile_image=np.loadtxt('dalian_energy_b2.profile.txt')
            
        elif self.B_select=='B3':
            amp_a2=self.amp_a2*1e6
            amp_a3=self.amp_a3*1e6
            amp_a4=self.amp_a4*1e6
            amp_a5=self.amp_a5*1e6
            amp_a6=self.amp_a6*1e6
            amp_a7=self.amp_a7*1e6
            
            pha_a2=self.pha_a2
            pha_a3=self.pha_a3
            pha_a4=self.pha_a4
            pha_a5=self.pha_a5
            pha_a6=self.pha_a6
            pha_a7=self.pha_a7
            
            volt_error=self.volt_error*np.random.rand()
            
            cmd='elegant dalian_energy_b3.ele -macro=use_beamline='+self.use_beamline+' '\
            +'-macro=volt_error='+str(volt_error)+' '\
            +'-macro=a2amp='+str(amp_a2)+' '\
            +'-macro=a2pha='+str(pha_a2)+' '\
            +'-macro=a3amp='+str(amp_a3)+' '\
            +'-macro=a3pha='+str(pha_a3)+' '\
            +'-macro=a4amp='+str(amp_a4)+' '\
            +'-macro=a4pha='+str(pha_a4)+' '\
            +'-macro=a5amp='+str(amp_a5)+' '\
            +'-macro=a5pha='+str(pha_a5)+' '\
            +'-macro=a6amp='+str(amp_a6)+' '\
            +'-macro=a6pha='+str(pha_a6)+' '\
            +'-macro=a7amp='+str(amp_a7)+' '\
            +'-macro=a7pha='+str(pha_a7)+' '\
#            +'-rpnDefns=/Users/duan/software/notouch/defns.rpn > log.txt' # only need in MAC OS
#            print cmd
            os.system(cmd)
            
            os.system('sdds2plaindata -noRowCount -parameter=Sx -parameter=Sy -para=Cx -para=Cy \
            -para=pCentral dalian_energy_b3.fin dalian_energy_b3.profile.txt')
            
            self.profile_image=np.loadtxt('dalian_energy_b3.profile.txt')
            
            
        sx=self.profile_image[0]
        sy=self.profile_image[1]
        cx=self.profile_image[2]
        cy=self.profile_image[3]
        energy=self.profile_image[4]*0.511 # in MeV
        

        
        x=np.arange(-1e-2,1e-2,1e-5)
        y=np.arange(-1e-2,1e-2,1e-5)

        
        X, Y = np.meshgrid(x, y)
        
        rou_B_design=self.L_bend/(np.pi/6)
        delta_x=(energy-self.designed_energy)/self.designed_energy*rou_B_design

        cx_new=cx+delta_x
        
        energy_spread=sx/self.designed_etax
        
        Z1 = mlab.bivariate_normal(X, Y, sx, sy,cx_new,cy,(np.random.random()*2-1)*2e-8)
        noise=np.random.random(X.shape)*1e4
        
        Z = Z1+Z1+noise

        self.axes1.imshow(Z,extent=[-1e-2,1e-2,-1e-2,1e-2],origin='lower', 
                        vmax=abs(Z).max(), vmin=-abs(Z).max(),cmap=cm.jet, )
                        
                        
        self.canvas1.draw()
        
        
        self.energy=np.append(self.energy,energy)
        self.energy_spread=np.append(self.energy_spread,energy_spread)
        
        self.axes2.plot(self.energy)
        self.axes3.plot(self.energy_spread)
        self.canvas2.draw()
        
        
        
        
        self.lineEdit_energy.setText(str(energy))
        self.lineEdit_energy_spread.setText(str(energy_spread*100))





    @pyqtSignature("")
    def on_pushButton_default_clicked(self):
        """
        Slot documentation goes here.
        """
        self.amp_a2=40
        self.amp_a3=40
        self.amp_a4=46.5
        self.amp_a5=46.5
        self.amp_a6=46.5
        self.amp_a7=46.5
        
        self.pha_a2=90
        self.pha_a3=90
        self.pha_a4=90
        self.pha_a5=90
        self.pha_a6=90
        self.pha_a7=90
        
        self.lineEdit_pha_a2.setText(str(self.pha_a2))
        self.lineEdit_pha_a3.setText(str(self.pha_a3))
        self.lineEdit_pha_a4.setText(str(self.pha_a4))
        self.lineEdit_pha_a5.setText(str(self.pha_a5))
        self.lineEdit_pha_a6.setText(str(self.pha_a6))
        self.lineEdit_pha_a7.setText(str(self.pha_a7))
        
        self.lineEdit_amp_a2.setText(str(self.amp_a2))
        self.lineEdit_amp_a3.setText(str(self.amp_a3))
        self.lineEdit_amp_a4.setText(str(self.amp_a4))
        self.lineEdit_amp_a5.setText(str(self.amp_a5))
        self.lineEdit_amp_a6.setText(str(self.amp_a6))
        self.lineEdit_amp_a7.setText(str(self.amp_a7))
        
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
        self.horizontalScrollBar_pha_a2.setValue(self.pha_a2)
        
        self.horizontalScrollBar_amp_a2.setValue(self.pha_a2)
        self.horizontalScrollBar_amp_a3.setValue(self.pha_a3)
        self.horizontalScrollBar_amp_a4.setValue(self.pha_a4)
        self.horizontalScrollBar_amp_a5.setValue(self.pha_a5)
        self.horizontalScrollBar_amp_a6.setValue(self.pha_a6)
        self.horizontalScrollBar_amp_a7.setValue(self.pha_a7)
        
        self.pushButton_start.setEnabled(1)
        self.pushButton_pause.setEnabled(1)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
    

