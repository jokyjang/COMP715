import os
import sys
import random
from vtk import *
from PyQt4 import QtCore, QtGui
import numpy as np
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

global window
# Define interaction style
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
        self.year = 1801
        self.month = 1
        self.phase = 0
        self.lon = 0
        self.lat = 0
    
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
        lphase = QtGui.QLabel('phase:', self)
        self.yearLe = QtGui.QLineEdit(str(self.year), self)
        self.monthLe = QtGui.QLineEdit(str(self.month), self)
        self.phaseLe = QtGui.QLineEdit(str(self.phase), self)
        dateHL = QtGui.QHBoxLayout()
        dateHL.addStretch(1)
        dateHL.addWidget(lphase)
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
        self.sld.valueChanged[int].connect(self.sldChangeValue)
        sldHL = QtGui.QHBoxLayout()
        #sldHL.addStretch(1)
        sldHL.addWidget(self.lsld)
        sldHL.addWidget(self.sld)
        #print self.sld.tickInterval()

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
    
    def getDate(self, value):
        year = (value-1) // 12 + 1801
        month = (value-1) % 12 + 1
        return (year, month)
    
    def getVTRFile(self, year, month):
        index = (year - 1801)*12+month-1
        return "%s/sst_%d_0_0.vtr" % (self.inputFileRoot, index)
    
    def setCoror(self, lon, lat):
        lon = int(round(lon/2) * 2)
        lat = int(round(lat/2) * 2)
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
    
    def typeCListner(self, text):
        if (text == 'correlation'):
            self.lsld.setText('Phase:')
            self.yearLe.setEnabled(False)
            self.monthLe.setEnabled(False)
            self.phaseLe.setEnabled(True)
        elif (text == 'magnitude'):
            self.lsld.setText('Time:')
            self.yearLe.setEnabled(True)
            self.monthLe.setEnabled(True)
            self.phaseLe.setEnabled(False)
        elif (text == 'phase'):
            self.lsld.setEnabled(False)
            self.lsld.setText('Phase:')
            self.yearLe.setEnabled(False)
            self.monthLe.setEnabled(False)
            self.phaseLe.setEnabled(False)
    
    def importListner(self):
        #inputFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~/')
        inputFileName = '/Users/zhangzhx/Dropbox/Homework/VisSci/HW1/Data/sst_1_0_0.vtr'
        self.inputFileRoot = inputFileName[:str(inputFileName).rfind('/')]
        self.sstArray = self.loadAllVTRFiles('sst')
        self.anomArray = self.loadAllVTRFiles('anom')
        self.drawBn.setEnabled(True)
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
            dataArray = self.sstArray if self.data == 'sst' else self.anomArray
            index = self.getIndexFromCoror(self.lon, self.lat)
            corr = self.calculateCorr(dataArray, index)
            self.drawCorr(corr)
        elif self.type == 'phase':
            dataArray = self.sstArray if self.data == 'sst' else self.anomArray
            index = self.getIndexFromCoror(self.lon, self.lat)
            (phase, corr) = self.calculatePhase(dataArray, index)
            self.drawPhase(phase, corr)
            
    def calculateCorr(self, dataArray, index):
        size = dataArray.shape[1]
        corr = [0 for i in xrange(size)]
        for i in xrange(size):
            if (dataArray[0][i] < -900):
                corr[i] = dataArray[0][i]
            else:
                corr[i] = np.corrcoef(dataArray[:,i], dataArray[:,index])[0][1]
        return np.array(corr)
    
    def calculatePhase(self, dataArray, index):
        size = dataArray.shape[1]
        phase = [0 for i in xrange(size)]
        corr = [0 for i in xrange(size)]
        for i in xrange(size):
            if (dataArray[0][i] < -900):
                phase[i] = corr[i] = dataArray[0][i]
            else:
                phase[i] = random.random() * 2 - 1
                corr[i] = random.random() * 2 - 1
        return (phase, corr)
    
    def loadAllVTRFiles(self, data):
        dataArray = []
        for y in range(1901, 1911):
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
    def get_phase_color_map(self, phase):
        
        transFunction = vtkDiscretizableColorTransferFunction()
        transFunction.SetNumberOfValues(8)
        transFunction.DiscretizeOn()
        transFunction.AddRGBPoint(-1.0, 1, 1, 1)
        transFunction.AddRGBPoint(-0.6, 0.902, 0.902, 0)
        transFunction.AddRGBPoint(-0.757979, 0.9294, 0.9294, 0.2862)
        #transFunction.AddRGBPoint(-0.488299, 236, 236, 59)
        #transFunction.AddRGBPoint(0, 230, 0, 0)
        #transFunction.AddRGBPoint(0.244677, 164, 0 , 0)
        transFunction.AddRGBPoint(0.2, 0.902,0,0)
        transFunction.AddRGBPoint(1.0, 0, 0, 0)

        scalarBar = vtkScalarBarActor()
        #scalarBar.SetLookupTable(colorLookupTable)
        scalarBar.SetLookupTable(transFunction)
        self.ren.AddActor2D(scalarBar)
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
       
        #print '#no of tuples:', dataset.GetNumberOfTuples()
        for i in range(len(phase)):
            p = phase[i]
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
    
    def clone_data(self, dataset):

        calc = vtkArrayCalculator()
        calc.SetInputData(dataset)
        #calc.AddScalarArrayName("ampanomfil")
        #calc.SetFunction("ampanomfil");
        #calc.SetResultArrayName("clone");
        calc.Update();
        
        return calc.GetOutput()
    
    def get_opacity_value(self, value, no_of_bands):
        temp = (((value - self.amp_min) // (self.amp_max-self.amp_min)) + 1 ) * (255/no_of_bands)

        return (255-temp)
    
    def get_amp_color_map(self, corr):

        '''
        transFunction = vtkDiscretizableColorTransferFunction()
        transFunction.SetNumberOfValues(8)
        transFunction.DiscretizeOn()
        transFunction.EnableOpacityMappingOn()
        transFunction.AddRGBPoint(-1.0, 1, 1, 1)
        #transFunction.AddRGBPoint(-0.6, 0.902, 0.902, 0)
        #transFunction.AddRGBPoint(-0.757979, 0.9294, 0.9294, 0.2862)
        #transFunction.AddRGBPoint(-0.488299, 236, 236, 59)
        #transFunction.AddRGBPoint(0, 230, 0, 0)
        #transFunction.AddRGBPoint(0.244677, 164, 0 , 0)
        #transFunction.AddRGBPoint(0.2, 0.902,0,0)
        transFunction.AddRGBPoint(1.0, 1, 1, 1)
        '''
        #(minv, maxv) = dataset.GetRange()
        (minv, maxv) = (-1, 1)
        self.amp_min = minv
        self.amp_max = maxv
       
        print "minv#, maxv#",  minv, maxv       
        #scalarBar = vtkScalarBarActor()
        #scalarBar.SetLookupTable(colorLookupTable)
        #scalarBar.SetLookupTable(transFunction)
        #self.ren.AddActor2D(scalarBar)
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(4)
        colors.SetName("Colors")
       
        for i in range(len(corr)):
            p = corr[i]
            color = [0 for i in range(4)]
            color[0] = 255
            color[1] = 255
            color[2] = 255
            color[3] = 255
            if p >= -1:  
                color[3] = int(round(self.get_opacity_value(p, 16)))

            colors.InsertNextTupleValue(color)

        return colors
    
    def drawPhase(self, phase, corr):
       
        (minz, maxz) = (-1, 1)
        #print minz, maxz
       
        colors = self.get_phase_color_map(phase)
        self.dataSet.GetPointData().SetScalars(colors)
        
        # Create a mapper
        mapper = vtkDataSetMapper()
        #mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetInputData(self.dataSet)
        mapper.ScalarVisibilityOn()
        #mapper.SetInputData(sstData)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
 
        #amplitude part starts here
        
        clone = self.clone_data(self.dataSet)
        #clone = self.slice_data(clone, 'ampanomfil', -1, 1)
        #amplData = clone.GetPointData().GetArray('ampanomfil')


        colors1 = self.get_amp_color_map(corr)
        clone.GetPointData().SetScalars(colors1)

        ampMapper = vtkDataSetMapper()
        ampMapper.SetInputData(clone)
        ampMapper.ScalarVisibilityOn()

        actor2 = vtkActor()
        actor2.SetMapper(ampMapper)
        #actor2.GetProperty().SetOpacity(0.995);

        self.ren.AddActor(actor)
        self.ren.AddActor(actor2)
        self.ren.ResetCamera()
        #self.show()
        
        self.iren.Initialize()
    
    def drawCorr(self, array):
        
        #pd = self.dataSet.GetPointData()
        #numOfArrays = pd.GetNumberOfArrays()
        #dataset = pd.GetArray(str(self.data))
        #print dataset.__class__
        #for i in range(numOfArrays):
        #    print pd.GetArrayName(i)
        
        #print dataset.GetSize()
        #print dataset.GetValue(16000)
        #print dataset.GetElementComponentSize()
        #print dataset.PrintSelf(0)
        (minz, maxz) = (-1, 1)#dataset.GetRange()
        #print minz, maxz
        
        # Create the color map
        colorLookupTable = vtkLookupTable()
        colorLookupTable.SetTableRange(minz, maxz)
        colorLookupTable.Build()
        
        # Generate the colors for each point based on the color map
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        
        for i in range(self.dataSet.GetNumberOfPoints()):
            p = array[i]
            
            dcolor = [0 for i in range(3)]
            colorLookupTable.GetColor(p, dcolor)
            
            color = [0 for i in range(3)]
            for j in range(3):
                color[j] = int(255.0 * dcolor[j])
            
            colors.InsertNextTupleValue(color)
        
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
    
    def drawVTR(self, inputFileName):
        reader = vtkXMLRectilinearGridReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        
        reader.GetOutput().Register(reader)
        self.dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())
        '''
        numOfCells = dataSet.GetNumberOfCells()
        numOfPoints = dataSet.GetNumberOfPoints()
        print dataSet.GetClassName()
        print '# of cells:', numOfCells
        print '# of points:', numOfPoints
        '''
        
        pd = self.dataSet.GetPointData()
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
        
        for i in range(self.dataSet.GetNumberOfPoints()):
            p = dataset.GetValue(i)
            
            dcolor = [0 for i in range(3)]
            colorLookupTable.GetColor(p, dcolor)
            
            color = [0 for i in range(3)]
            for j in range(3):
                color[j] = int(255.0 * dcolor[j])
            
            colors.InsertNextTupleValue(color)
        
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
        
    def initVTK(self):
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.SetInteractorStyle(MouseInteractorStylePP(self))
        
    def sldChangeValue(self, value):
        (self.year, self.month) = self.getDate(value)
        self.yearLe.setText(str(self.year))
        self.monthLe.setText(str(self.month))
        self.drawListner()
        #inputFileName = self.getVTRFile(self.year, self.month)
        #self.drawVTR(inputFileName)

#def doYouKnowWindow():
#    print window.__class__

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())