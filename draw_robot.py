from kinematics import Kinematics
from robots import table_rx90 as table
from visual import *

##rod = cylinder(pos=(0,0,0),axis=(500,0,0),radius=100)
##arrow(pos=(0,2,1), axis=(5,0,0), shaftwidth=0.02)
##points(pos=[(0,0,0), (1,0,0), (0,1,0),(0,0,1)], size=1, color=color.red, size_units="world")
##rod2 = cylinder(pos=(2.5,1,0),axis=(0,5,0),radius=0.2)
##f = frame()

#arrow(frame=f2, axis=(0,0,1))
scene.center = (0,2,0)
scene.forward = (0,-1,0)
scene.up = (0,0,1)
f = frame(axis = (0,0,1),pos=(0,0,0), up=(1,0,0))
arrow(frame=f, axis=(1,0,0),color = color.blue)
arrow(frame=f, axis=(0,1,0),color = color.red)
rod = cylinder(frame = f,radius=0.3,color = color.yellow)


# Parameters for the graphical representation
d_rev = 20
l_rev = 200
d_prism = 20
l_prism = 200
d_body = 5

##kinematics = Kinematics(table)
##qstr = ['q{0}'.format(i + 1) for i in range(
##        len(kinematics.ajoints))]
##for jnt in kinematics.joints:
##    T = transform(jnt.theta, jnt.r, jnt.alpha, jnt.d, jnt.gamma, jnt.b)
##    print T
##    m, Pjminus1 = kinematics.get_joint_transform(jnt)
##    Pj = Base.Vector(m.A14, m.A24, m.A34)
##    v = Pj - Pjminus1
##    f = frame()
##    f.pos = Pj
##    f.axis = (m[0][0],m[0][1],m[0][2])
##    if (v.Length > 0):
##        rod = cylinder(Pjminus1, v, radius=5)
##    if (jnt.isrevolute()):
##        rod = cylinder(frame=f, pos=(0,0,-50), axis=(0,0,100))
##    elif (jnt.isprismatic()):
##        joint_shape = Part.makeBox(d_prism, d_prism, l_prism,
##        Base.Vector(-d_prism / 2, -d_prism / 2, -l_prism / 2))
##    if not(jnt.isfixed()):
##        joint_shape.Matrix = m
##        comp.add(joint_shape)
##        feature.Shape = comp
##
##doc = FreeCAD.activeDocument()
##if doc == None:
##    doc = FreeCAD.newDocument()
##mechanism = doc.addObject("Part::FeaturePython", "Mechanism")
##mechanism.Label = "Robot"
##Mechanism(mechanism)
##mechanism.ViewObject.Proxy = 0
##doc.recompute()
##import FreeCADGui as Gui
##Gui.SendMsgToActiveView("ViewFit")

