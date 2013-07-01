#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Izzat Mukhanov <izzatbek@gmail.com   >             *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__ = "DrawBot v 1.0 beta for Symoro+"
__author__ = "Izzat Mukhanov <izzatbek@gmail.com>"

from kinematics import Kinematics
from robots import table_rx90 as table
from create_window import display as c_display
from visual import *
import wx

class Graphics:
    def init_all(self, robot):
        """Helper function providing common initialization for initial robot and robot that is set later after editing"""
        self.scene.autocenter = True
        self.scene.autoscale = True
        self.kinematics = Kinematics(robot)
        self.assign_scale()
        self.init_lists()
        self.init_ui()
        self.draw()
        self.update_spin_controls()
        rate(1000)
        # rate is executed to perform code above before turning off the autocenter and autoscale
        self.scene.autoscale = False
        self.scene.autocenter = False

    def __init__(self, panel, sizer, change_function, robot=table, width=600, height=600, x=900, y=0):
        """Arguments:
        panel - wxPanel on UI-elements will be placed
        sizer - wxBoxSizer (to make proper layout)
        change_function - a pointer to the function which is called
            when a particular joint is selected in order to show its geometrical parameters
        robot - a list or tuple of tuples representing each row of the robot description table
        width, height, x, y - self-explanatory
        """
        self.p = panel
        self.main_sizer = sizer
        self.scene = c_display(x=x, y=y, width=width, height=height, forward=vector(0,1,0), background=(1,1,1), title="Simulation")
        self.scene.bind('mousedown', self.grab)
        self.scene.bind('click', self.select)
        distant_light(direction=(0, -1, 0), color=color.gray(0.35))
        # cost_tolerance defines the value of tolerance required for convergence of loops
        self.cost_tolerance = 20
        self.init_all(robot)
        # Reference to the function which is called when a joint is selected
        self.ch_func = change_function

    def set_robot(self, robot=table):
        """ The function is called when the graphics window is already displayed to draw new robot description """
        for obj in self.scene.objects:
            obj.visible = False
            del obj
        self.init_all(robot)

    def init_ui(self):
        """Initialization of UI-elements"""
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        gridControl = wx.GridBagSizer(hgap=10, vgap=10)
        cb = wx.CheckBox(self.p, label="Exploded View")
        cb.SetValue(True)
        cb.Bind(wx.EVT_CHECKBOX, self.changeRepresentation)
        gridControl.Add(cb, pos=(0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.cb_end_effs = wx.CheckBox(self.p, label="End-effectors")
        self.cb_end_effs.SetValue(True)
        self.cb_end_effs.Bind(wx.EVT_CHECKBOX, self.end_effector_change)
        gridControl.Add(self.cb_end_effs, pos=(1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        cb_world = wx.CheckBox(self.p, label="Base frame")
        cb_world.SetValue(False)
        cb_world.Bind(wx.EVT_CHECKBOX, self.world_frame)
        gridControl.Add(cb_world, pos=(2,0), flag=wx.ALIGN_CENTER_VERTICAL)

        self.tButton = wx.ToggleButton(self.p, label="All Frames")
        self.tButton.SetValue(True)
        self.tButton.Bind(wx.EVT_TOGGLEBUTTON, self.show_all_frames)
        gridControl.Add(self.tButton, pos=(3,0), flag=wx.ALIGN_CENTER)

        self.btnReset = wx.Button(self.p, label="Reset All")
        self.btnReset.Bind(wx.EVT_BUTTON, self.reset_joints)
        gridControl.Add(self.btnReset, pos=(7,0), flag=wx.ALIGN_CENTER)

        btnRandom = wx.Button(self.p, label="Random")
        btnRandom.Bind(wx.EVT_BUTTON, self.find_random)
        gridControl.Add(btnRandom, pos=(8,0), flag=wx.ALIGN_CENTER)

        self.solve_loops = self.kinematics.contains_loops()
        self.contains_loops = self.solve_loops
        if self.kinematics.contains_loops():
            self.radioBox = wx.RadioBox(self.p, choices = ['Make Loops', 'Break Loops'], style=wx.RA_SPECIFY_ROWS)
            self.radioBox.Bind(wx.EVT_RADIOBOX, self.select_loops)
            gridControl.Add(self.radioBox, pos=(9,0), flag=wx.ALIGN_CENTER)

            self.lblConvergence = wx.StaticText(self.p, label='  Convergence  ')
            self.lblConvergence.SetForegroundColour((0,127,0))
            font = self.lblConvergence.GetFont()
            font.SetWeight(wx.BOLD)
            self.lblConvergence.SetFont(font)
            gridControl.Add(self.lblConvergence, pos=(10,0), flag=wx.ALIGN_CENTER)

            self.btnActive = wx.Button(self.p, label="Solve Active")
            self.btnActive.Bind(wx.EVT_BUTTON, self.find_close)
            gridControl.Add(self.btnActive, pos=(11,0), flag=wx.ALIGN_CENTER)

            self.btnReset.SetLabelText("Reset Active")

        self.opacity = 1.
        s = wx.Slider(self.p, size=(100,20), minValue=0, maxValue=99, value=99)
        s.Bind(wx.EVT_SCROLL, self.change_opacity)
        label = wx.StaticText(self.p, label='Joint opacity')
        gridControl.Add(label, pos=(5,0), flag=wx.ALIGN_CENTER)
        gridControl.Add(s, pos=(6,0), flag=wx.ALIGN_CENTER)

        self.spin_ctrls = []
        gridJoints = wx.GridBagSizer(hgap=10, vgap=10)
        for i, jnt in enumerate(self.kinematics.mjoints):
            gridJoints.Add(wx.StaticText(self.p, label='q'+str(jnt.j)), pos=(i,0), flag=wx.ALIGN_CENTER_VERTICAL)
            if jnt.isprismatic():
                s = wx.SpinCtrlDouble(self.p, size=(70,-1), id=i, min=0, max=self.max_prismatic, value="0")
            else:
                s = wx.SpinCtrlDouble(self.p, size=(70,-1), id=i, min=-180, max=180, value="0")
            s.Bind(wx.EVT_SPINCTRLDOUBLE, self.setq)
            s.SetDigits(2)
            if jnt.ispassive():
                s.Enable(False)
            self.spin_ctrls.append(s)
            s.SetIncrement(5)
            gridJoints.Add(s, pos=(i,1), flag=wx.ALIGN_CENTER_VERTICAL)

        choices = []
        for i, jnt in enumerate(self.kinematics.joints):
            choices.append("Frame " + str(jnt.j))

        self.drag_pos = None
        self.check_list = wx.CheckListBox(self.p, choices=choices)#, size=wx.Size(100, len(choices)*(cb.GetSize().GetHeight()+1)))
        self.check_list.SetChecked(range(len(choices)))
        self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.check_frames)
        gridControl.Add(self.check_list, pos=(4,0), flag=wx.ALIGN_CENTER)

        top_sizer.Add(gridJoints, 0, wx.ALL, 10)
        top_sizer.AddSpacer(10)
        top_sizer.Add(gridControl, 0, wx.ALL, 10)
        self.main_sizer.Add(top_sizer, 0, wx.ALL, 12)
        if __name__ == "__main__":
            self.p.SetSizerAndFit(self.main_sizer)

    def show_frames(self, list):
        """Diplays frames which are in the list """
        selected_frames = [f for i, f in enumerate(self.frames) if i in list]
        for i, obj in enumerate(self.frames_arrows):
            obj.visible = True if obj.frame in selected_frames else False

    def init_lists(self):
        """This function is called whenever the objects in the display are redrawn.
        """
        self.joint_objs = []
        self.frames_arrows = []
        self.end_frames = []
        self.frames = []
        # cylinders and next joint
        self.prismatic_links = []

    def show_end_effectors(self, show=True):
        """Draws or removes end-effectors (Which are just joints that are not antecedents of other joints and are not cut joints
        """
        if show:
            indices = self.kinematics.get_last_joints_indices()
            for index in indices:
                obj = self.joint_objs[index]
                direction = self.direction(self.kinematics.joints[index])
                eframe = frame(frame=obj.frame, axis=(direction, 0, 0))
                self.end_frames.append(eframe)
                cylinder(frame=eframe, axis=(self.len_obj/4, 0, 0), radius=self.rad_con, opacity=0.5, color=color.magenta)
                cylinder(frame=eframe, axis=(0, self.len_obj/6, 0), radius=self.rad_con, opacity=0.5, pos=(self.len_obj/4, 0, 0), color=color.magenta)
                cylinder(frame=eframe, axis=(0, -self.len_obj/6, 0), radius=self.rad_con, opacity=0.5, pos=(self.len_obj/4, 0, 0), color=color.magenta)
                cylinder(frame=eframe, axis=(self.len_obj/6, 0, 0), radius=self.rad_con, opacity=0.5, pos=(self.len_obj/4, self.len_obj/6, 0), color=color.magenta)
                cylinder(frame=eframe, axis=(self.len_obj/6, 0, 0), radius=self.rad_con, opacity=0.5, pos=(self.len_obj/4, -self.len_obj/6, 0), color=color.magenta)
                if isinstance(obj, cylinder):
                    eframe.pos = (obj.pos.x + self.len_obj/2 + direction*self.len_obj/2, 0, 0)
                else:
                    eframe.pos = (obj.pos.x + direction*self.len_obj/2, 0, 0)
        else:
            for f in self.end_frames:
                for obj in f.objects:
                    obj.visible = False
                    del obj
            self.end_frames = []

    def put_frame(self, frame, i=0):
        """ Helper function to draw the z and x - axes with the labels on them """
        frame.visible = True
        visible = self.check_list.IsChecked(i)
        self.frames_arrows.append(arrow(frame=frame, axis=(self.len_obj,0,0), color=color.red, shaftwidth=self.len_obj/25., visible=visible))
        self.frames_arrows.append(label(frame=frame, text="z"+str(i+1), pos=(self.len_obj,0), opacity=0, yoffset=3, color=color.black, border=0, box=False, line=False, visible=visible))
        self.frames_arrows.append(arrow(frame=frame, axis=(0,self.len_obj,0), color=color.green, shaftwidth=self.len_obj/25., visible=visible))
        self.frames_arrows.append(label(frame=frame, text="x"+str(i+1), pos=(0,self.len_obj), opacity=0, yoffset=3, color=color.black, border=0, box=False, line=False, visible=visible))

    def assign_scale(self):
        """ This function calculates coefficients which are used to draw the objects (Joints, links, end-effectors)
        It computes the minimum and maximum r or d different from 0.
        Then uses those sizes to determine the reference numbers which are used all over the class.

        self.len_obj determines the length of prismatic and revolute joints. In addition, it is used as reference with constant coefficient to determine other sizes and lengths
        self.rad_con determines the radius of links
        self.max_prismatic defines the upper limit for prismatic joints [0; self.max_prismatic]

        """
        minv = inf
        maxv = 0
        for i, jnt in enumerate(self.kinematics.joints):
            dist = max(abs(jnt.r), abs(jnt.d))
            if dist < minv and dist != 0:
                minv = dist
            if dist > max:
                maxv = dist
        if minv == inf:
            minv, maxv = 100, 100
        self.len_obj = minv/2.
        self.rad_con = self.len_obj/50.
        self.max_prismatic = 4*(minv + maxv)
        self.kinematics.set_ub(self.max_prismatic)

    def direction(self, jnt):
        """Returns 1 if the direction of previous r was positive otherwise 0
        It is used to determine the direction of shifts in expanded view.
        (Scientific Representation close to Wisama Khalil's representation in the books)
        """
        while jnt:
            if jnt.r != 0:
                return jnt.r/abs(jnt.r)
            jnt = jnt.antc
        return 1

    def check_cost(self, cost):
        """ Determines if the found solution is tolerable. If not, displays "No Convergence"
        """
        if self.contains_loops:
            if (cost > self.cost_tolerance):
                self.lblConvergence.SetLabelText("No Convergence!")
                self.lblConvergence.SetForegroundColour((255,0,0))
                self.btnActive.Enable(True)
                return False
            else:
                self.lblConvergence.SetLabelText("    Convergence    ")
                self.lblConvergence.SetForegroundColour((0,127,0))
                self.btnActive.Enable(False)
                return True

    def draw(self, scientific=True):
        """
        The core method of this class. The function draws all the objects once, assigns to corresponding frames.
        The next time redraw-method is called to simplify calculations and drawing by changing depending on the frame positions and orientations.
        This method makes use of DGM transformation matrices to calculate frames and links.
        """
        transforms, cost = self.kinematics.get_joint_transforms(self.solve_loops)
        self.check_cost(cost)
        shiftp = 0
        for i, jnt in enumerate(self.kinematics.joints):
            T = transforms[i]
            f = frame(axis=T[:3,2],pos=T[:3,3], up=T[:3,0])
            self.frames.append(f)
            if jnt.antc:
                prevIndex = self.kinematics.joints.index(jnt.antc)
                prevF = self.frames[prevIndex]
                # To have nice and consistent representation and to apply expanded representation
                # One vector (link) connecting 2 consecutive frames is broken down into 2 vectors:
                p = vector(jnt.T[2,3], jnt.T[0,3], jnt.T[1,3])
                a = vector(jnt.T[2,2], jnt.T[0,2], jnt.T[1,2])*jnt.r + vector(1,0,0)*jnt.b
                q = p - a
                # The first one is along x or u of the first frame
                cylinder(frame=prevF, axis=q, radius=self.rad_con, opacity=0.5)
                # The second one is along  z of the second frame
                cyl = cylinder(frame=f, axis=(-jnt.r, 0, 0), radius=self.rad_con, opacity=0.5)
                if jnt.isprismatic():
                    # The second one is added into prismatic links list
                    # because it may change not only position but length as well
                    self.prismatic_links.append((cyl, jnt))

            if jnt.isprismatic():
                obj = box(frame=f, axis=(self.len_obj,0,0), height=self.len_obj/4., width=self.len_obj/4., opacity=self.opacity, color= color.orange)
            elif jnt.isrevolute():
                obj = cylinder(frame=f, pos=(-self.len_obj/2,0,0), axis=(self.len_obj,0,0), radius=self.len_obj/8., opacity=self.opacity, color=color.yellow)
            else:
                obj = sphere(frame=f, radius=self.len_obj/6., color=color.green, opacity=self.opacity)
            self.put_frame(f, i)
            self.joint_objs.append(obj)

            # If representation is exploded (scientific) and 2 consecutive frames have the same position
            if scientific and jnt.d == 0 and jnt.r == 0:
                # Shift If:
                # the previous frame was the first
                if i == 1:
                    self.joint_objs[i-1].pos -= (3*self.len_obj/2,0,0)
                    cylinder(frame=prevF, axis=(-3*self.len_obj/2, 0, 0), radius=self.rad_con, opacity=0.5)
                # or current frame is the last
                elif self.kinematics.is_last_joint(jnt):
                    diff = vector(self.direction(jnt.antc)*3*self.len_obj/2,0,0)
                    obj.pos += diff
                    cylinder(frame=f, axis=diff, radius=self.rad_con, opacity=0.5)
                # or previous frame had r != 0
                elif jnt.antc and jnt.antc.r != 0:
                    # previous was coaxial prismatic with r != 0
                    if not jnt.antc.isrevolute() and prevF.axis == f.axis:
                        shiftp = (abs(jnt.antc.r) - 2*self.len_obj)/3
                        self.joint_objs[prevIndex].pos -= vector(2*shiftp + 3* self.len_obj/2,0,0)*self.direction(jnt.antc)
                    # previous was revolute with r != 0
                    else:
                        self.joint_objs[prevIndex].pos -= vector(jnt.antc.r/2,0,0)
                # or the one before previous was prismatic
                elif shiftp:
                    self.joint_objs[prevIndex].pos -= vector(shiftp + self.len_obj/2,0,0)*self.direction(jnt.antc)
                    shiftp = 0
        self.show_end_effectors(self.cb_end_effs.Value)

    def redraw(self):
        """This function is used to reposition the frames. All other objects are drawn with respect to the frames.
        Therefore, DGM is calculated and applied to frames."""
        transforms, cost = self.kinematics.get_joint_transforms(self.solve_loops)
        self.check_cost(cost)
        for i in range(len(self.frames)):
            T = transforms[i]
            f = self.frames[i]
            f.pos = T[:3,3]
            f.axis = T[:3,2]
            f.up = T[:3,0]
        # For prismatic joints the link length must be recomputed. Therefore, assigning those links to frames wouldn't be sufficient.
        for cyl, jnt in self.prismatic_links:
            cyl.axis = (-(jnt.r+jnt.q),0,0)
        self.update_spin_controls()

    ######### EVENT HANDLERS ##########

    def end_effector_change(self, evt):
        self.show_end_effectors(evt.IsChecked())

    def change_opacity(self, evt):
        """Slider event handler. Changes opacity of all joints
        """
        self.opacity = evt.EventObject.GetValue()/100.
        for obj in self.joint_objs:
            obj.opacity = self.opacity

    def world_frame(self, evt):
        """Adds or removes the frame with labels for the base frame.
        """
        if evt.EventObject.Value:
            self.world_frame = frame(axis=(0,0,1), pos=(0,0,0), up=(1,0,0))
            arrow(frame=self.world_frame, axis=(self.len_obj,0,0), color=color.red, shaftwidth=self.len_obj/25.)
            label(frame=self.world_frame, text="z0", pos=(self.len_obj,0), opacity=0, yoffset=3, color=color.black, border=0, box=False, line=False)
            arrow(frame=self.world_frame, axis=(0,self.len_obj,0), color=color.green, shaftwidth=self.len_obj/25.)
            label(frame=self.world_frame, text="x0", pos=(0,self.len_obj), opacity=0, yoffset=3, color=color.black, border=0, box=False, line=False)
        else:
            self.world_frame.visible = False
            del self.world_frame

    def show_all_frames(self, evt):
        """Shows or hides all the frames (Toggle button event handler
        """
        indices = range(len(self.frames)) if self.tButton.Value else []
        self.show_frames(indices)
        self.check_list.SetChecked(indices)

    def update_spin_controls(self):
        from random import random
        print random()
        for i, jnt in enumerate(self.kinematics.mjoints):
            self.spin_ctrls[i].Value = jnt.q*180/pi if jnt.isrevolute() else jnt.q

    def select_loops(self, evt):
        """Solve loops checkbox event handler. If checked, solves the loops immediately when variables are changed.
        In this case passive variables are disabled for modification and calculated in terms of active variables.
        """
        selection = self.radioBox.GetSelection()
        if selection == 0:
            self.solve_loops = True
            self.redraw()
            for i, ctrl in enumerate(self.spin_ctrls):
                if self.kinematics.mjoints[i].ispassive():
                    ctrl.Enable(False)
            self.btnReset.SetLabelText("Reset Active")
        else:
            self.solve_loops = False
            for i, jnt in enumerate(self.kinematics.mjoints):
                self.spin_ctrls[i].Enable(True)
            self.update_spin_controls()
            self.btnReset.SetLabelText("Reset All")

    def find_close(self, evt):
        """Finds a solution from current configuration by changing all the joint variables (including active)
        """
        if self.check_cost(self.kinematics.find_close()):
            self.redraw()

    def find_random(self, evt):
        """Finds a solution randomly initializing joint variables (including active)
        """
        if self.contains_loops:
            self.check_cost(self.kinematics.find_random(self.cost_tolerance))
            self.radioBox.SetSelection(0)
            self.select_loops(None)
        else:
            self.kinematics.random_qm()
            self.redraw()

    def reset_joints(self, evt):
        """Sets all the joint variables back. Useful for a user in case of loops
        """
        for jnt in self.kinematics.mjoints:
            jnt.q = 0
        self.redraw()

    def check_frames(self, evt):
        """Check list event handler. Shows frames which are selected
        """
        self.show_frames(self.check_list.GetChecked())
        self.tButton.Value = False
        self.check_list.DeselectAll()

    def setq(self, evt):
        """Sets joint values from the spin-controls
        """
        from math import pi
        jntIndex = evt.GetId()
        jnt = self.kinematics.mjoints[jntIndex]
        if jnt.isrevolute():
            jnt.q = pi*evt.Value/180.
        else:
            jnt.q = evt.Value
        self.redraw()

    def changeRepresentation(self, evt):
        """Switch between to representations:
        Normal view - all joints are located on their frames.
        Expanded view - joints are shifted along z if their frames coincide.
        """
        for obj in self.scene.objects:
            if obj != self.world_frame and obj.frame != self.world_frame:
                obj.visible = False
                del obj
        self.init_lists()
        self.draw(evt.IsChecked())

    def select(self, evt):
        """If a joint object is selected, highlights an object and shows only its frame
        """
        self.show_frames(self.check_list.GetChecked())
        for joint in self.joint_objs:
            joint.color = color.yellow if isinstance(joint, cylinder) else color.orange if isinstance(joint, box) else color.green
        obj = evt.pick
        if obj in self.joint_objs:
            obj.color = (obj.color[0]-0.3, obj.color[1]-0.3, obj.color[2]-0.3)
            f = obj.frame
            self.ch_func(self.joint_objs.index(obj) + 1)
            for o in self.frames_arrows:
                if o.frame != f:
                    o.visible = False
                else:
                    o.visible = True

    # The next 3 functions are used for panning - Scene center is shifted to the mouse displacement distance (In the plane parallel to the display passing through scene.center)

    def grab(self, evt):
        self.drag_pos = evt.pos
        self.scene.bind('mouseup', self.drop)
        self.scene.bind('mousemove', self.move)

    def move(self, evt):
        self.scene.center += self.drag_pos - evt.pos

    def drop(self, evt):
        self.scene.unbind('mousemove', self.move)
        self.scene.unbind('mouseup', self.drop)

if __name__ == "__main__":
    class TestWindow:
        def __init__(self, width=500, height=500):
            w = window(width=900, height=600, menus=True, title='Robot')
            self.p = w.panel
            mainSizer = wx.BoxSizer(wx.HORIZONTAL)
            mainSizer.AddSpacer(600)
            Graphics(panel=self.p, sizer=mainSizer, change_function=self.change)

        def change(self, id):
            print id

    TestWindow()