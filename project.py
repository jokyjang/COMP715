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

        self.widthL = 1100
        self.heightL = 600

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(self.frame)
        splitter.setSizes([225, self.widthL-225])

        vbox = QtGui.QHBoxLayout()
        vbox.addWidget(splitter)
        self.setLayout(vbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(0, 0, self.widthL, self.heightL)
        
        self.setWindowTitle('Visualization in Science')
        self.show()
    
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

    def slice_data(self, dataset, arrayName, lower, upper, between,
            sliceByLower, sliceByUpper):

        thresholdFilter = vtkThresholdPoints()
        dataset.GetPointData().SetActiveScalars(arrayName)

        if between:
            thresholdFilter.ThresholdBetween(lower, upper)
        elif sliceByUpper:
           thresholdFilter.ThresholdByUpper(upper) 
        else:
            thresholdFilter.ThresholdByLower(lower)

        thresholdFilter.SetInput(dataset)
        thresholdFilter.Update()

        #gFilter = vtkGeometryFilter()
        #gFilter.SetInput(thresholdFilter.GetOutput())
        #gFilter.Update()
        return thresholdFilter.GetOutput()
        #return gFilter.GetOutput()

    def get_lut(self, target, minv, maxv, renderer):
      
        no_of_steps = 8
        dim = 3
        step = (maxv-minv)/no_of_steps

        colors = [[0 for k in xrange(dim)] for j in xrange(no_of_steps+1)]
        colors[0][0] = 0.23
        colors[0][1] = 0.3
        colors[0][2] = 0.75
        colors[1][0] = 0.40
        colors[1][1] = 0.54
        colors[1][2] = 0.93
        colors[2][0] = 0.43
        colors[2][1] = 0.56
        colors[2][2] = 0.95
        colors[3][0] = 0.5
        colors[3][1] = 0.63
        colors[3][2] = 0.98
        colors[4][0] = 0.87
        colors[4][1] = 0.87
        colors[4][2] = 0.87
        colors[5][0] = 0.93
        colors[5][1] = 0.82
        colors[5][2] = 0.76
        colors[6][0] = 0.97
        colors[6][1] = 0.7
        colors[6][2] = 0.59
        colors[7][0] = 0.92
        colors[7][1] = 0.49
        colors[7][2] = 0.37
        colors[8][0] = 0.7
        colors[8][1] = 0.015
        colors[8][2] = 0.15

        transFunction = vtkDiscretizableColorTransferFunction()
        transFunction.SetNumberOfValues(no_of_steps+1)
        transFunction.DiscretizeOn()

        for i in range(0, no_of_steps+1):
            transFunction.addRGBPoint(minv + i * step, colors[i][0],
                    colors[i][1], colors[i][2])

        scalarBarTransFunction = vtkDiscretizableColorTransferFunction()
        scalarBarTransFunction.DeepCopy(transFunction)
        scalarBarTransFunction.SetNumberOfValues(no_of_steps)

        #continents in deep purple color
        transFunction.AddRGBPoint(-999, 0.56, 0.27, 0.52)

        scalarBar = vtkScalarBarActor()
        scalarBar.SetLookupTable(scalarBarTransFunction)
        scalarBar.SetDisplayPosition(self.widthL * 0.2, 20)
        scalarBar.SetWidth(0.5)
        scalarBar.SetHeight(0.08)
        # Do not stretch beyond the default size
        scalarBar.SetMaximumWidthInPixels(scalarBar.GetWidth() * self.widthL)
        scalarBar.SetMaximumHeightInPixels(scalarBar.GetHeight() * self.heightL)
        scalarBar.SetOrientationToHorizontal()
        renderer.AddActor2D(scalarBar)

        return transFunction

    def get_phase_color_map(self, dataset):

        transFunction  = self.get_lut()
        scalarBar = vtkScalarBarActor()
        #scalarBar.SetLookupTable(colorLookupTable)
        scalarBar.SetLookupTable(transFunction)
        scalarBar.SetDisplayPosition(self.widthL * 0.2, 20)
        scalarBar.SetWidth(0.5)
        scalarBar.SetHeight(0.08)
        # Do not stretch beyond the default size
        scalarBar.SetMaximumWidthInPixels(scalarBar.GetWidth() * self.widthL)
        scalarBar.SetMaximumHeightInPixels(scalarBar.GetHeight() * self.heightL)
        scalarBar.SetOrientationToHorizontal()
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
                color[0] = 82 
                color[1] = 87
                color[2] = 110

            colors.InsertNextTupleValue(color)

        return colors

    def get_opacity_value(self, value, no_of_bands):
        temp = (((value - self.amp_min) // (self.amp_max-self.amp_min)) + 1 ) * (255/no_of_bands)

        return (255-temp)

    def get_uncertainity_plan (self, dataset, low, high):

        clone = dataset
        #clone = self.slice_data(dataset, self.amplitude, low, high, True, False,
        #       False)
        amplData = clone.GetPointData().GetArray(self.amplitude)
        clone.GetPointData().SetActiveScalars(self.amplitude)

        colors1 = self.get_amp_color_map(amplData, 0.2, 1)
        clone.GetPointData().SetScalars(colors1)

        ampMapper = vtkDataSetMapper()
        ampMapper.SetInput(clone)
        ampMapper.ScalarVisibilityOn()

        actor2 = vtkActor()
        actor2.SetMapper(ampMapper)
        actor2.GetProperty().SetOpacity(0.97);

        return actor2

    def get_glyph_plane (self, dataset, low, high):

        #lowerHalf = self.clone_data(dataset, self.amplitude)

        clone = dataset
        clone = self.slice_data(dataset, self.amplitude, low, high, True, False,
               False)
        amplData = clone.GetPointData().GetArray(self.amplitude)
        clone.GetPointData().SetActiveScalars(self.amplitude)

        glyphs = vtkGlyphSource2D()
        glyphs.SetGlyphTypeToTriangle()
        glyphs.FilledOff()
        glyphs.SetColor(255,255,0)
        glyphs.Update()

        glyph = vtkGlyph2D()
        glyph.SetInput(clone)
        glyph.SetScaleModeToScaleByScalar()
        glyph.SetScaleFactor(5)
        glyph.SetSourceConnection(glyphs.GetOutputPort())
        #glyph.SetColorModeToColorByVector()
        glyph.SetRange(low, high)
        glyph.Update()


        print "color mode# ", glyph.GetColorModeAsString()

        lut =  vtkLookupTable()
        lut.SetNumberOfTableValues(2);
        lut.SetRange(0.0,1.0);
        lut.SetTableValue( 0, 1.0, 0.0, 0.0);
        lut.SetTableValue( 1, 1.0, 0.0, 0.0);
        #lut.IndexedLookupOn ()
        lut.Build()

        #glyphMapper = vtkGlyph3DMapper()
        glyphMapper = vtkPolyDataMapper()
        glyphMapper.SetInputConnection(glyph.GetOutputPort())
        glyphMapper.SetLookupTable(lut) 
        actor2 = vtkActor()
        actor2.SetMapper(glyphMapper)

        return actor2

    def get_amp_color_map(self, dataset, low, high):

        (minv, maxv) = dataset.GetRange()
 
        print "minv#, maxv#",  low, high       
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(4)
        colors.SetName("Colors")
       
        for i in range(dataset.GetNumberOfTuples()):
            p = dataset.GetValue(i)
            color = [0 for i in range(4)]
            if p >= low and p <= high:  
                for j in range(4):
                    color[j] = 155
                color[3] = 0
            elif p >= -1 and p < low:
                color[0] = 55
                color[1] = 55
                color[2] = 55
                color[3] = 180
            else:
                color[0] = 82
                color[1] = 87
                color[2] = 110
                color[3] = 255

            colors.InsertNextTupleValue(color)

        return colors

    def clone_data(self, dataset, target):

        calc = vtkArrayCalculator()
        calc.SetInput(dataset)
        calc.AddScalarArrayName(target)
        calc.SetFunction(target);
        calc.SetResultArrayName(target);
        calc.Update();
        
        return calc.GetOutput()

    # Here it is assumed that the dataset contains only valid entries and
    # all the invalid entries are marked with value -999
    def get_correlation_uncertainity_design(self, dataset, target, renderer):

        clone = self.clone_data (dataset, target)

        pd = dataSet.GetPointData()
        amplitude = pd.GetArray(target)
        #print sstData.__class__
        #for i in range(numOfArrays):
     
        (minv, maxv) = amplitude.GetRange()
        lut = self.get_lut(target, minv, maxv, renderer) 
        #colors = self.get_phase_color_map(sstData)
        dataSet.GetPointData().SetActiveScalars('phaseanomfil')
        #dataSet.GetPointData().SetScalars(colors)
        # Create a mapper
        mapper = vtkDataSetMapper()
        #mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetInput(dataSet)
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.ScalarVisibilityOn()
        mapper.SetColorModeToMapScalars()
        mapper.SetLookupTable(lut)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.SetScale(8.0, 8.0, 8.0)
         
        #amplitude part starts here
        #actor2 = self.get_glyph_plane(clone, 0, 1)
        #actor2.SetScale(8.0, 8.0, 8.0)

        actor2 = self.get_uncertainity_plan(clone, 0.3, 1)
        actor2.SetScale(8.0, 8.0, 8.0)
        self.ren.AddActor2D(actor)
        self.ren.AddActor2D(actor2)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        

        
    def draw_graph_from_file(self, inputFileName):
        
        print inputFileName
        reader = vtkXMLRectilinearGridReader()
        reader.SetFileName(str(inputFileName))
        reader.Update()
        
        #returns a rectilinear grid
        reader.GetOutput().Register(reader)
        #typecasting to a more general class vtkDataSet
        dataSet = vtkDataSet.SafeDownCast(reader.GetOutput())

        clone = self.clone_data(dataSet, self.amplitude)

        pd = dataSet.GetPointData()
        numOfArrays = pd.GetNumberOfArrays()
        sstData = pd.GetArray('phaseanomfil')
        #print sstData.__class__
        #for i in range(numOfArrays):
      
        lut = self.get_lut() 
        #colors = self.get_phase_color_map(sstData)
        dataSet.GetPointData().SetActiveScalars('phaseanomfil')
        #dataSet.GetPointData().SetScalars(colors)
        # Create a mapper
        mapper = vtkDataSetMapper()
        #mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetInput(dataSet)
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.ScalarVisibilityOn()
        mapper.SetColorModeToMapScalars()
        mapper.SetLookupTable(lut)
        
        # Create an actor
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.SetScale(8.0, 8.0, 8.0)
         
        #amplitude part starts here
        #actor2 = self.get_glyph_plane(clone, 0, 1)
        #actor2.SetScale(8.0, 8.0, 8.0)

        actor2 = self.get_uncertainity_plan(clone, 0.3, 1)
        actor2.SetScale(8.0, 8.0, 8.0)
        self.ren.AddActor2D(actor)
        self.ren.AddActor2D(actor2)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        
    def initVTK(self):
     
        '''
        Keypress j / Keypress t: toggle between joystick (position
        sensitive) and trackball (motion sensitive) styles. In
        joystick style, motion occurs continuously as long as a 
        mouse button is pressed. In trackball style, motion occurs
        when the mouse button is pressed and the mouse pointer moves.
        '''

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.amplitude = "ampanomfil"
        self.amp_max = 0
        self.amp_min = 0
        self.ren = vtkRenderer()
        self.ren.SetBackground(0.32, 0.34, 0.43)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    #window.show()
    sys.exit(app.exec_())
