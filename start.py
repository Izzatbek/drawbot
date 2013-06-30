from __future__ import division, print_function
from visual import *
import create_window as MY

import os
import wx

from wx.lib.intctrl import IntCtrl
from editor import CreateEditor
from read_par import par_reader


class StartWindow():
    def __init__(self):

        #initialise frame
#        self.w = window(width=640,height=480,menus=True, title="Getting Started...")
        self.w = MY.window(width=640,height=480,menus=True, style=MY.default, title="DrawBot - Getting Started")
#        flag = self.w.win.GetWindowStyleFlag()
#        self.w.win.ToggleWindowStyle(flag)
#        self.w.win.SetWindowStyle(style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
#        self.w.win.Refresh()
#        super(wx.Frame, self.w.win).SetWindowStyle(style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
#        super(wx.Frame, self.w.win).Refresh()
        self.p = self.w.panel

        # Setting up the menu.
        filemenu= wx.Menu()
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.w.win.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.w.win.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.w.win.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        #setup sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)        #main
        radioGrid = wx.GridBagSizer(hgap=5, vgap=5) #for radio buttons
        newGrid = wx.GridBagSizer(hgap=5, vgap=5)   #for new file form
        hSizer = wx.BoxSizer(wx.HORIZONTAL)         #for buttons

        #radio buttons
        self.radioLabel = wx.StaticText(self.p, label="Define geometric parameters from:")
        self.rb1 = wx.RadioButton(self.p, label="New geometric parameter table", style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.p, label="Open existing .par file")
        self.rb1.SetValue(1)
        self.rb2.SetValue(0)
        self.w.win.Bind(wx.EVT_RADIOBUTTON, self.SwitchNew, id=self.rb1.GetId())
        self.w.win.Bind(wx.EVT_RADIOBUTTON, self.SwitchNew, id=self.rb2.GetId())

        #New File Form
        self.lblname = wx.StaticText(self.p, label="Robot Name: ")
        self.lblNJ = wx.StaticText(self.p, label="Number of Physical Joints: ")
        self.lblB = wx.StaticText(self.p, label="Number of Loops: ")
        self.valname = wx.TextCtrl(self.p, value="Enter robot name", size=(140,-1))
        self.valNJ = IntCtrl(self.p, value=6, size=(50,-1), min=0, limited=1)
        self.valB = IntCtrl(self.p, value=0, size=(50,-1), min=0, limited=1)
        self.valB.SetMax(self.valNJ.GetValue())
        self.w.win.Bind(wx.EVT_TEXT, self.ChangeNJ, self.valNJ)

        #OK and Exit buttons
        self.btnOK = wx.Button(self.p, wx.ID_OK, "OK")
        self.w.win.Bind(wx.EVT_BUTTON, self.OnOK, self.btnOK)
        self.btnExit = wx.Button(self.p, wx.ID_EXIT, "Exit")
        self.w.win.Bind(wx.EVT_BUTTON, self.OnExit, self.btnExit)

        #place New File Form widgets
        newGrid.Add((50, 5), pos=(0,0), span=(3,1))
        newGrid.Add(self.lblname, pos=(0,1))
        newGrid.Add(self.lblNJ, pos=(1,1))
        newGrid.Add(self.lblB, pos=(2,1))
        newGrid.Add((10, 5), pos=(0,3), span=(3,1))
        newGrid.Add(self.valname, pos=(0,2))
        newGrid.Add(self.valNJ, pos=(1,2))
        newGrid.Add(self.valB, pos=(2,2))

        #place buttons in hSizer
        hSizer.Add(self.btnOK, 0, wx.ALL, 10)
        hSizer.Add(self.btnExit, 0, wx.ALL, 10)
        
        #place radio buttons with new file form
        radioGrid.Add((10,5), pos=(0,0))
        radioGrid.Add(self.rb1, pos=(0,1))
        radioGrid.Add(newGrid, pos=(1,0), span=(1,2))
#        radioGrid.Add((10,5), pos=(2,0))
        radioGrid.Add(self.rb2, pos=(2,1))

        #place everything together
#        mainSizer.AddSpacer(10)
        mainSizer.Add(self.radioLabel, 0, wx.ALL, 5)
        mainSizer.Add(radioGrid, 0)
#        mainSizer.AddSpacer(10)
        mainSizer.Add(hSizer, 0, wx.ALIGN_RIGHT)
#        mainSizer.AddSpacer(10)
        self.w.SizerFit(mainSizer)

    #event handlers
    def SwitchNew(self, event):
        if (self.rb1.GetValue() == 1):
            self.valname.Enable(1)
            self.valNJ.Enable(1)
            self.valB.Enable(1)
        else:
            self.valname.Enable(0)
            self.valNJ.Enable(0)
            self.valB.Enable(0)
        
    def ChangeNJ(self, event):
        Bmax = self.valNJ.GetValue()
        self.valB.SetMax(Bmax)

    def OnOK(self, event):
        if (self.rb1.GetValue() == 1):
            CreateEditor(NJ=self.valNJ.GetValue(), B=self.valB.GetValue(), name=str(self.valname.GetValue()))
            print((self.valNJ.GetValue(), self.valB.GetValue(), str(self.valname.GetValue())))
            self.w.Destroy()
        else:
            self.OnOpen()
#        event.Skip()
            
    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self.w.win, "Developers:\nMatthias Cassar\nIzzatbek Mukhanov\nGa"+unichr(235)+
                               "l Ecorchard\n\nCopyright "+unichr(169)+" 2013", "About DrawBot v.1.0 Beta", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.w._OnExitApp(e)  # Close the frame.

    def OnOpen(self):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self.w.win, "Choose a file", self.dirname, "", "*.par", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            robot_name, table, NF, NJ = par_reader(os.path.join(self.dirname, self.filename))
            #f = open(os.path.join(self.dirname, self.filename), 'r')
            #self.control.SetValue(f.read())
            #f.close()
            print(table)
            print('\n')
            table = self.CheckForVariables(NF,table)
            print(table)
            CreateEditor(NJ, NF-NJ, table, robot_name)
            print((NJ, NF-NJ, table, robot_name))
            self.w.Destroy()
        dlg.Destroy()

    def CheckForVariables(self,NF,table):
#        for j in range(NF):
#            row = table[j]
#            if row[2] == 0:
#                table[j] = row[0:8] + (0,row[9])
#            elif row[2] == 1:
#                table[j] = row[0:9] + (0,)
#            else:
#                table[j] = row[0:8] + (0,0)
        print(table)
        print('\n')
        
        variables = []
        var_pos = []
        for j in range(NF):
            for row in range(10):
                if isinstance(table[j][row], str):
                    variables.append(table[j][row])
                    var_pos.append((j,row))

        print(variables)
        print('\n')

        v = len(variables)
        if v==0:
            return table
        else:
            ask = AskVariables(parent=self.w.win, variables=variables)
            if ask.ShowModal() == wx.ID_OK:
                print("Got values")
                values = ask.GetValues()
            ask.Destroy()

            for i in range(v):
                r = var_pos[i][0]
                c = var_pos[i][1]
                val = values[i]
                row = table[r]
                table[r] = row[0:c] + (val,) + row[c+1:10]

        print(table)

        return table


class AskVariables(wx.Dialog):

    def __init__(self, parent=None, variables=None):
            super(AskVariables, self).__init__(parent, style=wx.SYSTEM_MENU|wx.CAPTION)
            self.variables = variables
            self.InitUI()
            self.SetTitle("Symbolic Variables Detected")
#            self.SetSizerAndFit(self.mainSizer)

    def InitUI(self):
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        #Instruction
        instr = wx.StaticText(self, label="Some symbolic variables were detected\nwhen loading the .par file. Please provide\nnumerical values for the following:")

        #create scrolling input panel
        from wx.lib.scrolledpanel import ScrolledPanel
        self.p = ScrolledPanel(self)
        
        scrSizer = wx.BoxSizer(wx.VERTICAL)
        scrGrid = wx.GridBagSizer(hgap=5, vgap=5)

        self.value_inputs = []
        for v in range(len(self.variables)):
##            var_lbl = wx.StaticText(self.p, size=(100,22), label=self.variables[v]+":", style=wx.ALIGN_RIGHT)
##            var_val = wx.SpinCtrlDouble(self.p, initial=0, value="0", size=(100,-1))
##            hSizer = wx.BoxSizer(wx.HORIZONTAL)
##            hSizer.Add(var_lbl, 0, flag=wx.ALL, border=5)
##            hSizer.Add(var_val, 0, flag=wx.ALL, border=5)
##            scrSizer.Add(hSizer,0)

            var_lbl = wx.StaticText(self.p, label=self.variables[v]+":", style=wx.ALIGN_RIGHT)
            var_val = wx.SpinCtrlDouble(self.p, initial=0, value="0", size=(100,-1))
            scrGrid.Add(var_lbl, pos=(v,0), flag=wx.ALIGN_RIGHT)
            scrGrid.Add(var_val, pos=(v,1), flag=wx.ALIGN_LEFT)
            self.value_inputs.append(var_val)
        
        scrSizer.Add(scrGrid, 0, wx.ALIGN_CENTRE)
        self.p.SetSizer(scrSizer)
        self.p.SetBestSize((250,150))
#        self.p.SetAutoLayout(1)
#        self.p.SetupScrolling(0,1)
        self.p.SetScrollbars(0,1,1,1)

        #OK button
        okButton = wx.Button(self, wx.ID_OK, "OK")
        okButton.Bind(wx.EVT_BUTTON, self.OnOK)

        #order elements
        self.mainSizer.Add(instr, flag=wx.ALL|wx.ALIGN_CENTER, border = 20)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.p, flag=wx.ALIGN_CENTER)
        self.mainSizer.AddSpacer(20)
        self.mainSizer.Add(okButton, flag=wx.ALL|wx.ALIGN_RIGHT, border = 20)

        self.SetSizerAndFit(self.mainSizer)

    def OnOK(self, e):
        print("OK pressed")
        self.values = []
        for v in range(len(self.variables)):
            self.values.append(self.value_inputs[v].GetValue())
        self.EndModal(wx.ID_OK)

    def GetValues(self):
        return self.values

            

        


if __name__ == '__main__':
    Start=StartWindow()

