# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 13:13:54 2019

@author: Devlin
"""
###########################\
import numpy as np       ###\
import random as rn       ###\ 
import sqlite3 as sql      ###\______               
#####################################|    This script acts as the toolkit for
import tkinter as tk              ###| the program. It contains all the general
from tkinter import ttk           ###| use funtions as well as the classes for
from tkinter import scrolledtext  ###| the program data. Where the other 
from tkinter import messagebox    ###| scripts are concerned with display and 
#####################################| editing data, this contains all the 
import journal_template as jt       #| classes and funcs for handling the data.
import journal_sqlinit as jsql      #|
#####################################|________________________________________
##############################################################################\
###############################################################################
##                                CLASSES                                    ##
###############################################################################
##############################################################################/
## NOTE CLASS ###############################################################/
############################################################################/
class Note():
    """Notes are designed to be universal among all entry categories, so it 
    doesn't read well. Check the source details list in journal_template for
    a better understanding"""
    def __init__(self, nid, pid, cat): 
        self.note_id = nid
        self.subject_id = pid
        self.category = cat
        self.details = {'books': jt.notes_book,
                        'movies': jt.notes_movie,
                        'tvshows': jt.notes_tv,
                        'restaurants': jt.notes_food,
                        'other': jt.notes_other}
        
    ###########################################################################
    ###########################################################################
    def SQL_write(self):
        """writes the SQL code to pull this exact note"""
        return 'note_id = {}'.format(self.note_id)
    
    ###########################################################################
    ###########################################################################
    def smart_fill(self, tup):
        """Creates named attributes using the lists in journal_template"""
        atts = self.details[self.category]
        array = self.__dict__
        for i in range(4):
            array[atts[i]] = tup[i]

    ###########################################################################
    ###########################################################################
    def nfind(self, target):
        """For finding information from certain note items. To start, the 
        episode and season number of TV Episodes, as they are saved together.
        I hate this function and want to find a way to remove it."""
        if self.category == 'tvshows':
            markers = {'start': 1,
                       'Ep': self.Episode.find('E'),
                       'end': len(self.Episode)}
            if target.lower() == 's':
                a = markers['start']
                b = markers['Ep']
            elif target.lower() == 'e':
                a = markers['Ep'] + 1
                b = markers['end']
            
        return self.Episode[a:b]      
        
    ###########################################################################
    ###########################################################################
    def rewrite(self, lstobj):
        """takes a list of widgets and pulls the data from them to rewrite its
        own attributes. Widgets must be in order of items 1-4. Currently only
        used in the note edit page"""   
        new = []
        for o in lstobj:
            try:
                new.append(o.get())
            except TypeError:
                new.append(o.get('1.0', tk.END))
                
        if self.category == 'tvshows':
            x = new[:2]
            y = 'S{}E{}'.format(*x)
            new = [y] + new[2:]
        
        self.smart_fill(new)
    
    ###########################################################################
    ###########################################################################
    def __str__(self):
        if self.category == 'books': 
            return self.Quip.capitalize()
        elif self.category == 'movies': 
            return self.Quip.capitalize()
        elif self.category == 'tvshows': 
            return '{}: {}'.format(self.Episode, self.Name)
        elif self.category == 'restaurants': 
            return '{}: {}'.format(self.Course, self.Name)
        else:
            return ''
    
    def __repr__(self):
        return '<Note Object xcidkwhatever54>'

###############################################################################\
## WRITE UP CLASS ##############################################################)
###############################################################################/
class WriteUp():
    def __init__(self, title, dte, body):
        self.title = title
        self.date = dte
        self.body = body
    
    ###########################################################################
    ###########################################################################
    def __repr__(self):
        return '{}: Written {}'.format(self.title, self.date)
    
    def __str__(self):
        return self.body

###############################################################################\
## FORM CREATION CLASSES #######################################################)
###############################################################################/
## These all create data-entry widgets and place a label next to it. #########/
## They also all have a get_data() method that returns the data in   ########/
## the widget. These classes used to be methods of the subject class #######/
## that returned the widget object, but that seemed messy.           ######/
##########################################################################/
#########################################################################/
class CreateEntry():
    def __init__(self, src, txt, order, deftxt):     
        self.row = order.index(txt)
        self.lab = tk.Label(src, text = '{} >> '.format(txt), **jt.message_style)
        
        self.entry = tk.Entry(src, width = 35)
        self.entry.insert(0, deftxt)
        
        self.lab.grid(row = self.row, column = 0)
        self.entry.grid(row = self.row, column = 1, padx = 5, pady = 5)
        
    ###########################################################################
    def get_data(self):
        return self.entry.get()
        
###############################################################################
###############################################################################
class CreateRate():
    def __init__(self, src, txt, order, base):
        self.start = bint(base)
        
        self.row = order.index(txt)
        self.lab = tk.Label(src, text = '{} >> '.format(txt), **jt.message_style)
        
        self.rate = tk.Scale(src, orient = tk.HORIZONTAL, from_ = 0,  to = 10, **jt.scale_style)
        self.rate.set(self.start)
        
        self.lab.grid(row = self.row, column = 0)
        self.rate.grid(row = self.row, column = 1, padx = 5, pady = 5)
     
    ###########################################################################
    def get_data(self):
        return self.rate.get()
    
###############################################################################
###############################################################################
class CreateDrop():
    def __init__(self, src, txt, order, lst, tags): 
        if txt in lst:
            self.dex = lst.index(txt)
        else:
            self.dex = 0
        
        self.row = order.index(txt)
        self.clab = tk.Label(src, text = '{} >> '.format(txt), **jt.message_style)
        
        self.cats = ttk.Combobox(src, values = lst)
        self.cats.current(self.dex)
        
        self.clab.grid(row = self.row, column = 0)
        self.cats.grid(row = self.row, column = 1, padx = 5, pady = 5)
    
    ###########################################################################
    def get_data(self):
        return self.cats.get()
        
###############################################################################\
## SUBJECT PARENT CLASS ########################################################)
###############################################################################/
class Subject():
    def __init__(self, e_id, name, rating):
        self.subject_id = e_id
        self.name = name
        self.rating = rating
        self.notes = self.note_pull()
        self.content = self.content_pull()
        
        self.tbl = ''                  #--------------------------------------#
        self.columns = ()              # To be defined in the child classes.  #
        self.detail_gets = {}          # For use in Parent Class Methods.     #
        self.note_gets = ()            #--------------------------------------#
        
    ###########################################################################\
    ## SQLite INTEGRATION TOOLS ################################################)
    ###########################################################################/
    def note_pull(self):
        """Finds notes in the SQLite 'notes' table with matching subject_ids"""
        notes = []
        y = SQL_pull('*', 'notes', self.SQL_equal('subject_id'))
        
        for n in y:
            blank = Note(*n[:3])
            blank.smart_fill(n[-4:])
            notes.append(blank)
        
        return notes
    
    ###########################################################################
    ###########################################################################
    def content_pull(self):
        """Finds entries in the SQLite 'entries' table with matching subject_ids"""
        work = []
        y = SQL_pull('*', 'entries', self.SQL_equal('subject_id'))
        
        for e in y:
            new = WriteUp(e[2], e[3], e[4])
            work.append(new)
            
        return work
    
    ###########################################################################
    ###########################################################################    
    def SQL_save(self, state):
        """Updates the SQLite tables with new information"""
        array = self.__dict__
        data = {key: item.get_data() for key, item in self.detail_gets.items()}
        
        for key in self.detail_gets:
            array[key] = data[key]
        
        current = [array[i] for i in self.columns]
        
        if state == 'new':
            code = self.tbl[0]
            SQL_insert(current, code)
        elif state == 'update':
            stored = SQL_pull('*', self.tbl, self.SQL_equal('subject_id'))[0]
        
            for i in range(len(self.columns)):
                col = self.columns[i]
                new = current[i]
                old = stored[i]
                if new != old:
                    if type(new) == int:    
                        SQL = 'UPDATE {} SET {} = {} WHERE subject_id = "{}"'
                    else:
                        SQL = 'UPDATE {} SET {} = "{}" WHERE subject_id = "{}"'
                    code = SQL.format(self.tbl, col, new, self.subject_id)
                    SQL_run(code)
            
    ###########################################################################
    ###########################################################################
    def SQL_equal(self, txt):
        """Creates an SQL statement to check for equality. For example...
        subject_id = "ae65_pl9812%" or year = "2011" or rating = 9"""
        array = self.__dict__
        val = array[txt]
        
        if type(val) == int:
            return '{} = {}'.format(txt, val)
        else:
            return '{} = "{}"'.format(txt, val)
    
    ###########################################################################
    def attach_note(self):
        """Takes the data inputed into the notes fields and adds it to the 
        class. Lots of Try/Excepts don't judge me"""
        info = []
        for o in self.note_gets:
            try:
                info.append(o.get())
            except TypeError:
                info.append(o.get('1.0', tk.END))
                
        if self.tbl == 'tvshows':
            x = info[:2]
            y = 'S{}E{}'.format(*x)
            info = [y] + info[2:]
        
        data = (self.subject_id, self.tbl, *info)
        SQL_insert(data, 'N')
        
        messagebox.showinfo('Done', 'Note Attached!')
        for o in self.note_gets:
            try:
                o.delete(0, tk.END)
            except tk.TclError:
                o.delete(1.0, tk.END)
            except AttributeError:
                o.set(0) 
 
    ###########################################################################\
    ## FORM CREATION TOOLS #####################################################)
    ###########################################################################/
    def pair_create(self, src, txt, fill, r, cash = False):
        """Used to populate the Read Entry page. Creates a Label widget
        with the name of the tag in a small font, then places next to it a 
        second Label widget with the tag contents in a large font"""
        money = {True: cashify(str(fill)), False: fill}
        v = money[cash]
        
        label = tk.Label(src, text = '{}: '.format(txt), **jt.detail_style)
        nme = tk.Label(src, text = v, **jt.message_style)
        label.grid(row = r, column = 0, sticky = tk.E)
        nme.grid(row = r, column = 1, sticky = tk.W) 
    
    ###########################################################################\
    ## DUNDER NONSENSE #########################################################)
    ###########################################################################/
    def __str__(self):
        x = len(self.content)
        y = {True: 'ies',
             False: 'y'}
        
        a = len(self.notes)
        b = {True: 's',
             False: ''}
        
        base = '{}: {} Entr{} and {} Note{}'
        
        return base.format(self.name, x, y[x > 1], a, b[a > 1])
    
    def __repr__(self):
        return self.name

#######################################################################\
##            ##########################################################\
## SUBCLASSES ###########################################################\
##            ############################################################\
###########################################################################\
##                                                                       ###\
## READ UI  - Used to read notes attached to the subject class           ####\   
## ENTRY UI - Used to create the add details page for the subject class  #####\
## VIEW UI  - Used to create the view details page for the subject class ######\
## NOTE UI  - Used to create the add note page for the subject class     #######\
##                                                                       ########\
##################################################################################\
## BOOK CHILD CLASS ###############################################################)
##################################################################################/
class Book(Subject):
    def __init__(self, e_id, name, rating, author, pub_year, pages, isbn, genre):
        super().__init__(e_id, name, rating)
        self.author = author
        self.pub_year = pub_year
        self.pages = pages
        self.isbn = isbn
        self.genre = genre
        self.ro = jt.tags_book
        self.columns = jt.sql_books
        self.note_var = 'Quote'
        self.tbl = 'books'
              
    ## READ UI ################################################################
    ###########################################################################
    def readUI(self, src, reading):
        quip = tk.Label(src, 
                        text = '...{}...'.format(reading.Quip), 
                        **jt.detail_style)
            
        quote = tk.Message(src, 
                           text = '"{}"'.format(reading.Quote[:-1]), 
                           **jt.detail_style, 
                           width = 600)
            
        page = tk.Label(src, 
                        text = 'Page {}'.format(reading.Page), 
                        **jt.detail_style)
            
        desc = tk.Message(src, 
                          text = reading.Interpretation, 
                          **jt.detail_style, 
                          width = 600)
        
        quip.grid(row = 1, sticky = tk.W)
        quote.grid(row = 2, sticky = tk.W)
        page.grid(row = 3, sticky = tk.E)
        desc.grid(row = 4, sticky = tk.W)
     
    ## ENTRY UI ###############################################################
    ###########################################################################
    def entryUI(self, src):
        book_name = CreateEntry(src, 'Book Name', self.ro, self.name)
        book_rating = CreateRate(src, 'Rating', self.ro, self.rating)
        auth_name = CreateEntry(src, 'Author', self.ro, self.author)
        pub_year = CreateEntry(src, 'Publication Year', self.ro, self.pub_year)
        page_ct = CreateEntry(src, 'Page Count', self.ro, self.pages)
        isbn = CreateEntry(src, 'ISBN', self.ro, self.isbn)
        genre = CreateEntry(src, 'Genre', self.ro, self.genre)
        
        self.detail_gets = {'name': book_name,
                            'rating': book_rating,
                            'author': auth_name,
                            'pub_year': pub_year, 
                            'pages': page_ct,
                            'isbn': isbn,
                            'genre': genre}
          
    ## VIEW UI ################################################################
    ###########################################################################
    def viewUI(self, src):
        top_frame = tk.Frame(src, **jt.bframe_style)
        lab_frame = tk.Frame(top_frame, **jt.bframe_style)
        rate_frame = tk.Frame(top_frame, **jt.bframe_style)
        mid_frame = tk.Frame(src, **jt.bframe_style)
        
        self.pair_create(lab_frame, 'Author', self.author, 0)          
        self.pair_create(lab_frame, 'Genre', self.genre, 1)       
        self.pair_create(mid_frame, 'Publication Year', self.pub_year, 0)
        self.pair_create(mid_frame, 'Page Count', self.pages, 1)
        self.pair_create(mid_frame, 'ISBN', self.isbn, 2)
        
        rating_label = tk.Label(rate_frame,
                                text = '{}/10'.format(self.rating),
                                **jt.header_style)

        rating_label.grid(row = 0, column = 0, sticky = tk.E)        
        
        top_frame.grid(row = 0)
        lab_frame.grid(column = 0, row = 0)
        rate_frame.grid(column = 1, row = 0)
        mid_frame.grid(row = 1)
        
    ## NOTE UI ################################################################
    ###########################################################################
    def noteUI(self, src, base = None):
        top_line = tk.Frame(src, **jt.bframe_style)
        page_lab = tk.Label(top_line, text = '     Page >> ', **jt.detail_style)
        page_ent = tk.Entry(top_line, width = 5)
        page_lab.grid(column = 0, row = 0)
        page_ent.grid(column = 1, row = 0)
        
        quip_lab = tk.Label(top_line, text = '     Quip >> ', **jt.detail_style)
        quip_ent = tk.Entry(top_line, width = 20)
        quip_lab.grid(column = 2, row = 0)
        quip_ent.grid(column = 3, row = 0)
        top_line.grid(row = 0, padx = 5, pady = 5)
        
        quote_frame = tk.Frame(src, **jt.bframe_style)
        quote_lab = tk.Label(quote_frame, text = '       Quote >> ', **jt.detail_style)
        quote_box = scrolledtext.ScrolledText(quote_frame, width = 30, height = 5)
        
        quote_lab.grid(column = 0, row = 0, sticky = tk.N)
        quote_box.grid(column = 1, row = 0, sticky = tk.E)
        quote_frame.grid(row = 1, padx = 5, pady = 5)
        
        desc_frame = tk.Frame(src, **jt.bframe_style)
        desc_lab = tk.Label(desc_frame, text = 'Description >> ', **jt.detail_style)
        desc_box = scrolledtext.ScrolledText(desc_frame, width = 30, height = 5)
        
        desc_lab.grid(column = 0, row = 0, sticky = tk.N)
        desc_box.grid(column = 1, row = 0, sticky = tk.E)
        desc_frame.grid(row = 2, padx = 5, pady = 5)
        
        self.note_gets = [page_ent, quip_ent, quote_box, desc_box]
       
        if base is not None:
            page_ent.insert(0, base.Page)
            quip_ent.insert(0, base.Quip)
            quote_box.insert(0, base.Quote)
            desc_box.insert(0, base.Interpretation)
           
##################################################################################\
## MOVIE CHILD CLASS ##############################################################)
##################################################################################/
class Movie(Subject):
    def __init__(self, e_id, name, rating, release_year, director, lead, genre, budget, box_office):
        super().__init__(e_id, name, rating)
        self.release_year = release_year
        self.director = director
        self.lead = lead
        self.genre = genre
        self.budget = budget
        self.boxoffice = box_office
        self.ro = jt.tags_movie
        self.columns = jt.sql_movies
        self.note_var = 'Quote'
        self.tbl = 'movies'
        
        d = (bint(self.boxoffice) - bint(self.budget))
        self.ror = round(d / max(1, bint(self.boxoffice)) * 100, 1)
       
    ## READ UI ################################################################
    ###########################################################################
    def readUI(self, src, reading):
        quip = tk.Label(src, 
                        text = '...{}...'.format(reading.Quip), 
                        **jt.detail_style)
            
        quote = tk.Message(src, 
                           text = '"{}"'.format(reading.Quote[:-1]), 
                           width = 300,
                           **jt.detail_style)
        
        ts = tk.Label(src, 
                      text = reading.Time, 
                      **jt.detail_style)
        
        desc = tk.Message(src, 
                          text = reading.Interpretation, 
                          width = 300, 
                          **jt.detail_style)
        
        quip.grid(row = 1, sticky = tk.W)
        quote.grid(row = 2, sticky = tk.W, columnspan = 3)
        ts.grid(row = 3, sticky = tk.E)
        desc.grid(row = 4, sticky = tk.W, columnspan = 3)
   
    ## ENTRY UI ###############################################################
    ###########################################################################    
    def entryUI(self, src):
        movie_name = CreateEntry(src, 'Movie Name', self.ro, self.name)
        year = CreateEntry(src, 'Release Year', self.ro, self.release_year)
        director = CreateEntry(src, 'Director', self.ro, self.director)
        lead = CreateEntry(src, 'Lead', self.ro, self.lead)
        genre = CreateEntry(src, 'Genre', self.ro, self.genre)
        rating = CreateRate(src, 'Rating', self.ro, self.rating)
        budget = CreateEntry(src, 'Budget', self.ro, self.budget)
        boffice = CreateEntry(src, 'Box Office', self.ro, self.boxoffice)
        
        self.detail_gets = {'name': movie_name,
                            'rating': rating,
                            'release_year': year, 
                            'director': director, 
                            'lead': lead, 
                            'genre': genre, 
                            'budget': budget, 
                            'boxoffice': boffice}
        
    ## VIEW UI ################################################################
    ###########################################################################   
    def viewUI(self, src):
        yframe = tk.Frame(src, **jt.bframe_style)
        top_frame = tk.Frame(src, **jt.bframe_style)
        lab_frame = tk.Frame(top_frame, **jt.bframe_style)
        rate_frame = tk.Frame(top_frame, **jt.bframe_style)
        mid_frame = tk.Frame(src, **jt.bframe_style)
        money_frame = tk.Frame(mid_frame, **jt.bframe_style)
        pct_frame = tk.Frame(mid_frame, **jt.bframe_style)
        
        self.pair_create(lab_frame, 'Director', self.director, 0)
        self.pair_create(lab_frame, 'Lead', self.lead, 1) 
        self.pair_create(lab_frame, 'Genre', self.genre, 2) 
        self.pair_create(yframe, 'Year', self.release_year, 0)
        self.pair_create(money_frame, 'Budget', self.budget, 0, cash = True)
        self.pair_create(money_frame, 'Box Office', self.boxoffice, 1, cash = True)
        
        rating_label = tk.Label(rate_frame,
                                text = '{}/10'.format(self.rating),
                                **jt.header_style)
        
        ror = tk.Label(pct_frame,
                       text = str(self.ror) + '%',
                       **jt.header_style)             

        rating_label.grid(row = 0, column = 0, sticky = tk.E)
        ror.grid(row = 0, column = 0, sticky = tk.E)
        
        yframe.grid(row = 0)
        top_frame.grid(row = 1)
        lab_frame.grid(column = 0, row = 0)
        rate_frame.grid(column = 1, row = 0)
        mid_frame.grid(row = 2)
        money_frame.grid(column = 0, row = 0)
        pct_frame.grid(column = 1, row = 0)
        
    ## NOTE UI ################################################################
    ###########################################################################
    def noteUI(self, src, base = None):
        top_line = tk.Frame(src, **jt.bframe_style)
        ts_lab = tk.Label(top_line, text = 'Time Stamp >> ', **jt.detail_style)
        ts_ent = tk.Entry(top_line, width = 10)
        ts_lab.grid(column = 0, row = 0, sticky = tk.W)
        ts_ent.grid(column = 1, row = 0)
        
        quip_lab = tk.Label(top_line, text = '  Quip >> ', **jt.detail_style)
        quip_ent = tk.Entry(top_line, width = 20)
        quip_lab.grid(column = 2, row = 0)
        quip_ent.grid(column = 3, row = 0, sticky = tk.E)
        top_line.grid(row = 0, padx = 5, pady = 5)
        
        quote_frame = tk.Frame(src, **jt.bframe_style)
        quote_lab = tk.Label(quote_frame, text = '       Quote >> ', **jt.detail_style)
        quote_box = scrolledtext.ScrolledText(quote_frame, width = 30, height = 5)
        
        quote_lab.grid(column = 0, row = 0, sticky = tk.N)
        quote_box.grid(column = 1, row = 0, sticky = tk.E)
        quote_frame.grid(row = 1, padx = 5, pady = 5)
        
        desc_frame = tk.Frame(src, **jt.bframe_style)
        desc_lab = tk.Label(desc_frame, text = 'Description >> ', **jt.detail_style)
        desc_box = scrolledtext.ScrolledText(desc_frame, width = 30, height = 5)
        
        desc_lab.grid(column = 0, row = 0, sticky = tk.N)
        desc_box.grid(column = 1, row = 0, sticky = tk.E)
        desc_frame.grid(row = 2, padx = 5, pady = 5)
        
        self.note_gets = [ts_ent, quip_ent, quote_box, desc_box]
        
        if base is not None:
            ts_ent.insert(0, base.Time)
            quip_ent.insert(0, base.Quip)
            quote_box.insert('1.0', base.Quote)
            desc_box.insert('1.0', base.Interpretation)
           
##################################################################################\
## TV SHOW CHILD CLASS ############################################################)
##################################################################################/
class TVShow(Subject):
    def __init__(self, e_id, name, rating, debut_year, neps, creator, network, genre):
        super().__init__(e_id, name, rating)
        self.debut_year = debut_year
        self.num_episodes = neps
        self.creator = creator
        self.network = network
        self.genre = genre
        self.ro = jt.tags_tvshow
        self.columns = jt.sql_tvshows
        self.note_var = 'Episode'
        self.tbl = 'tvshows'
    
    ## READ UI ################################################################
    ###########################################################################
    def readUI(self, src, reading):
        ssn = tk.Label(src, 
                       text = reading.Episode, 
                       **jt.detail_style)
            
        ep = tk.Label(src, 
                      text = 'Name: {} '.format(reading.Name), 
                      **jt.detail_style)
            
        rate = tk.Label(src, 
                        text = '{}/10'.format(reading.Rating), 
                        **jt.detail_style)
            
        desc = tk.Message(src, 
                          text = reading.Description, 
                          width = 300,
                          **jt.detail_style)
        
        ssn.grid(row = 2, column = 0)
        ep.grid(row = 1, columnspan = 2)
        rate.grid(row = 2, column = 1)
        desc.grid(row = 3, columnspan = 2)
 
    ## ENTRY UI ###############################################################
    ###########################################################################   
    def entryUI(self, src):
        show_name = CreateEntry(src, 'Show Name', self.ro, self.name)
        year = CreateEntry(src, 'Debut Year', self.ro, self.debut_year)
        eps = CreateEntry(src, 'No. Episodes', self.ro, self.num_episodes)
        creator = CreateEntry(src, 'Creator', self.ro, self.creator)
        network = CreateEntry(src, 'Network', self.ro, self.network)
        genre = CreateEntry(src, 'Genre', self.ro, self.genre)
        rating = CreateRate(src, 'Rating', self.ro, self.rating)
        
        self.detail_gets = {'name': show_name,
                            'rating': rating,
                            'debut_year': year, 
                            'num_episodes': eps,
                            'creator': creator,
                            'network': network,
                            'genre': genre}

    ## VIEW UI ################################################################
    ###########################################################################
    def viewUI(self, src):
        top_frame = tk.Frame(src, **jt.bframe_style)
        lab_frame = tk.Frame(top_frame, **jt.bframe_style)
        rate_frame = tk.Frame(top_frame, **jt.bframe_style)
        mid_frame = tk.Frame(src, **jt.bframe_style)
        
        self.pair_create(lab_frame, 'Creator', self.creator, 0)          
        self.pair_create(lab_frame, 'Debut Year', self.debut_year, 1)       
        self.pair_create(mid_frame, 'Network', self.network, 0)
        self.pair_create(mid_frame, 'Genre', self.genre, 1)
        self.pair_create(mid_frame, 'No. Episodes', self.num_episodes, 2)
        
        rating_label = tk.Label(rate_frame,
                                text = '{}/10'.format(self.rating),
                                **jt.header_style)

        rating_label.grid(row = 0, column = 0, sticky = tk.E)        
        
        top_frame.grid(row = 0)
        lab_frame.grid(column = 0, row = 0)
        rate_frame.grid(column = 1, row = 0)
        mid_frame.grid(row = 1)
        
    ## NOTE UI ################################################################
    ###########################################################################
    def noteUI(self, src, base = None):
        top_line = tk.Frame(src, **jt.bframe_style)
        s_lab = tk.Label(top_line, text = '         S', **jt.detail_style)
        s_ent = tk.Entry(top_line, width = 3)
        s_lab.grid(column = 0, row = 0, sticky = tk.S)
        s_ent.grid(column = 1, row = 0, sticky = tk.S)
        
        e_lab = tk.Label(top_line, text = 'E', **jt.detail_style)
        e_ent = tk.Entry(top_line, width = 3)
        e_lab.grid(column = 2, row = 0, sticky = tk.S)
        e_ent.grid(column = 3, row = 0, sticky = tk.S)
        
        ep_rate = tk.Scale(top_line, 
                           orient = tk.HORIZONTAL, 
                           from_ = 0, to = 10, 
                           **jt.scale_style)
        
        ep_rate.grid(column = 4, row = 0, sticky = tk.E, padx = 25) 
        
        name_lab = tk.Label(top_line, text = 'Episode Name >> ', **jt.detail_style)
        name_ent = tk.Entry(top_line, width = 22)
        name_lab.grid(row = 1, columnspan = 4, pady = 6)
        name_ent.grid(row = 1, column = 4, pady = 6)
        
        top_line.grid(row = 0, padx = 5)
        
        desc_frame = tk.Frame(src, **jt.bframe_style)
        desc_lab = tk.Label(desc_frame, text = 'Description >> ', **jt.detail_style)
        desc_box = scrolledtext.ScrolledText(desc_frame, width = 30, height = 10)
        
        desc_lab.grid(column = 0, row = 0, sticky = tk.N)
        desc_box.grid(column = 1, row = 0, sticky = tk.E)
        desc_frame.grid(row = 1, padx = 5, pady = 5)
        
        self.note_gets = [s_ent, e_ent, name_ent, ep_rate, desc_box]
        
        if base is not None:
            s_ent.insert(0, base.nfind('s'))
            e_ent.insert(0, base.nfind('e'))
            name_ent.insert(0, base.Name)
            ep_rate.set(int(base.Rating))
            desc_box.insert('1.0', base.Description)
           
##################################################################################\
## RESTAURANT CHILD CLASS #########################################################)
##################################################################################/
class Food(Subject):
    def __init__(self, e_id, name, rating, city, cuisine, experience):
        super().__init__(e_id, name, rating)
        self.city = city
        self.cuisine = cuisine
        self.experience = experience
        self.ro = jt.tags_food
        self.columns = jt.sql_food
        self.note_var = 'Meal'
        self.tbl = 'restaurants'
        self.exps = ('Fast Food', 
                     'Casual Dining', 
                     'Casual Sit Down', 
                     'Formal Sit Down')
        
        self.courses = ('Appetizer', 
                        'Main Course', 
                        'Dessert', 
                        'Drinks')
        
        self.ratio = {'Appetizer': 1.43,
                      'Main Course': 1,
                      'Dessert': 1.666666,
                      'Drinks': 2.5}
        
        self.organized = {i: [n for n in self.notes if n.Course == i] for i in self.courses}
        
        pprops = []
        for c in self.courses:
            if len(self.organized[c]) > 0:
                prices = [float(n.Cost) for n in self.organized[c]]
                pmean = (sum(prices) / max(1, len(prices))) * self.ratio[c]
                pprops.append(pmean)
        
        self.food_cost = round(np.mean(pprops), 2)
        self.food_rate = int(np.mean([int(n.Rating) for n in self.notes]))
    
    ## READ UI ################################################################
    ###########################################################################
    def readUI(self, src, reading):
        course = tk.Label(src, 
                       text = reading.Course,
                       **jt.message_style)
            
        name = tk.Label(src, 
                      text = reading.Name,
                      **jt.message_style)
            
        cost = tk.Label(src, 
                          text = cashify(reading.Cost),
                          **jt.message_style)
            
        rate = tk.Label(src, 
                          text = "{}/10".format(reading.Rating),
                          **jt.message_style)
        
        course.grid(row = 2, columnspan = 3)
        name.grid(row = 1, columnspan = 3)
        cost.grid(row = 3, columnspan = 3)
        rate.grid(row = 4, columnspan = 3)
              
    ## ENTRY UI ###############################################################
    ###########################################################################   
    def entryUI(self, src):
        rest_name = CreateEntry(src, 'Restaurant Name', self.ro, self.name)
        rating = CreateRate(src, 'Rating', self.ro, self.rating)
        city = CreateEntry(src, 'City', self.ro, self.city)
        cuisine = CreateEntry(src, 'Cuisine', self.ro, self.cuisine)
        experience = CreateDrop(src, 'Experience', self.ro, self.exps, self.experience)
        
        self.detail_gets = {'name': rest_name,
                            'rating': rating,
                            'city': city,
                            'cuisine': cuisine,
                            'experience': experience}
        
    ## VIEW UI ################################################################
    ###########################################################################    
    def viewUI(self, src):
        top_frame = tk.Frame(src, **jt.bframe_style)
        lab_frame = tk.Frame(top_frame, **jt.bframe_style)
        rate_frame = tk.Frame(top_frame, **jt.bframe_style)
        mid_frame = tk.Frame(src, **jt.bframe_style)
        
        self.pair_create(lab_frame, 'City', self.city, 0)          
        self.pair_create(lab_frame, 'Cuisine', self.cuisine, 1)
        self.pair_create(lab_frame, 'Experience', self.experience, 2)
        
        rating_label = tk.Label(rate_frame,
                                text = '{}/10'.format(self.rating),
                                **jt.header_style)

        rating_label.grid(row = 0, column = 0, sticky = tk.E)   
            
        avgcost_lab = tk.Label(mid_frame, text = 'Approx. Cost', **jt.message_style)
        avgcost = tk.Label(mid_frame, text = '${}'.format(self.food_cost), **jt.message_style)
        
        avgrate_lab = tk.Label(mid_frame, text = 'Food Rating', **jt.message_style)
        avgrate = tk.Label(mid_frame, text = '{}/10'.format(self.food_rate), **jt.message_style)
        
        avgcost_lab.grid(row = 0, column = 0, padx = 10)
        avgcost.grid(row = 1, column = 0, padx = 10)
        avgrate_lab.grid(row = 0, column = 1, padx = 10)
        avgrate.grid(row = 1, column = 1, padx = 10)
        
        top_frame.grid(row = 0)
        lab_frame.grid(column = 0, row = 0)
        rate_frame.grid(column = 1, row = 0)
        mid_frame.grid(row = 1, pady = 10)
    
    ## NOTE UI ################################################################
    ###########################################################################
    def noteUI(self, src, base = None):
        format_frame = tk.Frame(src, **jt.bframe_style)
        name_lab = tk.Label(format_frame, text = 'Name >> ', **jt.detail_style)
        name_ent = tk.Entry(format_frame, width = 20)
        course_lab = tk.Label(format_frame, text = 'Course >> ', **jt.detail_style)
        course_box = ttk.Combobox(format_frame, width = 12)
        course_box['values'] = self.courses
        course_box.current(0)
        
        name_lab.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
        name_ent.grid(row = 0, column = 1, sticky = tk.E, pady = 2)
        course_lab.grid(row = 1, column = 0, sticky = tk.W, pady = 2)
        course_box.grid(row = 1, column = 1, sticky = tk.E, pady = 2) 
        
        cost_lab = tk.Label(format_frame, text = 'Cost >> ', **jt.detail_style)
        cost_ent = tk.Entry(format_frame, width = 10)
        
        rating = tk.Scale(format_frame, 
                          from_ = 0, to = 10, 
                          orient = tk.HORIZONTAL, 
                          **jt.scale_style)
        
        cost_lab.grid(row = 2, column = 0, sticky = tk.W, pady = 2)
        cost_ent.grid(row = 2, column = 1, sticky = tk.E, pady = 2)
        rating.grid(row = 3, columnspan = 2, pady = 2)
 
        self.note_gets = [name_ent, course_box, cost_ent, rating]
        
        if base is not None:
            name_ent.insert(0, base.Name)
            cdex = self.courses.index(base.Course)
            course_box.current(cdex)
            cost_ent.insert(0, base.Cost)
            rating.set(int(base.Rating))
            
        format_frame.grid(padx = 10, pady = 10)
           
##################################################################################\
## OTHER CHILD CLASS ##############################################################)
##################################################################################/
class Other(Subject):
    def __init__(self, e_id, name, rating):
        super().__init__(e_id, name, rating)
        self.ro = jt.tags_other
        self.note_var = 'Note'
    
    ## READ UI ################################################################
    ###########################################################################
    def readUI(self, src, reading):
        pass
              
    ## ENTRY UI ###############################################################
    ###########################################################################   
    def entryUI(self, src):
        ename = CreateEntry(src, 'Name', self.ro, self.name)
        notes = CreateEntry(src, 'Notes', self.ro, self.tags)
        
        self.detail_gets = {'name': ename, 
                            'notes': notes}
    
    ## VIEW UI ################################################################
    ###########################################################################    
    def viewUI(self, src):
        pass
    
    ## NOTE UI ################################################################
    ###########################################################################
    def noteUI(self, src):
        pass

##############################################################################\
###############################################################################
##                              FUNCTIONS                                    ##                                
###############################################################################
##############################################################################/
def class_fill(src_tbl, tuple_data):
    """Takes the tuple data pulled from a SQLite fetch request and uses it to
    populate one of the above classes"""
    funnel = {'books': Book,
              'movies': Movie,
              'tvshows': TVShow,
              'restaurants': Food}
    
    return funnel[src_tbl](*tuple_data)

###############################################################################
###############################################################################
def cashify(s):
    """Cashify: Takes a numeric string input and adds commas and a number sign"""
    if '$' in s:
        return s
    else:
        lst = list(s)
        lst.reverse()
    
        c = 3
        for i in range(int(len(lst) / 3)):
            if c < len(lst):
                lst.insert(c, ',')
                c += 4
        
        lst.reverse()
        cash = '${}'.format(''.join(lst))
        return cash

###############################################################################
###############################################################################
def idfy(n):
    """Identify: creates a **hopefully** uniqe ID for each journal entry.
    Input a number length and it picks random digits, letters, and symbols"""
    x = ''
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numsym = list('0123456789-|:_=~')
    pick_from = letters + numsym
    for i in range(n):
        a = rn.choice(pick_from)
        x += a
        
    return x

############################################################################### 
###############################################################################
def bint(s):
    """Blank Int: if the value is an empty string, returns zero, else, converts
    the string to an int"""
    try:
        return int(s)
    except ValueError:
        return 0
    
###############################################################################
###############################################################################           
def SQL_pull(SELECT, FROM, WHERE = False):
    """Pull data from an SQLite table"""
    if WHERE != False:
        w = ' WHERE {}'.format(WHERE)
    else:
        w = ''
        
    db_file = jt.file_location + jt.file_name
    conn = sql.connect(db_file)
    click = conn.cursor()    
    code = "SELECT {} FROM {}{}".format(SELECT, FROM, w)
    click.execute(code)
    data = click.fetchall()
    conn.close()
    
    return data

###############################################################################
###############################################################################
def SQL_run(code):
    """Runs any generic SQL code"""
    db_file = jt.file_location + jt.file_name
    conn = sql.connect(db_file)
    click = conn.cursor()
    click.execute(code)
    conn.commit()
    conn.close()
    
###############################################################################
###############################################################################
def SQL_insert(data, tbl):
    """Inserts new rows to a given SQLite table"""
    a = {'E': jsql.insert_entry,
         'N': jsql.insert_note,
         'M': jsql.insert_movie,
         'B': jsql.insert_book,
         'T': jsql.insert_tvshow,
         'R': jsql.insert_restaurant}
    
    db_file = jt.file_location + jt.file_name
    conn = sql.connect(db_file)
    cur = conn.cursor()
    code = a[tbl.upper()]
    cur.execute(code, data)
    conn.commit()
    conn.close()
    