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
        
        self.setGeometry(300, 300, 600, 400)
        
        self.setWindowTitle('Visualization in Science')
        #self.show()
    
    def get_vtr_file(self):
        
        root = '/Users/zhangzhx/Dropbox/Homework/VisSci/HW1/Data'
        index = (self.year - 1800)*12+self.month
        return "%s/sst_%d/sst_%d_0_0.vtr" % (root, index, index)
    
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
    
    def draw_graph_from_file(self, inputFileName):
        
        print inputFileName
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
        numOfArrays = pd.GetNumberOfArrays()
        sstData = pd.GetArray('sst')
        #print sstData.__class__
        #for i in range(numOfArrays):
        #    print pd.GetArrayName(i)
        
        #print sstData.GetSize()
        #print sstData.GetValue(16000)
        #print sstData.GetElementComponentSize()
        #print sstData.PrintSelf(0)
        (minz, maxz) = sstData.GetRange()
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
            p = sstData.GetValue(i)
            
            dcolor = [0 for i in range(3)]
            colorLookupTable.GetColor(p, dcolor)
            
            color = [0 for i in range(3)]
            for j in range(3):
                color[j] = int(255.0 * dcolor[j])
            
            colors.InsertNextTupleValue(color)
        
        dataSet.GetPointData().SetScalars(colors)
        
        # Create a mapper
        mapper = vtkDataSetMapper()
        #mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetInputData(dataSet)
        #mapper.SetInputData(sstData)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        #self.show()
        self.iren.Initialize()
        
    def initVTK(self):
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    #window.show()
    sys.exit(app.exec_())