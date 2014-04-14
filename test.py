from vtk import *
#import sys

class A:
    def __init__(self):
        self.a = 5
        
    def AA(self):
        print self.a

if __name__ == "__main__":
    a = A()
    a.AA()
    '''
    cylinder = vtkCylinderSource()
    cylinder.SetResolution(128)
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(cylinder.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    
    ren1 = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    ren1.AddActor(actor)
    #ren1.SetBackground(.1, .2, .3) # Background color dark blue
    
    renWin.Render()
    iren.Start()
    '''