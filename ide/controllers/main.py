# -*- coding: utf-8 -*-
# Copyright 2004 Roman Yakovenko.
# 2007 Alexander Eisenhuth
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import wx

""" Contoller class. Part of MVC
Responsibility: Glue view and model code:
- Handle all events from view (p.e. button) """
class MainController:
    def __init__(self, view):
        self._view = view
        
        # Give controller object to the view
        self._view.set_controller(self)
        
    def GenXmlCode(self):
        """ Generate XML code"""
        self._appendOutText("Generation of XML code staretd")
    
    def GenCppCode(self):
        """ Generate Boost.Python code"""
        self._appendOutText("Generation of C++ code for Boost.Python started")
        
    def GenPyPPCode(self):
        """ Generate Py++ code"""
        self._appendOutText("Generation of Py++ code started")
        
    def OpenHeaderDlg(self):
        """ """
        dialog = wx.FileDialog(self._view, "Choose a Header file", ".", "", 
                               "Header (*.h)|*.h|All Files(*)|*", wx.OPEN)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self._view.textHeader.Clear()
                self._view.textHeader.AppendText(dialog.GetPath())
        finally:
            dialog.Destroy()
            
    def OpenGccXmlDlg(self):
        """ """
        dialog = wx.FileDialog(self._view, "Choose GccXml executable", 
                               ".", "", "All Files(*)|*", wx.OPEN)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self._view.textGccXml.Clear()
                self._view.textGccXml.AppendText(dialog.GetPath())
        finally:
            dialog.Destroy()
            
    def _appendOutText(self, text):
        self._view.textOutput.AppendText(text + "\n")
        
    