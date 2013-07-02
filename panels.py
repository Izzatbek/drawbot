import os
import wx
from wx.lib.intctrl import IntCtrl
from copy import copy
from math import pi
import sys

class GeometricPanel(wx.Panel):
    def __init__(self, parent, NJ=6, B=0, table=None):
        wx.Panel.__init__(self, parent)

        self.NJ = NJ
        self.B = B
        self.NF = NJ+B
        self.NL = NJ-B

        self.Disabled = False

        # create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid1 = wx.GridBagSizer(hgap=5, vgap=5)
        grid2 = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # create table of geometric parameters
        # NOTE!!! gamma, alpha, theta are in degrees
        if (table==None):
            self.geo_table = []
            for j in range (1,self.NF+1):
                # (antec, sameas, mu, sigma, gamma, b, alpha, d, theta, r)
                if (j > self.NJ):
                    antec = self.NL
                    sameas = j-self.B
                    sigma = 2
                else:
                    antec = j-1
                    sameas = 0
                    sigma = 0
                geo_row = (antec, sameas, 1, sigma, 0, 0, 0, 0, 0, 0)
                self.geo_table.append(geo_row)
        else:
            self.geo_table = table
            #set sameas
            for j in range (1,self.NF+1):
                row = self.geo_table[j-1]
                antec = row[0]
                if (j > self.NJ):
                    sameas = j-self.B
                else:
                    sameas = 0
                mu = row[2]
                sigma = row[3]
                gamma = row[4]*180/pi
                b = row[5]
                alpha = row[6]*180/pi
                d = row[7]
                theta = row[8]*180/pi
                r = row[9]
                self.geo_table[j-1] = (antec, sameas, mu, sigma, gamma, b, alpha, d, theta, r)
                    
        self.currJ = 1
        print(self.geo_table)

        #grid 1 elements
            #labels
        self.lblNF = wx.StaticText(self, label="Number of frames (NF):")
        self.lblNJ = wx.StaticText(self, label="Number of physical joints (NJ):")
        self.lblNL = wx.StaticText(self, label="Number of moving links (NL):")
        self.lblB  = wx.StaticText(self, label="Number of loops (B):")
        self.lblrtype  = wx.StaticText(self, label="Robot Type:")

            #values (static/info)
        self.valNF = wx.StaticText(self, label=str(self.NF))
        self.valNJ = wx.StaticText(self, label=str(self.NJ))
        self.valNL = wx.StaticText(self, label=str(self.NL))
        self.valB  = wx.StaticText(self, label=str(self.B))
        self.valrtype  = wx.StaticText(self, label="")

            #grid layout
        grid1.Add(self.lblNF, pos=(0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.lblNJ, pos=(1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.lblNL, pos=(2,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.lblB,  pos=(3,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.valNF, pos=(0,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.valNJ, pos=(1,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.valNL, pos=(2,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.valB,  pos=(3,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add((30,30), pos=(0,2), span=(4,1))
        grid1.Add(self.lblrtype,  pos=(1,3), flag=wx.ALIGN_CENTER_VERTICAL)
        grid1.Add(self.valrtype,  pos=(1,4), flag=wx.ALIGN_CENTER_VERTICAL)

        #grid 2 elements
            #labels
        self.lblj = wx.StaticText(self, label="j:", style=wx.ALIGN_RIGHT)
        self.lblantec = wx.StaticText(self, label="a:", style=wx.ALIGN_RIGHT)
        self.lblmu = wx.StaticText(self, label="mu:", style=wx.ALIGN_RIGHT)
        self.lblsigma = wx.StaticText(self, label="sigma:", style=wx.ALIGN_RIGHT)
        self.lblgamma = wx.StaticText(self, label="gamma:", style=wx.ALIGN_RIGHT)
        self.lblalpha = wx.StaticText(self, label="alpha:", style=wx.ALIGN_RIGHT)
        self.lbltheta = wx.StaticText(self, label="theta (off.):", style=wx.ALIGN_RIGHT)
        self.lblb = wx.StaticText(self, label="b:", style=wx.ALIGN_RIGHT)
        self.lbld = wx.StaticText(self, label="d:", style=wx.ALIGN_RIGHT)
        self.lblr = wx.StaticText(self, label="r (off.):", style=wx.ALIGN_RIGHT)

            #droplists
        frameList = [str(j+1) for j in range (self.NF)]
        self.valj = wx.ComboBox(self, size=(50, -1), choices=frameList, style=wx.CB_READONLY)
        self.valj.SetSelection(0)
        antecList = [str(j) for j in range (self.NL+1) if (j != self.currJ)]
        self.valantec = wx.ComboBox(self, size=(50, -1), choices=antecList, style=wx.CB_READONLY)
        self.valantec.SetSelection(0)
        self.valmu = wx.ComboBox(self, size=(50, -1), choices=["0","1"], style=wx.CB_READONLY)
        self.valmu.SetSelection(0)
        self.valsigma = wx.ComboBox(self, size=(50, -1), choices=["0","1","2"], style=wx.CB_READONLY)
        self.valsigma.SetSelection(0)

            #numerical inputs
        self.valgamma = wx.SpinCtrlDouble(self, initial=0, size=(70,-1), min=-360, max=360)
        self.valalpha = wx.SpinCtrlDouble(self, initial=0, size=(70,-1), min=-360, max=360)
        self.valtheta = wx.SpinCtrlDouble(self, initial=0, size=(70,-1), min=-360, max=360)
        self.valb = wx.SpinCtrlDouble(self, initial=0, size=(100,-1), min=-999999, max=999999)
        self.vald = wx.SpinCtrlDouble(self, initial=0, size=(100,-1), min=-999999, max=999999)
        self.valr = wx.SpinCtrlDouble(self, initial=0, size=(100,-1), min=-999999, max=999999)
        
            #same event handler for all inputs
        self.Bind(wx.EVT_COMBOBOX, self.ChangeParam, self.valj)
        self.Bind(wx.EVT_COMBOBOX, self.ChangeParam, self.valantec)
        self.Bind(wx.EVT_COMBOBOX, self.ChangeParam, self.valmu)
        self.Bind(wx.EVT_COMBOBOX, self.ChangeParam, self.valsigma)
        self.Bind(wx.EVT_TEXT, self.ChangeParam, self.valgamma)
        self.Bind(wx.EVT_TEXT, self.ChangeParam, self.valalpha)
        self.Bind(wx.EVT_TEXT, self.ChangeParam, self.valtheta)
        self.Bind(wx.EVT_TEXT, self.ChangeParam, self.valb)
        self.Bind(wx.EVT_TEXT, self.ChangeParam, self.vald)
        self.Bind(wx.EVT_TEXT, self.ChangeParam, self.valr)

            #units
        self.dg1 = wx.StaticText(self, label=unichr(186))
        self.dg2 = wx.StaticText(self, label=unichr(186))
        self.dg3 = wx.StaticText(self, label=unichr(186))
        self.mm1 = wx.StaticText(self, label="mm")
        self.mm2 = wx.StaticText(self, label="mm")
        self.mm3 = wx.StaticText(self, label="mm")

            #Show frame description
        self.lblftype = wx.StaticText(self, label="Frame Type:")
        self.valftype = wx.StaticText(self, label="")
        
            #grid layout
        grid2.Add(self.lblj,     pos=(0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lblftype,  pos=(0,3), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, span=(1,3))
        grid2.Add(self.valftype,  pos=(0,7), flag=wx.ALIGN_CENTER_VERTICAL, span=(1,3))
        grid2.Add((5,5), pos=(1,0))
        
        grid2.Add(self.lblantec, pos=(2,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lblmu,    pos=(3,0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lblsigma, pos=(4,0), flag=wx.ALIGN_CENTER_VERTICAL)

        grid2.Add(self.valj,     pos=(0,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.valantec, pos=(2,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.valmu,    pos=(3,1), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.valsigma, pos=(4,1), flag=wx.ALIGN_CENTER_VERTICAL)

        
        grid2.Add(self.lblgamma, pos=(2,3), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lblalpha, pos=(3,3), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lbltheta, pos=(4,3), flag=wx.ALIGN_CENTER_VERTICAL)

        grid2.Add(self.valgamma, pos=(2,4), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.valalpha, pos=(3,4), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.valtheta, pos=(4,4), flag=wx.ALIGN_CENTER_VERTICAL)

        grid2.Add(self.dg1, pos=(2,5), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.dg2, pos=(3,5), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.dg3, pos=(4,5), flag=wx.ALIGN_CENTER_VERTICAL)

        grid2.Add(self.lblb,pos=(2,7), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lbld,pos=(3,7), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.lblr,pos=(4,7), flag=wx.ALIGN_CENTER_VERTICAL)

        #small space for r off.
        grid2.Add((20,20), pos=(2,8), span=(3,1))
        
        grid2.Add(self.valb,pos=(2,9), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.vald,pos=(3,9), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.valr,pos=(4,9), flag=wx.ALIGN_CENTER_VERTICAL)

        grid2.Add(self.mm1, pos=(2,10), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.mm2, pos=(3,10), flag=wx.ALIGN_CENTER_VERTICAL)
        grid2.Add(self.mm3, pos=(4,10), flag=wx.ALIGN_CENTER_VERTICAL)

        #sizers
        mainSizer.Add(grid1, 0, wx.ALL, 5)
        mainSizer.AddSpacer(10)
        mainSizer.Add(grid2, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

        #initialise values
        from visual import rate
        rate(1000)
        self.LoadValues()
        


    def ChangeParam(self, event):

        #Save Changes of currJ
        antec = int(self.valantec.GetValue())
        sameas = self.geo_table[self.currJ-1][1]
        mu    = int(self.valmu.GetValue())
        sigma = int(self.valsigma.GetValue())
        gamma = float(self.valgamma.GetValue())
        alpha = float(self.valalpha.GetValue())
        theta = float(self.valtheta.GetValue())
        b = int(self.valb.GetValue())
        d = int(self.vald.GetValue())
        r = int(self.valr.GetValue())
        # (antec, sameas, mu, sigma, gamma, b, alpha, d, theta, r)
        self.geo_table[self.currJ-1] = (antec, sameas, mu, sigma, gamma, b, alpha, d, theta, r)


        #Change combobox choices and dis/enable inputs
        if (self.currJ != self.valj.GetSelection() + 1):
            self.currJ = self.valj.GetSelection() + 1   #1:NF

                #antecedant list
            antecList = [str(j) for j in range(self.NL+1) if (j != self.currJ)]
            self.valantec.Clear()
            for item in antecList:
                self.valantec.Append(item)

                #mu list
            if (self.currJ > self.NL):
                #joint is passive for j>n, j>NL
                self.valmu.Enable(0)
            else:
                self.valmu.Enable(1)

                #sigma list, and r and theta inputs
            if (self.currJ > self.NJ):
                #joint is fixed (sigma=2) for virtual joints j>NJ
                #and r and theta are zero
                self.valsigma.Enable(0) 
                self.valr.Enable(0) 
                self.valtheta.Enable(0)
            else:
                self.valsigma.Enable(1)
                self.valr.Enable(1) 
                self.valtheta.Enable(1)

        self.LoadValues()

        if self.Disabled:
            self.DisablePanel()

    def LoadValues(self):            
        #Load values to inputs
        # (antec, sameas, mu, sigma, gamma, b, alpha, d, theta, r)
        row = self.geo_table[self.currJ-1]
        self.valantec.SetStringSelection(str(row[0]))
        self.valmu.SetStringSelection(str(row[2]))
        self.valsigma.SetStringSelection(str(row[3]))
        self.valgamma.SetValue(row[4])
        self.valalpha.SetValue(row[6])
        self.valtheta.SetValue(row[8])
        self.valb.SetValue(row[5])
        self.vald.SetValue(row[7])
        self.valr.SetValue(row[9])

        if row[3]==0:
            self.lbltheta.SetLabel("theta off.:")
            self.lblr.SetLabel("r:")
        elif row[3]==1:
            self.lbltheta.SetLabel("theta:")
            self.lblr.SetLabel("r off.:")
        else:
            self.lbltheta.SetLabel("theta off.:")
            self.lblr.SetLabel("r off.:")

        frameTypes=["Normal Joint","End Joint","Cut Joint","Virtual Frame"]
        if self.currJ>self.NJ:
            self.valftype.SetLabel(frameTypes[3])
        else:
            if self.currJ>self.NL:
                self.valftype.SetLabel(frameTypes[2])
            else:
                isend = True
                for j in range(self.NF):
                    if self.geo_table[j][0] == self.currJ:
                        isend = False
                        break
                if (isend):
                    self.valftype.SetLabel(frameTypes[1])
                else:
                    self.valftype.SetLabel(frameTypes[0])

        robotTypes=["Serial Robot","Tree Structure","Closed Loop Robot", "Tree Structure\nwith Closed Loop"]
        nend = 0
        for j in range(1,self.NL+1):
            isend = True
            for f in range(self.NF):
                if self.geo_table[f][0] == j:
                    isend = False
                    break
            if (isend):
                nend = nend+1
        if (nend > 1):
            if self.B == 0:
                self.valrtype.SetLabel(robotTypes[1])
            else:
                self.valrtype.SetLabel(robotTypes[3])
        else:
            if self.B == 0:
                self.valrtype.SetLabel(robotTypes[0])
            else:
                self.valrtype.SetLabel(robotTypes[2])


    def DisablePanel(self):
        self.valantec.Enable(0)
        self.valmu.Enable(0)
        self.valsigma.Enable(0)
        self.valgamma.Enable(0)
        self.valb.Enable(0)
        self.valalpha.Enable(0)
        self.vald.Enable(0)
        self.valtheta.Enable(0)
        self.valr.Enable(0)

        self.Disabled = True

    def EnablePanel(self):

        self.Disabled = False

        self.valantec.Enable(1)
        self.valmu.Enable(1)
        self.valsigma.Enable(1)
        self.valgamma.Enable(1)
        self.valb.Enable(1)
        self.valalpha.Enable(1)
        self.vald.Enable(1)
        self.valtheta.Enable(1)
        self.valr.Enable(1)

        self.ChangeParam(wx.EVT_BUTTON)

    def ChangeJ(self, J):
        self.valj.SetSelection(J-1)
        self.ChangeParam(wx.EVT_BUTTON)


if __name__ == '__main__':
    from visual import *
    w = window(width=640,height=480,menus=True, title="Getting Started...")
    geo = GeometricPanel(w.win)
    w.win.SetSizerAndFit(geo.mainSizer)
