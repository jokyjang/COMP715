import os
import sys
from vtk import *
from PyQt4 import QtCore, QtGui
import numpy as np
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

global window
# Define interaction style
class MouseInteractorStylePP(vtkInteractorStyleTrackballCamera):
    
    def __init__(self, o):
        #MouseInteractorStylePP.outer = o
        #self.aV = 1
        #print self.outer.month
        self.AddObserver('LeftButtonPressEvent', self.OnLeftButtonDown)
        #self.outer.setCoror(3, 4)
    
    def GetOuter(self):
        return self.outer
    def setCoror(self, lon, lat):
        print self.outer.month
    def OnLeftButtonDown(self, obj, event):
        self.GetInteractor().GetPicker().Pick(self.GetInteractor().GetEventPosition()[0], \
            self.GetInteractor().GetEventPosition()[1], 0, \
            self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer())
        picked = self.GetInteractor().GetPicker().GetPickPosition()
        print "Picked value:",  picked[0], picked[1], picked[2]
        #self.setCoror(3, 4)
        self.x = picked[0]
        self.y = picked[1]
        #print 'av', self.aV
    
        #print self.outer.__class__
        window.setCoror(picked[0], picked[1])

class MainWindow(QtGui.QWidget):
 
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.initSetting()
        self.initUI()
        self.initVTK()
        self.show()
        
    def someMethod(self):
        print 'hello world'
    
    def initSetting(self):
        self.sstArray = None
        self.anomArray = None
    
    def initUI(self):
        
        left = QtGui.QFrame(self)
        
        self.importBn = QtGui.QPushButton("Import", self)
        self.importBn.clicked.connect(self.importListner)
        #self.importBn.clicked.connect(self.load_nc_file)
        self.exportBn = QtGui.QPushButton("Export", self)
        self.saveBn = QtGui.QPushButton("SaveAs", self)
        self.drawBn = QtGui.QPushButton("Draw", self)
        self.drawBn.clicked.connect(self.drawListner)
        
        ldata = QtGui.QLabel("dataset", self)
        self.data = 'sst'
        self.dataC = QtGui.QComboBox(self)
        self.dataC.addItem("sst")
        self.dataC.addItem("anom")
        ltype = QtGui.QLabel("draw", self)
        self.type = 'magnitude'
        self.typeC = QtGui.QComboBox(self)
        self.typeC.addItem("magnitude")
        self.typeC.addItem("correlation")
        #self.dataC.activated[str].connect(self.dataCListner)
        dataHL = QtGui.QHBoxLayout()
        dataHL.addStretch(1)
        dataHL.addWidget(ltype)
        dataHL.addWidget(self.typeC)
        dataHL.addWidget(ldata)
        dataHL.addWidget(self.dataC)
        
        lyear = QtGui.QLabel('year:', self)
        lmonth = QtGui.QLabel('month:', self)
        self.year = 1801
        self.month = 1
        self.yearLe = QtGui.QLineEdit(str(self.year), self)
        self.monthLe = QtGui.QLineEdit(str(self.month), self)
        dateHL = QtGui.QHBoxLayout()
        dateHL.addStretch(1)
        dateHL.addWidget(lyear)
        dateHL.addWidget(self.yearLe)
        dateHL.addWidget(lmonth)
        dateHL.addWidget(self.monthLe)
        
        llat = QtGui.QLabel('Lat.:', self)
        llon = QtGui.QLabel('Lon.:', self)
        self.lon = 0
        self.lat = 0
        self.lonLe = QtGui.QLineEdit(str(self.lon), self)
        self.latLe = QtGui.QLineEdit(str(self.lat), self)
        cororHL = QtGui.QHBoxLayout()
        cororHL.addStretch(1)
        cororHL.addWidget(llon)
        cororHL.addWidget(self.lonLe)
        cororHL.addWidget(llat)
        cororHL.addWidget(self.latLe)
        
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.valueChanged[int].connect(self.sldChangeValue)
        self.sld.setRange(1, 1920)
        #print self.sld.tickInterval()

        vl = QtGui.QVBoxLayout()
        vl.addStretch(1)
        vl.addWidget(self.importBn)
        vl.addWidget(self.exportBn)
        vl.addWidget(self.saveBn)
        vl.addLayout(dataHL)
        vl.addLayout(dateHL)
        vl.addWidget(self.sld)
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
    
    def getDate(self, value):
        year = (value-1) // 12 + 1801
        month = (value-1) % 12 + 1
        return (year, month)
    
    def getVTRFile(self, year, month):
        index = (year - 1801)*12+month-1
        return "%s/sst_%d_0_0.vtr" % (self.inputFileRoot, index)
    
    def setCoror(self, lon, lat):
        self.lonLe.setText(str(lon))
        self.latLe.setText(str(lat))

    '''
    TODO: implement this method later if possible
    def load_nc_file(self):
        
        #inputFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~/')
        inputFileName = '/Users/zhangzhx/Dropbox/Homework/VisSci/HW1/SST_Xiao.nc'
        reader = vtkNetCDFReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        #print reader.GetFileName()
        print reader.GetNumberOfVariableArrays()
        #for i in range(reader.GetNumberOfVariableArrays()):
        #    print 'Variable array name:', reader.GetVariableArrayName(i)
        #    print 'time unit:', reader.GetTimeUnits()
        #    print 'status:', reader.GetVariableArrayStatus(reader.GetVariableArrayName(i))
        #    print 'dimension:', reader.GetVariableDimensions().GetValue(i)
        
        readOut = reader.GetOutput()
        print readOut.__class__
        vtkpd = readOut.GetPointData()
        vtkfd = readOut.GetFieldData()
        
        
        #print readOut.__class__
        #print readOut
        #dimens = reader.GetAllDimensions()
        #print dimens.__class__
        
        reader.GetOutput().Register(reader)
        #print readOut
        dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())
    
        numOfCells = dataSet.GetNumberOfCells()
        numOfPoints = dataSet.GetNumberOfPoints()
        #print dataSet.GetClassName()
        #print '# of cells:', numOfCells
        print '# of points:', numOfPoints
        
        pd = dataSet.GetPointData()
        numOfArrays = pd.GetNumberOfArrays()
        dataset = pd.GetArray('sst')
        #print dataset.__class__
        for i in range(numOfArrays):
            print pd.GetArrayName(i)
        
        print dataset.GetSize()
        print dataset.GetValue(16000)
        #print dataset.GetElementComponentSize()
        #print dataset.PrintSelf(0)
        #(minz, maxz) = dataset.GetRange()
        #print minz, maxz
    '''
        
    def importListner(self):
        #inputFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~/')
        inputFileName = '/Users/zhangzhx/Dropbox/Homework/VisSci/HW1/Data/sst_1_0_0.vtr'
        self.inputFileRoot = inputFileName[:str(inputFileName).rfind('/')]
        self.drawVTR(inputFileName)
    
    def getIndexFromCoror(self, lon, lat):
        return lon/2+(lat+88)/2*89
    
    def drawListner(self):
        self.type = self.typeC.itemText(self.typeC.currentIndex())
        self.data = self.dataC.itemText(self.dataC.currentIndex())
        self.year = int(self.yearLe.text())
        self.month = int(self.monthLe.text())
        self.lon = int(self.lonLe.text())
        self.lat = int(self.latLe.text())
        if self.type == 'magnitude':
            inputFileName = self.getVTRFile(self.year, self.month)
            self.drawVTR(inputFileName)
        elif self.type == 'correlation':
            if (self.sstArray == None and self.data == 'sst'):
                self.sstArray = self.loadAllVTRFiles(self.data)
                print self.sstArray.shape
            elif (self.anomArray == None and self.data == 'anom'):
                self.anomArray = self.loadAllVTRFiles(self.data)
                print self.anomArray.shape
            dataArray = self.sstArray if self.data == 'sst' else self.anomArray
            index = self.getIndexFromCoror(self.lon, self.lat)
            corr = self.calculateCorr(dataArray, index)
            self.drawArray(corr)
            
    def calculateCorr(self, dataArray, index):
        corr = np.zeros(dataArray.shape[1])
        for i in range(dataArray.shape[1]):
            corr[i] = (np.mean(dataArray[:,i]) + np.mean(dataArray[:,index]))/2
        return corr
    
    def loadAllVTRFiles(self, data):
        dataArray = []
        for y in range(1901, 1961):
            for m in range(1, 13):
                inputFileName = self.getVTRFile(y, m)
                if not os.path.exists(inputFileName):
                    print inputFileName, 'does not exist'
                dataArray.append(self.loadVTRFile(inputFileName, data))
        return np.array(dataArray)
    
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
    
    #TODO
    def drawArray(self, array):
        pass
    
    def drawVTR(self, inputFileName):
        reader = vtkXMLRectilinearGridReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        
        reader.GetOutput().Register(reader)
        dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())
        '''
        numOfCells = dataSet.GetNumberOfCells()
        numOfPoints = dataSet.GetNumberOfPoints()
        print dataSet.GetClassName()
        print '# of cells:', numOfCells
        print '# of points:', numOfPoints
        '''
        
        pd = dataSet.GetPointData()
        #numOfArrays = pd.GetNumberOfArrays()
        dataset = pd.GetArray(str(self.data))
        #print dataset.__class__
        #for i in range(numOfArrays):
        #    print pd.GetArrayName(i)
        
        #print dataset.GetSize()
        #print dataset.GetValue(16000)
        #print dataset.GetElementComponentSize()
        #print dataset.PrintSelf(0)
        (minz, maxz) = dataset.GetRange()
        #print minz, maxz
        
        # Create the color map
        colorLookupTable = vtkLookupTable()
        colorLookupTable.SetTableRange(minz, maxz)
        colorLookupTable.Build()
        
        # Generate the colors for each point based on the color map
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        
        for i in range(dataSet.GetNumberOfPoints()):
            p = dataset.GetValue(i)
            
            dcolor = [0 for i in range(3)]
            colorLookupTable.GetColor(p, dcolor)
            
            color = [0 for i in range(3)]
            for j in range(3):
                color[j] = int(255.0 * dcolor[j])
            
            colors.InsertNextTupleValue(color)
        
        dataSet.GetPointData().SetScalars(colors)
        
        # Create a mapper
        mapper = vtkDataSetMapper()
        mapper.SetInputData(dataSet)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.iren.Initialize()
        
    def initVTK(self):
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.SetInteractorStyle(MouseInteractorStylePP(self))
        
    def sldChangeValue(self, value):
        (self.year, self.month) = self.getDate(value)
        #self.yearLe.setText(self.year)
        #self.monthLe.setText(self.month)
        #inputFileName = self.getVTRFile(self.year, self.month)
        #self.drawVTR(inputFileName)

#def doYouKnowWindow():
#    print window.__class__

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())