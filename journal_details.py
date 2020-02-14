# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:31:45 2019

@author: Devlin
"""            
##|                               ___     ___                               ___     ___
##|_______________________________\##\   /##/                               \##\   /##/
################################## \##\ /##/                                 \##\ /##/
import tkinter as tk            ### \#####/    This page is for editing the   \#####/   
from tkinter import messagebox  #### \###/   details and adding notes. It      \###/
##################################### )#(    takes the actual forms from the    )#( 
import journal_template as jt   #### /###\   source class.                     /###\  
import journal_toolkit as kit   ### /#####\                                   /#####\
################################## /##/ \##\_________________________________/##/ \##\
################################# /##/   \#####################################/   \##\
## EDIT DETAILS PAGE ########### (##(  *  )-----------------------------------(  *  )##)
################################# \##\___/#####################################\___/##/
class Page():
    def __init__(self, master, source):
        self.master = master
        self.source = source
        self.master.title('Add Details For {}'.format(self.source.name))        
        cframe = tk.Frame(self.master, **jt.bframe_style)
        sframe = tk.Frame(self.master, **jt.bframe_style)
        nframe = tk.Frame(self.master, **jt.bframe_style)
        
        #######################################################################
        ## SOURCE FILL ########################################################
        self.source.entryUI(cframe)
        
        #######################################################################
        ## NOTE FILL ##########################################################
        self.source.noteUI(nframe)
        
        attach_frame = tk.Frame(nframe, **jt.bframe_style)
        a_button = tk.Button(attach_frame, 
                             text = 'Attach {}'.format(self.source.note_var), 
                             command = self.source.attach_note,
                             **jt.button_style)
        
        a_button.grid()
        attach_frame.grid(row = 3, padx = 10, pady = 10)
        
        #######################################################################
        ## VERIFY AND SUBMIT ##################################################
        self.vstate = tk.BooleanVar()
        self.vstate.set(False)
        verify = tk.Checkbutton(sframe, 
                                text = 'Verify You\'re Ready to Save', 
                                var = self.vstate, 
                                **jt.check_style)
        
        verify.grid(row = 1, 
                    column = 0, 
                    sticky = tk.E + tk.S, 
                    padx = 5, 
                    pady = 5)
        
        
        sbmt = tk.Button(sframe, 
                         text = 'Save', 
                         command = self.opinion_save,
                         **jt.button_style)
        
        sbmt.grid(row = 1, 
                  column = 1, 
                  sticky = tk.E + tk.S, 
                  padx = 5, 
                  pady = 5)
 
        #######################################################################
        ## FRAME FINALIZE #####################################################
        self.master.configure(**jt.bframe_style)
        
        cframe.grid(row = 0, column = 0)
        nframe.grid(row = 0, rowspan = 3, column = 1, padx = 10)    
        sframe.grid(row = 2, column = 0)

    ##########################################################################\
    ## OPINION SAVE ###########################################################)
    ##########################################################################/   
    def opinion_save(self): 
        """Saves the information to the SQLite database"""
        current_raw = kit.SQL_pull('subject_id', self.source.tbl)
        current = [i for t in current_raw for i in t]
        
        if self.vstate.get():
            if self.source.subject_id in current:
                self.source.SQL_save('update')
                self.master.destroy()
            else:
                self.source.SQL_save('new')
                self.master.destroy()
        else:
            please = 'Please verify that you are\nfinished writing your thoughts'
            messagebox.showinfo('Please Verify', please)