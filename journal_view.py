# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:22:26 2019

@author: Devlin
"""
##################################|  Here I have the code for         @@@@@ | 
import tkinter as tk            ##| viewing the entry data. It        (*,*) | 
from tkinter import ttk         ##| also contains the Reader           \~/  |
from tkinter import messagebox  ##| class for reading thoughts      /   |   |
##################################| about the entries. The main    {(---|---|) 
import journal_toolkit as kit   ##| Viewer class populates with     \   |
import journal_template as jt   ##| functions in the source class      / \
import journal_details as jd    ##| and buttons open editing forms   _/   \_
import journal_event as je      ##|____________________________________________
###############################################################################
###############################################################################
#[___________________________________________________________________________]#
#| I have to be totaly honest, I have no idea how scrollbars work. I managed |#
#| to find enough code scraps online to peice together the window I wanted,  |#
#| and it works just the way I want it to, but I have no idea why. I mean,   |#
#| I have a general idea of what does what and why I need to do everything   |#
#| but I have no clue if there is a better way to do this, if anything here  |#
#| is redundant or unnecessary, or if this code secretly destroys the world. |#
#| I was forced to switch to PACK from GRID, which I prefer, because I       |#
#| couldn't find how to use grid with a scrollbar effectively. BUT IT WORKS. |#
#|___________________________________________________________________________|#
###############################################################################
class Reader():
    def __init__(self, master, txt):
        self.master = master
        self.text = txt
        self.master.title(self.text.title)
        self.canvas = tk.Canvas(self.master)
        self.frame = tk.Frame(self.canvas, **jt.rframe_style)
        self.scrollbar = tk.Scrollbar(self.master, 
                                      orient = tk.VERTICAL, 
                                      command = self.canvas.yview)
        
        self.canvas.create_window((0, 0), window = self.frame, anchor = 'nw')
        
        self.header = tk.Label(self.frame, 
                               text = self.text.title, 
                               **jt.reader_style).pack()
        
        self.msg = tk.Message(self.frame, 
                              text = self.text.body,
                              width = 600,
                              **jt.reader_style).pack()
        
        self.canvas.update_idletasks()
        self.canvas.bind('<Enter>', self.mouse_bind)
        self.canvas.bind('<Leave>', self.mouse_unbind)
        
        self.scrollbar.pack(fill = tk.Y, side = tk.RIGHT)
        self.canvas.pack(fill = tk.BOTH, expand = True, side = tk.LEFT)
        
        self.canvas.configure(scrollregion = self.canvas.bbox("all"), 
                              yscrollcommand = self.scrollbar.set, 
                              **jt.rframe_style)
        
        self.master.geometry('630x400')
    
    ###########################################################################
    ## BIND JUJU MAGIC ########################################################
    def mouse_bind(self, event = None):
        self.canvas.bind_all('<4>', self.mousewheel)
        self.canvas.bind_all('<5>', self.mousewheel)
        self.canvas.bind_all('<MouseWheel>', self.mousewheel)
    
    ###########################################################################
    ## UNBIND WITCHCRAFT ######################################################
    def mouse_unbind(self, event = None):
        self.canvas.unbind_all('<4>')
        self.canvas.unbind_all('<5>')
        self.canvas.unbind_all('<MouseWheel>')
    
    ###########################################################################
    ## SOME GODDAMN PARANORMAL ACTIVITY TYPE SHIT #############################
    def mousewheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.canvas.yview_scroll(1, 'units')
            
##############################################################################\
##~~~~~~~~~~~~~~~~~~~~~~~######################################################\
## VIEWER NOTEBOOK CLASS #######################################################)
##~~~~~~~~~~~~~~~~~~~~~~~######################################################/
##############################################################################/
class Viewer():
    def __init__(self, master, source):
        self.master = master
        self.source = source
        self.master.title('Viewing {}'.format(source.name))
        
        tab_control = ttk.Notebook(self.master)
        detail_tab = tk.Frame(tab_control, **jt.bframe_style)
        self.note_tab = tk.Frame(tab_control, **jt.bframe_style)
        tab_control.add(detail_tab, text = 'Details')
        tab_control.add(self.note_tab, text = 'Notes')
        tframe = tk.Frame(detail_tab, **jt.bframe_style)
        sub_frame = tk.Frame(detail_tab, **jt.bframe_style)
        univ_frame = tk.Frame(detail_tab, **jt.bframe_style)
        
        self.session = None
        
        if len(self.source.notes) == 0:
            tab_control.tab(1, state = tk.DISABLED)
        
        #######################################################################
        ## CATEGORY ###########################################################
        clab = tk.Label(tframe, 
                        text = self.source.name, 
                        **jt.header_style)
        
        clab.grid(row = 0, 
                  columnspan = 4)
        
        #######################################################################
        ## SUBJECT ############################################################
        self.source.viewUI(sub_frame)
            
        #######################################################################
        ## LIST BOX ###########################################################
        self.entry_lst = tk.Listbox(univ_frame, 
                                    selectmode = tk.SINGLE, 
                                    width = 60)
        
        self.entry_lst.grid(columnspan = 4, 
                            row = 2, 
                            padx = 10,
                            pady = 10)
        
        for entry in self.source.content:
            self.entry_lst.insert(tk.END, entry.__repr__())
        
        #######################################################################
        ## READ BUTTON ########################################################
        readbutton = tk.Button(univ_frame,
                               text = 'Read Entry',
                               command = self.read_entry,
                               **jt.button_style)
        
        readbutton.grid(row = 3,
                        column = 0,
                        padx = 0,
                        pady = 15)
        
        #######################################################################
        ## ADD ENTRY BUTTON ###################################################
        addbutton = tk.Button(univ_frame, 
                              text = 'Add Entry',
                              command = self.add_entry,
                              **jt.button_style)
        
        addbutton.grid(row = 3,
                       column = 1,
                       padx = 0,
                       pady = 15)
        
        #######################################################################
        ## EDIT DETAILS BUTTON ################################################
        editbutton = tk.Button(univ_frame, 
                               text = 'Edit Details',
                               command = self.edit_entry,
                               **jt.button_style)
        
        editbutton.grid(row = 3,
                        column = 2,
                        padx = 0,
                        pady = 15)
        
        #######################################################################
        ## DELETE THOUGHTS BUTTON #############################################
        delbtn = tk.Button(univ_frame,
                           text = 'Delete Entry',
                           command = lambda x = 'entries': self.thought_delete(x),
                           **jt.button_style)
        
        delbtn.grid(row = 3,
                    column = 3,
                    padx = 0,
                    pady = 15)
        
        #######################################################################
        ## FRAME FINALIZE #####################################################
        tframe.grid(row = 0)
        sub_frame.grid(row = 1)
        univ_frame.grid(row = 2)
        tab_control.pack(fill = 'both')
        
        ##/--------\##########################################################/
        ## NOTE TAB #########################################################(|
        ##\--------/##########################################################\
        self.viewbox = tk.Frame(self.note_tab, **jt.bframe_style)
        nlist_box = tk.Frame(self.note_tab, **jt.bframe_style)
        
        clab = tk.Label(self.note_tab, 
                        text = self.source.name, 
                        **jt.header_style)
        
        clab.grid(row = 0)
        
        #######################################################################
        ## NOTES LIST BOX #####################################################
        self.notes_list = tk.Listbox(nlist_box, 
                                     selectmode = tk.SINGLE, 
                                     width = 40)
        
        self.notes_list.grid(columnspan = 3, row = 0)
        
        for note in sorted(self.source.notes, key = lambda x: x.__str__()):
            self.notes_list.insert(tk.END, note)
        
        #######################################################################
        ## READ BUTTON ########################################################
        see_button = tk.Button(nlist_box, 
                               text = 'Read {}'.format(self.source.note_var),
                               command = self.note_print,
                               **jt.button_style)
        
        see_button.grid(row = 1, column = 0, padx = 5, pady = 10)
        
        #######################################################################
        ## EDIT NOTE BUTTON ###################################################
        rebtn = tk.Button(nlist_box,
                          text = 'Edit {}'.format(self.source.note_var),
                          command = self.edit_note,
                          **jt.button_style)
        
        rebtn.grid(row = 1, column = 1, padx = 5, pady = 10)
        
        #######################################################################
        ## DELETE NOTE BUTTON #################################################
        forget = tk.Button(nlist_box,
                           text = 'Delete {}'.format(self.source.note_var),
                           command = lambda x = 'notes': self.thought_delete(x),
                           **jt.button_style)
        
        forget.grid(row = 1, column = 2, padx = 5, pady = 10)
        
        #######################################################################
        ## FIRST NOTE FILL ####################################################
        self.note_print()
        
        nlist_box.grid(row = 2, padx = 55, pady = 00)
    
    ###########################################################################\
    ## READ ENTRY WINDOW CREATE ################################################)
    ###########################################################################/
    def read_entry(self):
        """Opens a reader window for the selected entry"""
        choice = self.entry_lst.get(tk.ACTIVE)
        names = [i.__repr__() for i in self.source.content]
        dex = names.index(choice)
        target = self.source.content[dex]
        self.session = tk.Toplevel(self.master, **jt.rframe_style)
        Reader(self.session, target)
    
    ###########################################################################\
    ## EDIT ENTRY WINDOW OPEN ##################################################)
    ###########################################################################/
    def edit_entry(self):
        """Opens up the details editor so we can... edit the details..."""
        self.session = tk.Toplevel(self.master, **jt.bframe_style)
        jd.Page(self.session, self.source)
    
    ###########################################################################\
    ## ADD ENTRY WINDOW OPEN ###################################################)
    ###########################################################################/
    def add_entry(self):
        """Lets you add a new entry. These function name are pretty good, huh?"""
        self.session = tk.Toplevel(self.master, **jt.bframe_style)
        je.Editor(self.session, self.source.tbl, self.source)
        
    ###########################################################################\
    ## EDIT NOTE WINDOW OPEN ###################################################)
    ###########################################################################/
    def edit_note(self):
        """Notes Suck. Here is the function that lets us edit a note. It works.
        it's also massive. How the hell does it take this much to edit a note
        but the details can be fixed in about 2 seconds? Notes Suck."""
        names = [note.__str__() for note in self.source.notes]
        
        selected = self.notes_list.get(tk.ACTIVE)
        dex = names.index(selected)        
        reading =  self.source.notes[dex]
        
        self.session = tk.Toplevel(self.master, **jt.bframe_style)
        self.source.noteUI(self.session, base = reading)
        
        attach_frame = tk.Frame(self.session, **jt.bframe_style)
        a_button = tk.Button(attach_frame, 
                             text = 'Rewrite {}'.format(self.source.note_var), 
                             command = lambda x = reading: self.save_rewrite(x),
                             **jt.button_style)
        
        a_button.grid()
        attach_frame.grid(row = 4, padx = 10, pady = 10)
    
    ###########################################################################\
    ## POPULATE NOTE TAB #######################################################)
    ###########################################################################/
    def note_print(self):
        """Notes must account for about 50% of the lines in this program, fuck
        notes. Here we set up the page to read a note. We need that IF block
        because greying out a tab won't prevent this code from running. So a 
        blank note is needed to fill the void"""
        self.viewbox.destroy()
        self.viewbox = tk.Frame(self.note_tab, **jt.bframe_style)

        names = [note.__str__() for note in self.source.notes]
        
        if len(names) > 0:
            selected = self.notes_list.get(tk.ACTIVE)
            dex = names.index(selected)        
            reading =  self.source.notes[dex]
        else:
            reading = kit.Note(0, 'place-holder', self.source.tbl)
            reading.smart_fill(['', '', '', ''])
            
        self.source.readUI(self.viewbox, reading)
        self.viewbox.grid(row = 1, padx = 10, pady = 5)
        
    ###########################################################################\
    ## DELETE THOUGHT ##########################################################)
    ###########################################################################/
    def thought_delete(self, d):
        """Deletes a note or an entry. The two blocks are similar but not
        enough to consolodate. Finds the selected note then creates the 
        SQL to delete it from the database"""
        base = 'DELETE FROM {} WHERE {}'
        if d == 'entries':
            target = self.entry_lst.get(tk.ACTIVE)
            all_repr = [e.__repr__() for e in self.source.content]
            dex = all_repr.index(target)
            dmw = self.source.content[dex]
            txt = 'title = "{}" AND subject_id = "{}"'
            addendum = txt.format(dmw, self.source.subject_id)
        
        elif d == 'notes':
            target = self.notes_list.get(tk.ACTIVE)
            all_str = [n.__str__() for n in self.source.notes]
            dex = all_str.index(target)
            dmw = self.source.notes[dex]
            txt = dmw.SQL_write() + f' AND {self.source.SQL_equal("subject_id")}'
            addendum = txt.format(dmw.item1, dmw.item2, dmw.item3)
       
        ays = 'Are you sure you want to delete this?'
        check = messagebox.askyesno(title = 'Please Verify',
                                    message = ays)
        
        if check:
            kit.SQL_run(base.format(d, addendum))
            
    ###########################################################################\
    ## SAVE NOTE REWRITE #######################################################)
    ###########################################################################/
    def save_rewrite(self, base):
        """Similar to SQL_save on the Subject class, this is how we rewrite a 
        note that has been edited"""
        pull_code = base.SQL_write() + f' AND {self.source.SQL_equal("subject_id")}'
        
        base.rewrite(self.source.note_gets)
        
        atts = jt.sql_notes[:3] + base.details[base.category]
        array = base.__dict__
        current = [array[i] for i in atts]
        
        stored = kit.SQL_pull('*', 'notes', pull_code)[0]

        for i in range(len(jt.sql_notes)):
            new = current[i]
            old = stored[i]
            col = jt.sql_notes[i]
            if new != old:
                if type(new) == int:    
                    SQL = 'UPDATE {} SET {} = {} WHERE note_id = "{}"'
                else:
                    SQL = 'UPDATE {} SET {} = "{}" WHERE note_id = "{}"'
                    
                code = SQL.format('notes', col, new, base.note_id)
                kit.SQL_run(code)
        
        self.session.destroy()