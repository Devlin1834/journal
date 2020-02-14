# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:26:32 2019

@author: Devlin
""" 
#################################|_____________________________________________|
from datetime import date      ##|_____________________________________________|
######################################|                                   |####|
import tkinter as tk                ##|   This is the code for adding new |####|
from tkinter import scrolledtext    ##| entries. It opens a small window  |####|
from tkinter import messagebox      ##| with a scrolledtext box for the   |####|
######################################/ entry itself and an Entry Widget  \####|
import journal_template as jt      ##/ for the title of the entry. Here,   \###|
import journal_toolkit as kit     ##/ entry refers to a writeup on the sub- \##|
import journal_details as jd     ##/ -ject material, not the subject itself. \#|
##################################/___________________________________________\|
###############################################################################\
## ENTRY EDITOR ################################################################)
###############################################################################/
class Editor():
    def __init__(self, master, tbl, source = None):
        self.master = master
        self.master.title('Add a New Thought')
        self.frame = tk.Frame(self.master, **jt.bframe_style)
        self.init_tbl = tbl
        self.session = None
        self.source = source
        
        if self.source is None:
            self.source = self.source_create()
        
        self.new = self.source.content == []
        
        #######################################################################
        ## TITLE ##############################################################
        elab = tk.Label(self.frame,
                        text = 'Entry Name >> ', 
                        **jt.message_style)
        
        elab.grid(row = 1, 
                       column = 0)
        
        self.ename = tk.Entry(self.frame, 
                              width = 55)
        
        self.ename.grid(row = 1, 
                        column = 1, 
                        padx = 5, 
                        pady = 5)

        #######################################################################
        ## OPINION BOX ########################################################
        self.opinion_box = scrolledtext.ScrolledText(self.frame,
                                                     width = 60, 
                                                     height = 25)
        
        self.opinion_box.grid(columnspan = 2,
                              rowspan = 2)
        
        #######################################################################
        ## CHECKBOX ###########################################################
        self.vstate = tk.BooleanVar()
        self.vstate.set(False)
        verify = tk.Checkbutton(self.frame,
                                text = 'Verify You\'re Ready to Submit', 
                                var = self.vstate, 
                                **jt.check_style)
        
        verify.grid(row = 5, 
                    column = 0, 
                    sticky = tk.E, 
                    padx = 5, 
                    pady = 5)
 
        #######################################################################
        ## SUBMIT BUTTON ######################################################
        txt = {True: 'Add Details',
               False: 'Attach Entry'}
        
        sbmt = tk.Button(self.frame, 
                         text = txt[self.new], 
                         command = lambda y = self.new: self.add_details(y), 
                         **jt.button_style)
        
        sbmt.grid(row = 5, 
                  column = 1, 
                  sticky = tk.E, 
                  padx = 5, 
                  pady = 5)
        
        #######################################################################
        ## FRAME PACK #########################################################
        self.frame.grid()  
        
    ###########################################################################\
    ## ADD DETAILS #############################################################)
    ###########################################################################/
    def add_details(self, new = True):
        """IMPORTANT: If you get an error in saving the subject, the entry will
        still be saved to a now-useless subject_id. You'll need to open up
        sqlite3 on the propmpt and delete the entry by hand."""
        if self.vstate.get():
            content = self.opinion_box.get('1.0', tk.END)
            name = self.ename.get()
            line = (self.source.subject_id, name, str(date.today()), content)
            kit.SQL_insert(line, 'E')
            
            if new:
                self.session = tk.Toplevel(self.master, **jt.bframe_style)
                jd.Page(self.session, self.source)
                self.master.withdraw() 
            else:
                self.master.destroy()
        
        else:
            veri = 'Please verify that you are\nfinished writing your thoughts'
            messagebox.showinfo('Please Verify', veri)
            
    ###########################################################################\
    ## SOURCE CREATE ###########################################################)
    ###########################################################################/
    def source_create(self):
        """Creates a blank class to be populated by the details we add. It used
        to be more important to the script but since adding SQLite, it's been 
        pared down a bit. Still, its necessary to generate the details UI"""
        identity = kit.idfy(12)
        
        c = {'books': kit.Book,
             'movies': kit.Movie,
             'tvshows': kit.TVShow,
             'restaurants': kit.Food,
             'other': kit.Other}
        
        blanks = ['' for i in range(jt.presets[self.init_tbl])]
            
        return c[self.init_tbl](identity, *blanks)