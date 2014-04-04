import vtk
import math
from vtk import *

p0 = (0,0,0)
p1 = (1,1,1)

distSquared = vtk.vtkMath.Distance2BetweenPoints(p0,p1)
dist = math.sqrt(distSquared)

print 'p0 =', p0
print 'p1 =', p1
print 'distSquared =', distSquared
print "distance =", dist
 
#setup sphere
sphereSource = vtk.vtkSphereSource()
sphereSource.Update()
 
polydata = vtk.vtkPolyData()
polydata.ShallowCopy(sphereSource.GetOutput())
 
normals = polydata.GetPointData().GetNormals();
normal0 = normals.GetTuple3(0);
 
print "Normal0: " + str(normal0[0]) + " " + str(normal0[1]) + " " + str(normal0[2])