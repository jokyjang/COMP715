import os
import sys
import random
import time
from vtk import *
from PyQt4 import QtCore, QtGui
import math
import numpy as np
from scipy import signal
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

global window

class MouseInteractorStylePP(vtkInteractorStyleTrackballCamera):
    
    def __init__(self, o):
        self.AddObserver('LeftButtonPressEvent', self.OnLeftButtonDown)

    def OnLeftButtonDown(self, obj, event):
        self.GetInteractor().GetPicker().Pick(self.GetInteractor().GetEventPosition()[0], \
            self.GetInteractor().GetEventPosition()[1], 0, \
            self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer())
        picked = self.GetInteractor().GetPicker().GetPickPosition()
        self.x = picked[0]
        self.y = picked[1]
        window.setCoror(picked[0], picked[1])

class MainWindow(QtGui.QWidget):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.initSetting()
        self.initUI()
        self.initVTK()
        self.show()
        
    def initSetting(self):
        self.sstArray = None
        self.anomArray = None
        self.data = 'sst'
        self.type = 'magnitude'
        self.year = 1854
        self.month = 1
        self.phase = 0
        self.lon = 0
        self.lat = 0
    def getIndexFromCoror(self, lon, lat):
        return lon/2+(lat+88)/2*89    
    def initUI(self):
        left = QtGui.QFrame(self)
        
        self.importBn = QtGui.QPushButton("Import", self)
        self.importBn.clicked.connect(self.importListner)
        self.exportBn = QtGui.QPushButton("Export", self)
        self.saveBn = QtGui.QPushButton("SaveAs", self)
        self.drawBn = QtGui.QPushButton("Draw", self)
        self.drawBn.clicked.connect(self.drawListner)
        
        ldata = QtGui.QLabel("dataset", self)
        self.dataC = QtGui.QComboBox(self)
        self.dataC.addItem("sst")
        self.dataC.addItem("anom")
        ltype = QtGui.QLabel("draw", self)
        
        self.typeC = QtGui.QComboBox(self)
        self.typeC.addItem("magnitude")
        self.typeC.addItem("correlation")
        self.typeC.addItem("phase")
        self.typeC.activated[str].connect(self.typeCListner)
        dataHL = QtGui.QHBoxLayout()
        dataHL.addStretch(1)
        dataHL.addWidget(ltype)
        dataHL.addWidget(self.typeC)
        dataHL.addWidget(ldata)
        dataHL.addWidget(self.dataC)
        
        lyear = QtGui.QLabel('year:', self)
        lmonth = QtGui.QLabel('month:', self)
        self.lphase = QtGui.QLabel('phase:', self)
        self.yearLe = QtGui.QLineEdit(str(self.year), self)
        self.monthLe = QtGui.QLineEdit(str(self.month), self)
        self.phaseLe = QtGui.QLineEdit(str(self.phase), self)
        dateHL = QtGui.QHBoxLayout()
        dateHL.addStretch(1)
        dateHL.addWidget(self.lphase)
        dateHL.addWidget(self.phaseLe)
        dateHL.addWidget(lyear)
        dateHL.addWidget(self.yearLe)
        dateHL.addWidget(lmonth)
        dateHL.addWidget(self.monthLe)
        
        llat = QtGui.QLabel('Lat.:', self)
        llon = QtGui.QLabel('Lon.:', self)
        self.lonLe = QtGui.QLineEdit(str(self.lon), self)
        self.latLe = QtGui.QLineEdit(str(self.lat), self)
        cororHL = QtGui.QHBoxLayout()
        cororHL.addStretch(1)
        cororHL.addWidget(llon)
        cororHL.addWidget(self.lonLe)
        cororHL.addWidget(llat)
        cororHL.addWidget(self.latLe)
        
        self.lsld = QtGui.QLabel('Time:', self)
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setRange(1, 1920)
        self.sld.valueChanged[int].connect(self.sldListner)
        sldHL = QtGui.QHBoxLayout()
        #sldHL.addStretch(1)
        sldHL.addWidget(self.lsld)
        sldHL.addWidget(self.sld)

        vl = QtGui.QVBoxLayout()
        vl.addStretch(1)
        vl.addWidget(self.importBn)
        vl.addWidget(self.exportBn)
        vl.addWidget(self.saveBn)
        vl.addLayout(dataHL)
        vl.addLayout(dateHL)
        vl.addLayout(sldHL)
        vl.addLayout(cororHL)
        vl.addWidget(self.drawBn)
        left.setLayout(vl)
        left.setFrameShape(QtGui.QFrame.StyledPanel)
        
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)        
        self.vl = QtGui.QVBoxLayout()
        self.frame.setLayout(self.vl)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(self.frame)

        vbox = QtGui.QHBoxLayout()
        vbox.addWidget(splitter)
        self.setLayout(vbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Visualization in Science')
        
        self.lsld.setText('Time:')
        self.yearLe.setEnabled(False)
        self.monthLe.setEnabled(False)
        self.phaseLe.setEnabled(False)
        self.latLe.setEnabled(False)
        self.lonLe.setEnabled(False)
        self.drawBn.setEnabled(False)
        self.sld.setEnabled(False)
    def initVTK(self):
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.SetInteractorStyle(MouseInteractorStylePP(self))     
    def setCoror(self, lon, lat):
        lon = int(round(lon/2) * 2)
        lat = int(round(lat/2) * 2)
        self.lonLe.setText(str(lon))
        self.latLe.setText(str(lat))
    def importListner(self):
        #inputFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~/')
        inputFileName = '/Users/zhangzhx/Dropbox/Homework/VisSci/HW1/Data/sst_1_0_0.vtr'
        self.inputFileRoot = inputFileName[:str(inputFileName).rfind('/')]
        self.sstArray = self.loadAllVTRFiles('sst')
        self.anomArray = self.loadAllVTRFiles('anom')
        self.drawBn.setEnabled(True)
        self.drawVTR(inputFileName)
        self.yearLe.setEnabled(True)
        self.monthLe.setEnabled(True)
        self.sld.setEnabled(True)
    def drawListner(self):
        self.type = self.typeC.itemText(self.typeC.currentIndex())
        self.data = self.dataC.itemText(self.dataC.currentIndex())
        self.year = int(self.yearLe.text())
        self.month = int(self.monthLe.text())
        self.lon = int(self.lonLe.text())
        self.lat = int(self.latLe.text())
        self.phase = float(self.phaseLe.text())
        if self.type == 'magnitude':
            inputFileName = self.getVTRFile(self.year, self.month)
            self.drawVTR(inputFileName)
        elif self.type == 'correlation':
            dataArray = self.sstArray if self.data == 'sst' else self.anomArray
            index = self.getIndexFromCoror(self.lon, self.lat)
            corr = self.calculateCorr(dataArray, index, self.phase)
            self.drawCorr(corr)
        #elif self.type == 'phase':
        #    dataArray = self.sstArray if self.data == 'sst' else self.anomArray
        #    index = self.getIndexFromCoror(self.lon, self.lat)
        #    (phase, corr) = self.calculatePhase(dataArray, index, int(self.phase))
        #    self.drawPhase(phase, corr)
    
    def typeCListner(self, text):
        if (text == 'correlation'):
            self.lsld.setText('Phase:')
            self.yearLe.setEnabled(False)
            self.monthLe.setEnabled(False)
            self.phaseLe.setEnabled(True)
            self.latLe.setEnabled(True)
            self.lonLe.setEnabled(True)
        elif (text == 'magnitude'):
            self.lsld.setText('Time:')
            self.yearLe.setEnabled(True)
            self.monthLe.setEnabled(True)
            self.phaseLe.setEnabled(False)
            self.latLe.setEnabled(False)
            self.lonLe.setEnabled(False)
        elif (text == 'phase'):
            self.lphase.setText('# of phases:')
            self.lsld.setText('# of phases:')
            self.yearLe.setEnabled(False)
            self.monthLe.setEnabled(False)
            self.phaseLe.setEnabled(True)
            self.latLe.setEnabled(True)
            self.lonLe.setEnabled(True)

    def sldListner(self, value):
        if (self.type == 'magnitude'):
            (self.year, self.month) = self.getDate(value)
            self.yearLe.setText(str(self.year))
            self.monthLe.setText(str(self.month))
            self.drawListner()
        elif (self.type == 'correlation'):
            self.phase = self.getPhase(value)
            self.phaseLe.setText('%.2f' % self.phase)
            self.drawListner()
    def getDate(self, value):
        year = (value-1) // 12 + 1854
        month = (value-1) % 12 + 1
        return (year, month)
    def getVTRFile(self, year, month):
        index = (year - 1854)*12+month-1
        return "%s/sst_%d_0_0.vtr" % (self.inputFileRoot, index)
    
    def loadVTRFile(self, inputFileName, data):
        reader = vtkXMLRectilinearGridReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        
        reader.GetOutput().Register(reader)
        dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())
        pd = dataSet.GetPointData()
        dataset = pd.GetArray(str(data))
        dataArray = [dataset.GetValue(i) for i in range(dataset.GetSize())]
        return dataArray
    
    def loadAllVTRFiles(self, data):
        dataArray = []
        for y in range(2000, 2014):
            for m in range(1, 13):
                inputFileName = self.getVTRFile(y, m)
                if not os.path.exists(inputFileName):
                    print inputFileName, 'does not exist'
                dataArray.append(self.loadVTRFile(inputFileName, data))
        return np.array(dataArray)
    
    def get_vtr_color_map(self, dataset):
        #print phase
        minz, maxz = dataset.GetRange()
        minz = -180
        print minz, maxz
        transFunction = vtkColorTransferFunction()
        #transFunction.SetNumberOfValues(8)
        #transFunction.DiscretizeOn()
        transFunction.AddRGBPoint(minz, 59.0/255, 76.0/255, 192.0/255)
        transFunction.AddRGBPoint((maxz-minz)/2.0, 221.0/255, 221.0/255, 221.0/255)
        transFunction.AddRGBPoint(maxz, 180.0/255, 4.0/255, 38.0/255)

        scalarBar = vtkScalarBarActor()
        #scalarBar.SetLookupTable(colorLookupTable)
        scalarBar.SetLookupTable(transFunction)
        self.ren.AddActor2D(scalarBar)
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
       
        #print '#no of tuples:', dataset.GetNumberOfTuples()
        for i in range(dataset.GetNumberOfTuples()):
            p = dataset.GetValue(i)
            color = [0 for i in range(3)]
            if p >= minz:  
                dcolor = [0 for i in range(3)]
                transFunction.GetColor(p, dcolor)
                for j in range(3):
                    color[j] = int(255.0 * dcolor[j])
            else:
                color[0] = 0
                color[1] = 0
                color[2] = 0

            colors.InsertNextTupleValue(color)
        return colors
    
    def get_color(self, dataset):
        # Create the color map
        (minz, maxz) = dataset.GetRange()
        colorLookupTable = vtkLookupTable()
        colorLookupTable.SetTableRange(minz, maxz)
        colorLookupTable.Build()
        
        # Generate the colors for each point based on the color map
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        
        for i in range(self.dataSet.GetNumberOfPoints()):
            p = dataset.GetValue(i)
            dcolor = [0 for i in range(3)]
            colorLookupTable.GetColor(p, dcolor)
            color = [0 for i in range(3)]
            for j in range(3):
                color[j] = int(255.0 * dcolor[j])
            colors.InsertNextTupleValue(color)
        return colors
    
    def drawVTR(self, inputFileName):
        reader = vtkXMLRectilinearGridReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        
        reader.GetOutput().Register(reader)
        self.dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())
        pd = self.dataSet.GetPointData()
        dataset = pd.GetArray(str(self.data))
        colors = self.get_vtr_color_map(dataset)
        #colors = self.get_color(dataset)
        self.dataSet.GetPointData().SetScalars(colors)
        
        # Create a mapper
        mapper = vtkDataSetMapper()
        mapper.SetInputData(self.dataSet)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.iren.Initialize()
    def get_corr_color_map(self, corr):
        #print phase
        transFunction = vtkDiscretizableColorTransferFunction()
        transFunction.SetNumberOfValues(10)
        transFunction.DiscretizeOn()
        transFunction.AddRGBPoint(-0.45, 59.0/255, 76.0/255, 192.0/255)
        #transFunction.AddRGBPoint(-0.757979, 0.9294, 0.9294, 0.2862)
        #transFunction.AddRGBPoint(-0.6, 0.902, 0.902, 0)
        transFunction.AddRGBPoint(-0.0485353, 206.0/255, 217.0/255, 236.0/255)
        transFunction.AddRGBPoint(0.0420639, 234.0/255, 212.0/255, 200.0/255)
        #transFunction.AddRGBPoint(0.244677, 164/255.0, 0 , 0)
        #transFunction.AddRGBPoint(0.2, 0.902,0,0)
        transFunction.AddRGBPoint(0.45, 180.0/255, 4.0/255, 38.0/255)

        scalarBar = vtkScalarBarActor()
        #scalarBar.SetLookupTable(colorLookupTable)
        scalarBar.SetLookupTable(transFunction)
        self.ren.AddActor2D(scalarBar)
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
       
        #print '#no of tuples:', dataset.GetNumberOfTuples()
        for i in range(len(corr)):
            p = corr[i]
            color = [0 for i in range(3)]
            if p >= -1:  
                dcolor = [0 for i in range(3)]
                #colorLookupTable.GetColor(p, dcolor)
                transFunction.GetColor(p, dcolor)
                for j in range(3):
                    color[j] = int(255.0 * dcolor[j])
            else:
                color[0] = 0
                color[1] = 0
                color[2] = 255

            colors.InsertNextTupleValue(color)
        return colors
    def phshift(self, y, pd):
        ymean=np.mean(y)
        my = [i-ymean for i in y]
        hy = signal.hilbert(my)
        my = [abs(i)*math.cos((pd*np.pi)+np.arctan(i.imag/i.real)) for i in hy]
        #my=abs(hy)*cos( (pd*pi) + (Arg(hy)) )
        my = [i+ymean for i in my]
        return my
    
    # too slower than the default numpy version
    def corrcoef(self, x, y):
        ux = np.mean(x)
        uy = np.mean(y)
        sx = [i-ux for i in x]
        sy = [i-uy for i in y]
        covA = [sx[i]*sy[i] for i in range(len(x))]
        vx = [sx[i]*sx[i] for i in range(len(x))]
        vy = [sy[i]*sy[i] for i in range(len(y))]
        return sum(covA)/(math.sqrt(sum(vx)*sum(vy)))
    def calculateCorr(self, dataArray, index, phase):
        #time1 = time.time()
        size = dataArray.shape[1]
        corr = [0 for i in xrange(size)]
        array = self.phshift(dataArray[:,index], phase)
        for i in xrange(size):
            if (dataArray[0][i] < -900):
                corr[i] = dataArray[0][i]
            else:
                corr[i] = np.corrcoef(dataArray[:,i], array)[0][1]
                #corr[i] = self.corrcoef(dataArray[:,i], array)
        return np.array(corr)
    def drawCorr(self, array):
        colors = self.get_corr_color_map(array)
        self.dataSet.GetPointData().SetScalars(colors)
        # Create a mapper
        mapper = vtkDataSetMapper()
        mapper.SetInputData(self.dataSet)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.iren.Initialize()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())