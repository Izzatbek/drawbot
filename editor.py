from __future__ import division, print_function
from visual import *
import create_window as MY

import os
import wx

from copy import copy
from math import pi
from panels import *
from graphics import Graphics


class EditingWindow():
    def __init__(self, NJ=6, B=0, table=None, filename='noname', dirname='',saved=False):
        self.w = MY.window(width = 1024, height = 800, menus=True, exitfn=self.OnExit, 
                           style=MY.default)
        self.p = self.w.panel
        self.filename = filename
        self.dirname = dirname
        self.NJ = NJ
        self.B = B
        self.table = table
        #flag indicating if this is new file
        self.saved = saved
        #flag indicating if simulation mode is active
        self.simulation = False
        # flag indicating if graphics have been called
        self.graphicsCalled = False
        self.CreateExteriorWindowComponents()
        self.CreateInteriorWindowComponents()
        if (table != None):
            self.GraphicToggle(wx.EVT_BUTTON)
        
    def CreateInteriorWindowComponents(self):
        ''' Create "interior" window components '''
        self.CreateButtons()
        self.CreateTabs()
        #Create Main Sizer to enclose everything
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.hSizer, 0, wx.CENTER)
        self.mainSizer.Add(self.ButtonsSizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.w.SizerFit(self.mainSizer)

    def CreateExteriorWindowComponents(self):
        ''' Create "exterior" window components, such as menu and status
            bar. '''
        self.CreateMenu()
        self.w.win.CreateStatusBar()
        self.SetTitle()

    def CreateTabs(self):
        #Create Tabbed Parameter Panel
        self.tabs = wx.Notebook(self.p)
        self.geo_panel=GeometricPanel(self.tabs, self.NJ, self.B, self.table)
        self.tabs.AddPage(self.geo_panel, "Geometric Parameters")
        #table of last parameters saved
        self.lastsaved = copy(self.geo_panel.geo_table)
        #Create Horizontal Sizer to enclose Parameter Panel (and later graphic controls)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer.Add(self.tabs, 0, wx.ALL, 5)
        
    def CreateButtons(self):
        #buttons
        self.btnSave = wx.Button(self.p, label="Save")
        self.btnSaveAs = wx.Button(self.p, label="Save As...")
        self.btnVisualise = wx.Button(self.p, label="Visualise")
        self.w.win.Bind(wx.EVT_BUTTON, self.CheckIfNew, self.btnSave)
        self.w.win.Bind(wx.EVT_BUTTON, self.OnSaveAs, self.btnSaveAs)
        self.w.win.Bind(wx.EVT_BUTTON, self.GraphicToggle, self.btnVisualise)

        self.ButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ButtonsSizer.Add(self.btnSave, 0, wx.ALL, 5)
        self.ButtonsSizer.Add(self.btnSaveAs, 0, wx.ALL, 5)
        self.ButtonsSizer.AddSpacer(30)
        self.ButtonsSizer.Add(self.btnVisualise, 0, wx.ALL, 5)
        
    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ABOUT, '&About', 'Information about this program',
                self.OnAbout),
             (None, None, None, None),
             (wx.ID_NEW, '&New', 'Create a new robot definition', self.OnNew),
             (None, None, None, None),
             (wx.ID_SAVE, '&Save', 'Save the current file', self.CheckIfNew),
             (wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
                self.OnSave),
             (None, None, None, None),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.w.win.Bind(wx.EVT_MENU, handler, item)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File') # Add the fileMenu to the MenuBar
        self.w.win.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def SetTitle(self):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        self.w.win.SetTitle('DrawBot - Editor: %s'%self.filename)


    # Helper methods:

    def defaultFileDialogOptions(self):
        ''' Return a dictionary with file dialog options that can be
            used in both the save file dialog as well as in the open
            file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.par')

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self.w.win, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle() # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

    def CheckIfChanges(self):
        change = False
        for j in range(self.NJ+self.B):
            if (self.lastsaved[j] != self.geo_panel.geo_table[j]):
                change = True
                break
        return change

    # Event handlers:

    def CheckIfNew(self, event):
        if (self.saved == False):
            self.OnSaveAs(event)
        else:
            self.OnSave(event)
                                   
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self.w.win, "Developers:\nMatthias Cassar\nIzzatbek Mukhanov\nGa"+unichr(235)+
                               "l Ecorchard\n\nCopyright "+unichr(169)+" 2013", "AboutDrawBot v.1.0 Beta", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, event):
            #update table
        self.geo_panel.ChangeParam(event)
        if (self.CheckIfChanges() | (not(self.saved))):
            dialog = wx.MessageDialog(self.w.win, 'Exit without saving?',
                                      'Unsaved Changes', wx.YES_NO|wx.NO_DEFAULT)
            if dialog.ShowModal() == wx.ID_YES:
                self.w._OnExitApp(event)
            dialog.Destroy()
        else:
            self.w._OnExitApp(event)  # Close the main window.

    def OnNew(self, event):
        self.geo_panel.ChangeParam(event)
        if (self.CheckIfChanges() | (not(self.saved))):
            dialog = wx.MessageDialog(self.w.win, 'Close current robot without saving?',
                                      'Unsaved Changes', wx.YES_NO|wx.NO_DEFAULT)
            if dialog.ShowModal() == wx.ID_YES:
                if self.graphicsCalled:
                    self.SimControl.scene.visible=False
                self.w.win.Hide()
                from start import StartWindow
                StartWindow()
            dialog.Destroy()
        else:
            if self.graphicsCalled:
                self.SimControl.scene.visible=False
            self.w.win.Hide()
            from start import StartWindow
            StartWindow()

    def OnSave(self, event):
        #Save current robot parameters
            #update table
        self.geo_panel.ChangeParam(event)
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
##        textfile.write(str(self.NJ)+'\n'+str(self.B)+'\n\n')
##        for j in range(self.NJ+self.B):
##            for row in range(10):
##                input = self.geo_panel.geo_table[j][row]
##                #for gamma, alpha, theta: save in radians
##                if ((row == 4) | (row == 6) | (row == 8)):
##                    input = input*pi/180
##                textfile.write(str(input))
##                textfile.write('\n')
##            textfile.write('\n')
        tableRad = self.TableRadians(self.geo_panel.geo_table)
        print("TableRad:")
        print(tableRad)
        from write_par import ParWriter
        textfile.write(ParWriter.par_string(tableRad, self.filename, self.filename))
        textfile.close()
        self.lastsaved=copy(self.geo_panel.geo_table)
        

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.SAVE,
                                   **self.defaultFileDialogOptions()):
            self.saved=True
            self.OnSave(event)

    def GraphicToggle(self, event):
        if self.simulation==True:
            self.OnEdit(event)
        else:
            self.OnVisualise(event)
        self.simulation = not(self.simulation)

    def OnVisualise(self, event):

        #TODO:
        #done: visualise the robot
        #done: to call graphic control and display
        #done: place controls in hSizer (probably need to define sizers inside this class)
        #done: resize the window
        #done: change Visualise button label to "Edit"
        #done: possibly merge with OnEdit to take the right action whether
        #       the window is in parameter mode, or graphics mode
        # Disable tabs!

        self.geo_panel.ChangeParam(event)
        tableRadians = self.TableRadians(self.geo_panel.geo_table)
        if self.graphicsCalled:
            self.SimControl.set_robot(robot=tableRadians)
        else:
            self.SimControl = Graphics(panel=self.p, sizer=self.hSizer, robot=tableRadians, change_function=self.geo_panel.ChangeJ)
            self.graphicsCalled = True
        self.w.SizerFit(self.mainSizer)
        self.btnVisualise.SetLabel("Edit")
        self.geo_panel.DisablePanel()

    def OnEdit(self,event):

        #TODO:
        #DONE: to hide controls
        #DONE: resize the window
        #DONE: must create event binding to the same button
        #DONE: possibly merge OnVisulaise and OnEdit since they are the same button
        # re-enable tabs

        #Remove item=1 --> SimControl sizer
        if self.hSizer.GetChildren():
            self.hSizer.Hide(1)
            self.hSizer.Remove(1)
            self.w.SizerFit(self.mainSizer)
            self.btnVisualise.SetLabel("Visualise")
            self.geo_panel.EnablePanel()

    def TableRadians(self,table):
        tableRadians = []
        for j in range(self.NJ+self.B):
            jtuple = ()
            for row in range(10):
                item = self.geo_panel.geo_table[j][row]
                #for gamma, alpha, theta: save in radians
                if ((row == 4) | (row == 6) | (row == 8)):
                    item = item*pi/180
                jtuple = jtuple+(item,)
            tableRadians.append(jtuple)
        return tableRadians
        
        

def CreateEditor(NJ=6, B=0, table=None, name='noname', dirname='', saved=False):
    EditingWindow(NJ, B, table, name, dirname, saved)
    
    
if __name__ == '__main__':
    CreateEditor()



#app = wx.App(False)
#CreateEditor()
#app.MainLoop()
