#!/usr/bin/python
import sys
from vtk import *
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(QtGui.QWidget):
 
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.initUI()
        self.initVTK()
        self.show()
        
    def initUI(self):
        
        left = QtGui.QFrame(self)
        
        self.importBn = QtGui.QPushButton("Import", self)
        self.importBn.clicked.connect(self.load_vtr_file)
        self.exportBn = QtGui.QPushButton("Export", self)
        self.saveBn = QtGui.QPushButton("SaveAs", self)
        self.drawBn = QtGui.QPushButton("Draw", self)
        self.drawBn.clicked.connect(self.draw_graph)
        
        hl = QtGui.QHBoxLayout()
        lyear = QtGui.QLabel('year:', self)
        self.yearLe = QtGui.QLineEdit('1800', self)
        lmonth = QtGui.QLabel('month:', self)
        self.monthLe = QtGui.QLineEdit('1', self)
        self.year = 1800
        self.month = 1
        hl.addStretch(1)
        hl.addWidget(lyear)
        hl.addWidget(self.yearLe)
        hl.addWidget(lmonth)
        hl.addWidget(self.monthLe)

        vl = QtGui.QVBoxLayout()
        vl.addStretch(1)
        vl.addWidget(self.importBn)
        vl.addWidget(self.exportBn)
        vl.addWidget(self.saveBn)
        vl.addLayout(hl)
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
        
        self.setGeometry(1200, 800, 800, 600)
        
        self.setWindowTitle('Visualization in Science')
        #self.show()
    
    def get_vtr_file(self):
        
        root = '/home/rajesh/Documents/UNC/4th sem/visualization/HWs/Project/data'
        #index = (self.year - 1800)*12+self.month
        index = 0
        return "%s/test/test_%d_0.vtr" % (root, index)
    
    def load_vtr_file(self):
        
        #inputFileName = self.get_vtr_file()
        inputFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~/')
        #inputFileName = '/Users/zhangzhx/Dropbox/Homework/VisSci/HW1/Data/sst_1/sst_1_0_0.vtr'
        self.draw_graph_from_file(inputFileName)
        
    def draw_graph(self):
        self.year = int(self.yearLe.text())
        self.month = int(self.monthLe.text())
        inputFileName = self.get_vtr_file()
        self.draw_graph_from_file(inputFileName)

    def slice_data(self, dataset, arrayName, lower, upper):

        dataset.GetPointData().SetActiveScalars(arrayName)
        thresholdFilter = vtkThresholdPoints()
        thresholdFilter.ThresholdBetween(lower, upper)
        thresholdFilter.SetInput(dataset)
        thresholdFilter.Update()

        return thresholdFilter.GetOutput()

    def get_phase_color_map(self, dataset):
        
        print 'hi'

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
       
        print '#no of tuples:', dataset.GetNumberOfTuples()
        for i in range(dataset.GetNumberOfTuples()):
            p = dataset.GetValue(i)
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

    def get_opacity_value(self, value, no_of_bands):
        temp = (((value - self.amp_min) // (self.amp_max-self.amp_min)) + 1 ) * (255/no_of_bands)

        return (255-temp)

    def get_amp_color_map(self, dataset):

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
        (minv, maxv) = dataset.GetRange()
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
       
        for i in range(dataset.GetNumberOfTuples()):
            p = dataset.GetValue(i)
            color = [0 for i in range(4)]
            color[0] = 255
            color[1] = 255
            color[2] = 255
            color[3] = 255
            if p >= -1:  
                color[3] = self.get_opacity_value(p, 16)

            colors.InsertNextTupleValue(color)

        return colors

    def clone_data(self, dataset):

        calc = vtkArrayCalculator()
        calc.SetInput(dataset)
        calc.AddScalarArrayName("ampanomfil")
        calc.SetFunction("ampanomfil");
        calc.SetResultArrayName("clone");
        calc.Update();
        
        return calc.GetOutput()
        
    def draw_graph_from_file(self, inputFileName):
        
        print inputFileName
        reader = vtkXMLRectilinearGridReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        
        #returns a rectilinear grid
        reader.GetOutput().Register(reader)
        #typecasting to a more general class vtkDataSet
        dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())

        clone = self.clone_data(dataSet)
       
        #dataSet = self.slice_data(dataSet, 'phaseanomfil', -1, 1)
        pd = dataSet.GetPointData()
        numOfArrays = pd.GetNumberOfArrays()
        sstData = pd.GetArray('phaseanomfil')
        #print sstData.__class__
        for i in range(numOfArrays):
            print pd.GetArrayName(i)
        
        print sstData.GetSize()
        print sstData.GetValue(16000)
        print sstData.GetNumberOfComponents()
        print dataSet.GetPoint(16000)
        (minz, maxz) = sstData.GetRange()
        #print minz, maxz
       
        colors = self.get_phase_color_map(sstData)
        dataSet.GetPointData().SetScalars(colors)
        
        # Create a mapper
        mapper = vtkDataSetMapper()
        #mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetInput(dataSet)
        mapper.ScalarVisibilityOn()
        #mapper.SetInputData(sstData)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
 
        #amplitude part starts here

        clone = self.slice_data(clone, 'ampanomfil', -1, 1)
        amplData = clone.GetPointData().GetArray('ampanomfil')


        colors1 = self.get_amp_color_map(amplData)
        clone.GetPointData().SetScalars(colors1)

        ampMapper = vtkDataSetMapper()
        ampMapper.SetInput(clone)
        ampMapper.ScalarVisibilityOn()

        actor2 = vtkActor()
        actor2.SetMapper(ampMapper)
        #actor2.GetProperty().SetOpacity(0.995);

        self.ren.AddActor(actor)
        self.ren.AddActor(actor2)
        self.ren.ResetCamera()
        #self.show()
        self.iren.Initialize()
        
    def initVTK(self):
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.amp_max = 0
        self.amp_min = 0
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    #window.show()
    sys.exit(app.exec_())
