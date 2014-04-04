#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
'''
    This example demonstrates the usage of the vtNamedColor class.
'''
import vtk
import string
 
def CheckVTKVersion(requiredMajorVersion):
    '''
        Check the VTK version.
    '''
    version = vtk.vtkVersion()
    if version.GetVTKMajorVersion() > requiredMajorVersion:
        raise
    else:
        return
 
class NamedColors(object):
 
    def __init__(self):
        '''
            Define a single instance of the NamedColors class here.
        '''
        self.namedColors = vtk.vtkNamedColors()
 
    def GetRGBColor(self,colorName):
        '''
            Return the red, green and blue components for a 
            color as doubles.
        '''
        rgb = [0.0,0.0,0.0] # black
        self.namedColors.GetColorRGB(colorName,rgb)
        return rgb
 
    def GetRGBColorInt(self,colorName):
        '''
            Return the red, green and blue components for a 
            color as integer.
        '''
        rgb = [0,0,0] # black
        self.namedColors.GetColorRGB(colorName,rgb)
        return rgb
 
    def GetRGBAColor(self,colorName):
        '''
            Return the red, green, blue and alpha
            components for a color as doubles.
        '''
        rgba = [0.0,0.0,0.0,1.0] # black
        self.namedColors.GetColor(colorName,rgba)
        return rgba
 
    def GetRGBAColorInt(self,colorName):
        '''
            Return the red, green, blue and alpha
            components for a color as integer.
        '''
        rgba = [0,0,0,1] # black
        self.namedColors.GetColor(colorName,rgba)
        return rgba
 
    def GetColorNames(self):
        '''
            Return a list of color names.
        '''
        colorsNames = self.namedColors.GetColorNames()
        colorsNames = colorsNames.split('\n')
        return colorsNames
 
    def GetSynonyms(self):
        '''
            Return a list of synonyms.
        '''
        syn = self.namedColors.GetSynonyms()
        syn = syn.split('\n\n')
        synonyms = []
        for ele in syn:
            synonyms.append(ele.split('\n'))
        return synonyms
 
    def FindSynonyms(self,colorName):
        '''
            Find any synonyms for a specified color.
        '''
        availableColors = self.GetColorNames()
        synonyms = []
        # We use lower case for comparison and 
        # just the red, green, and blue components
        # of the color.
        lcolorName = colorName.lower()
        myColor = self.GetRGBColorInt(colorName)
        for color in availableColors:
            rgb = self.GetRGBColorInt(color)
            if myColor == rgb:
                synonyms.append(color)
        return synonyms
 
 
    def DisplayCone(self):
        ''' 
            Create a cone, contour it using the banded contour filter and
                color it with the primary additive and subtractive colors.
        '''
        #print namedColors
 
        # Create a cone
        coneSource = vtk.vtkConeSource()
        coneSource.SetCenter(0.0, 0.0, 0.0)
        coneSource.SetRadius(5.0)
        coneSource.SetHeight(10)
        coneSource.SetDirection(0,1,0)
        coneSource.Update()
 
        bounds = [1.0,-1.0,1.0,-1.0,1.0,-1.0]
        coneSource.GetOutput().GetBounds(bounds)
 
        elevation = vtk.vtkElevationFilter()
        elevation.SetInputConnection(coneSource.GetOutputPort())
        elevation.SetLowPoint(0,bounds[2],0)
        elevation.SetHighPoint(0,bounds[3],0)
 
        bcf = vtk.vtkBandedPolyDataContourFilter()
        bcf.SetInputConnection(elevation.GetOutputPort())
        bcf.SetScalarModeToValue()
        bcf.GenerateContourEdgesOn()
        bcf.GenerateValues(7,elevation.GetScalarRange())      
 
        # Build a simple lookup table of
        # primary additive and subtractive colors.
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(7)
        # Test setting and getting a color here.
        # We are also modifying alpha.
        rgba = self.GetRGBAColor("Red")
        rgba[3] = 0.5
        self.namedColors.SetColor("My Red",rgba)
        rgba = self.GetRGBAColor("My Red")
        lut.SetTableValue(0,rgba)
        # Does "My Red" match anything?
        match = self.FindSynonyms("My Red")
        print "Matching colors to My Red:", match
 
        rgba = self.GetRGBAColor("DarkGreen")
        rgba[3] = 0.3
        lut.SetTableValue(1,rgba)
        #  Alternatively we can use our wrapper functions:
        lut.SetTableValue(2,self.GetRGBAColor("Blue"))
        lut.SetTableValue(3,self.GetRGBAColor("Cyan"))
        lut.SetTableValue(4,self.GetRGBAColor("Magenta"))
        lut.SetTableValue(5,self.GetRGBAColor("Yellow"))
        lut.SetTableValue(6,self.GetRGBAColor("White"))
        lut.SetTableRange(elevation.GetScalarRange())
        lut.Build()
 
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(bcf.GetOutputPort())
        mapper.SetLookupTable(lut)
        mapper.SetScalarModeToUseCellData()
 
        contourLineMapper = vtk.vtkPolyDataMapper()
        contourLineMapper.SetInputData(bcf.GetContourEdgesOutput())
        contourLineMapper.SetScalarRange(elevation.GetScalarRange())
        contourLineMapper.SetResolveCoincidentTopologyToPolygonOffset()
 
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
 
        contourLineActor = vtk.vtkActor()
        actor.SetMapper(mapper)
        contourLineActor.SetMapper(contourLineMapper)
        contourLineActor.GetProperty().SetColor(
            self.GetRGBColor("black"))
 
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
 
        renderer.AddActor(actor)
        renderer.AddActor(contourLineActor)
        renderer.SetBackground(
            self.GetRGBColor("SteelBlue"))
 
        renderWindow.Render()
 
        fnsave = "TestNamedColorsIntegration.png"
        renLgeIm = vtk.vtkRenderLargeImage()
        imgWriter = vtk.vtkPNGWriter()
        renLgeIm.SetInput(renderer)
        renLgeIm.SetMagnification(1)
        imgWriter.SetInputConnection(renLgeIm.GetOutputPort())
        imgWriter.SetFileName(fnsave)
        imgWriter.Write()
 
        renderWindowInteractor.Start()
 
if __name__ == "__main__":
    try:
        CheckVTKVersion(6)
    except:
        print "You need VTK Version 6 or greater."
        print "The class vtkNamedColors is in VTK version 6 or greater."
        exit(0)
    nc = NamedColors()
    colorNames = nc.GetColorNames()
    print "There are", len(colorNames), "colors:"
    print colorNames
    synonyms = nc.GetSynonyms()
    print "There are", len(synonyms), "synonyms:"
    print synonyms
    nc.DisplayCone()