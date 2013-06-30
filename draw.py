from kinematics import Kinematics
from robots import table_rx90 as table
from visual import *
from numpy import eye, dot
import wx

w = window(width=900, height=600, menus=True, title='Robot')
d = 20
display(window=w, x=d, y=d, width=500, height=500, forward=vector(0,1,0), background=(1,1,1))
p = w.panel # Refers to the full region of the window in which to place widgets

kinematics = Kinematics(table)
frames = []
def draw():
    T = eye(4)
    prevF = frame(axis=(0,0,1), up=(1,0,0))
    coinc = false
    z_axis = None
    prev_cyl = None
    for i, jnt in enumerate(kinematics.joints):
        T = dot(T, jnt.T)
        f = frame(axis=T[:3,2],pos=T[:3,3], up=T[:3,0])
        frames.append(f)

        cylinder(frame=prevF, axis=(jnt.T[2,3], jnt.T[0,3], jnt.T[1,3]), radius=3, opacity=0.5)
        if (jnt.isrevolute()):
            cyl = cylinder(frame=f, pos=(-75,0,0), axis=(150,0,0), radius=20, opacity=0.5, color=color.yellow)
            arrow(frame=f, axis=(100,0,0),color = color.red, shaftwidth=3)
            arrow(frame=f, axis=(0,100,0),color = color.green, shaftwidth=3)

        if i > 0 and f.pos - prevF.pos == (0,0,0):
            if not coinc:
                z_axis = prevF.axis
                prev_cyl.pos = (-275,0,0)
                coinc = true
            elif f.axis == z_axis:
                cyl.pos = (125,0,0)
            elif prevF.axis == z_axis:
                prev_cyl.pos = (-275,0,0)
        else:
            coinc = false
        prevF = f
        prev_cyl = cyl

def redraw():
    T = eye(4)
    for i, jnt in enumerate(kinematics.joints):
        T = dot(T, jnt.T)
        f = frames[i]
        f.pos = T[:3,3]
        f.axis = T[:3,2]
        f.up = T[:3,0]

def setq(evt): # called on slider events
    for i, jnt in enumerate(kinematics.joints):
        jnt.q = sliders[i].GetValue()/100.*2*pi
    redraw()

sliders = []
for i in range(6):
    s = wx.Slider(p, pos=(600,50 + i*40), size=(200,20), minValue=0, maxValue=100)
    s.Bind(wx.EVT_SCROLL, setq)
    wx.StaticText(p, pos=(650,30 + i*40), size=(200,20), label='Set joint variable q'+str(i+1))
    sliders.append(s)

draw()

#TODO text
#TODO transparent joints
#TODO colors