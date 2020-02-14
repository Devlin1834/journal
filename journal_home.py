# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:12:26 2019

@author: Devlin
"""

#################################\\     
# TODO - merge entry and       ##||         TV Show View Window Size
#        details add pages?    ##||          now movies do it too
#      - edit entries?         ##||         TV show tags
#      - define other          ##||\        search by ratings
####################################\
import tkinter as tk           #####|
####################################/
import journal_template as jt  ##||/
import journal_event as je     ##||
import journal_view as jv      ##||
import journal_toolkit as kit  ##||
#################################//
#################################\\____________________________________________
###############################################################################\
##           ###################################################################\
## HOME PAGE ####################################################################)
##           ###################################################################/
###############################################################################/
class Home():
    def __init__(self, master):
        self.master = master
        self.master.title('I Hope You Feel Opinionated!')
        self.frame = tk.Frame(self.master, **jt.bframe_style)
        self.session = None
        self.x = 340
        self.y = 360
        self.base_geo = (self.x, self.y)
        
        #######################################################################
        ## DATA CONTROL #######################################################
        self.counts = {}                                                     ##
        self.refference = {}     ##      Titles mapped to subject_ids        ##
        self.home_table = {}     ## subject_ids mapped to SQLite table names ##
        self.array_update(jt.sql_tables)
    
        #######################################################################
        ## TITLE ##############################################################
        ttl = tk.Label(self.frame, 
                       text = 'Opinion Record',
                       **jt.header_style)
        
        ttl.grid(row = 0, 
                 columnspan = 3)
        
        #######################################################################
        ## COMING SOON ########################################################
        self.msg = tk.Label(self.frame, 
                            text = '', 
                            **jt.message_style)
        
        self.msg.grid(row = 1, 
                      columnspan = 2)

        def coming_soon():
            self.msg.configure(text = 'Coming Soon!')
        
        #######################################################################
        ## ADD BUTTON #########################################################
        self.add_btn = tk.Button(self.frame, 
                                 text = 'Add Thoughts', 
                                 command = self.open_chooser, 
                                 **jt.button_style,
                                 width = 15)
        
        self.add_btn.grid(column = 0, 
                          row = 4, 
                          padx = 10, 
                          pady = 5)
        
        self.clicked = False
        
        #######################################################################
        ## ANALYZE BUTTON #####################################################
        self.anal_btn = tk.Button(self.frame, 
                                  text = 'Thought Stats', 
                                  command = coming_soon, 
                                  **jt.button_style,
                                  width = 15)
        
        self.anal_btn.grid(column = 1, 
                           row = 4, 
                           padx = 10, 
                           pady = 5)
        
        #######################################################################
        ## LIST BOX ###########################################################
        self.thoughts_lst = tk.Listbox(self.frame, 
                                       selectmode = tk.SINGLE, 
                                       width = 40)
        
        self.thoughts_lst.grid(columnspan = 2, 
                               row = 3, 
                               padx = 10,
                               pady = 10)
        
        for thought in sorted(self.refference.keys()):
            self.thoughts_lst.insert(tk.END, thought)
        
        #######################################################################
        ## VIEW BUTTON ########################################################
        self.view_btn = tk.Button(self.frame, 
                                  text = 'View Thoughts', 
                                  command = self.open_viewer, 
                                  **jt.button_style,
                                  width = 15)
        
        self.view_btn.grid(column = 1, 
                           row = 2, 
                           padx = 10, 
                           pady = 5)
        
        #######################################################################
        ## SEARCH BUTTON ######################################################
        self.search_btn = tk.Button(self.frame,
                                    text = 'Search Thoughts',
                                    command = self.open_looker,
                                    **jt.button_style,
                                    width = 15)
        
        self.search_btn.grid(row = 2,
                             column = 0,
                             padx = 10,
                             pady = 5)
        
        self.pushed = False
        
        #######################################################################
        ## FRAME PACK #########################################################
        self.frame.grid(row = 0, column = 0, padx = 18)

##||#################################################################################\
##:|## SEARCH FRAME ##################################################################)
##||## This one is a doozy, sorry future me. It establishes 4 frames with  ##########/
##:|## iteratively created checkboxes in each of them. At the head of      #########/
##||## frame is a label displaying the count for each category and a "BIG  ########/
##:|## BOOL" which is a larger checkbox to toggle all the sub-boxes.       #######/
##||## There are 3 supporting functions for this section...                ######/
##:|##   (1) Populate Filter - to create the sub-boxes                     #####/
##||##   (2) Checked - Checks or unchecks other boxes conditionally        ####/
##:|##   (3) Filter Thoughts - Refreshes the listbox based on the search   ###/
##||#########################################################################/
##:|## BASE FUNCTION #######################################################/
    def open_looker(self):
        if self.pushed:
            self.search_btn.configure(**jt.button_style)
            self.msg.configure(text = '')
            self.search_frame.destroy()
            self.master.geometry(self.resize())
        elif self.clicked:
            self.msg.configure(text = 'Close the Add Window Please')
            self.pushed = not self.pushed
        else:
            self.search_btn.configure(**jt.active_button)
            self.msg.configure(text = 'Filter Entries')
            self.search_frame = tk.Frame(self.master, **jt.bframe_style)
            self.master.geometry(self.resize(xplus = 475))
            
            ###################################################################
            ## MOVIES #########################################################
            t = 'movies'
            movie_frame = tk.Frame(self.search_frame)
            self.all_movies = tk.BooleanVar()
            self.all_movies.set(True)
            self.movie_boxes = self.populate_filter(movie_frame, 'genre', t)
            
            txt = '{} {}'.format(self.counts[t], t.capitalize())
            movie_msg = tk.Label(movie_frame, 
                                 text = txt, 
                                 **jt.message_style)
            
            mtotal = tk.Checkbutton(movie_frame,
                                    text = t.capitalize(),
                                    variable = self.all_movies,
                                    command = lambda x = t: self.checked(x),
                                    **jt.check_style)
            
            movie_msg.grid(row = 0, sticky = tk.W)
            mtotal.grid(row = 1, sticky = tk.W, pady = 5)
            
            movie_frame.configure(**jt.bframe_style)
            movie_frame.grid(row = 0, column = 0, sticky = tk.N, padx = 5)
            
            ###################################################################
            ## TV SHOWS #######################################################
            t = 'tvshows'
            tv_frame = tk.Frame(self.search_frame)
            self.all_tv = tk.BooleanVar()
            self.all_tv.set(True)
            self.tv_boxes = self.populate_filter(tv_frame, 'genre', t)
            
            txt = '{} {}'.format(self.counts[t], 'TV Shows')
            tv_msg = tk.Label(tv_frame, 
                              text = txt, 
                              **jt.message_style)
            
            ttotal = tk.Checkbutton(tv_frame,
                                    text = 'TV Shows',
                                    variable = self.all_tv,
                                    command = lambda x = t: self.checked(x),
                                    **jt.check_style)
            
            tv_msg.grid(row = 0, sticky = tk.W)
            ttotal.grid(row = 1, sticky = tk.W, pady = 5)
            
            tv_frame.configure(**jt.bframe_style)
            tv_frame.grid(row = 0, column = 1, sticky = tk.N, padx = 5)
            
            ###################################################################
            ## BOOKS ##########################################################
            t = 'books'
            book_frame = tk.Frame(self.search_frame)
            self.all_books = tk.BooleanVar()
            self.all_books.set(True)
            self.book_boxes = self.populate_filter(book_frame, 'genre', t)
            
            txt = '{} {}'.format(self.counts[t], t.capitalize())
            book_msg = tk.Label(book_frame, 
                                text = txt,
                                **jt.message_style)
            
            btotal = tk.Checkbutton(book_frame,
                                    text = t.capitalize(),
                                    variable = self.all_books,
                                    command = lambda x = t: self.checked(x),
                                    **jt.check_style)
            
            book_msg.grid(row = 0, sticky = tk.W)
            btotal.grid(row = 1, sticky = tk.W, pady = 5)
            
            book_frame.configure(**jt.bframe_style)
            book_frame.grid(row = 0, column = 2, sticky = tk.N, padx = 5)
            
            ###################################################################
            ## FOOD ###########################################################
            t = 'restaurants'
            food_frame = tk.Frame(self.search_frame)
            self.all_food = tk.BooleanVar()
            self.all_food.set(True)
            self.food_boxes = self.populate_filter(food_frame, 'cuisine', t)
            
            txt = '{} {}'.format(self.counts[t], t.capitalize())
            food_msg = tk.Label(food_frame, 
                                text = txt, 
                                **jt.message_style)
            
            ftotal = tk.Checkbutton(food_frame,
                                    text = t.capitalize(),
                                    variable = self.all_food,
                                    command = lambda x = t: self.checked(x),
                                    **jt.check_style)
            
            food_msg.grid(row = 0, sticky = tk.W)
            ftotal.grid(row = 1, sticky = tk.W, pady = 5)
            
            food_frame.configure(**jt.bframe_style)
            food_frame.grid(row = 0, column = 3, sticky = tk.N, padx = 5)
            
            ###################################################################
            ## SUMMARY ARRAYS #################################################
            self.boxes = {'movies': self.movie_boxes,
                          'tvshows': self.tv_boxes,
                          'books': self.book_boxes,
                          'restaurants': self.food_boxes}
        
            self.BIG = {'movies': self.all_movies,
                        'tvshows': self.all_tv,
                        'books': self.all_books,
                        'restaurants': self.all_food}
        
            self.catcounts = {'movies': movie_msg,
                              'tvshows': tv_msg,
                              'books': book_msg,
                              'restaurants': food_msg}
        
            self.rcols = {'movies': 'genre',
                          'tvshows': 'genre',
                          'books': 'genre',
                          'restaurants': 'cuisine'}
            
            ###################################################################
            ## FINALIZE FRAME #################################################
            filter_btn = tk.Button(self.search_frame,
                                   text = 'Filter Entries',
                                   command = self.filter_thoughts,
                                   **jt.button_style)
            
            filter_btn.grid(row = 1, columnspan = 4, pady = 10)
            
            self.search_frame.grid(column = 1, row = 0)
    
        self.pushed = not self.pushed
        
    ###########################################################################\
    ## POPULATE FILTER #########################################################)
    ###########################################################################/
    def populate_filter(self, src, col, tbl):
        """Creates one checkbox for each item in a SQLite table column. Returns
        an array where these items are mapped to their respective BooleanVars.
        Checkboxes are empowered with the same Checked function as the BIG BOOL
        boxes except we pass a couple more arguments to change its effect."""
        sub_cats = set([c for l in kit.SQL_pull(col, tbl) for c in l])
        select = {g: tk.BooleanVar() for g in sub_cats}
        for key in select:
            select[key].set(True)
                
        line = 1
        for g in sub_cats:
            line += 1
            tk.Checkbutton(src,
                           text = g,
                           variable = select[g],
                           command = lambda x = tbl,
                                            y = False,
                                            z = select: self.checked(x, y, z),
                           **jt.filter_style).grid(row = line, 
                                                   sticky = tk.W)
            
        return select

    ###########################################################################\
    ## CHECKED #################################################################)
    ###########################################################################/
    def checked(self, tbl, big = True, array = ''):   
        """Is used to check or uncheck search boxes conditionally.
        
        For the Big Bools - denoted by Big = True - checking it should check
        all the sub-boxes, and vice versa.
        
        For the sub-boxes - denoted by Big = False - unchecking it should uncheck
        the Big Bool and checking it should check the Big Bool if all the other
        sub-boxes are already checked.
        
        Finally, it updates the counter message with the new count."""
        selectall = self.BIG[tbl]
        counter = self.catcounts[tbl]
        rtag = self.rcols[tbl]
        
        if big:
            array = self.boxes[tbl]
            all_bools = [i.get() for i in array.values()]
            if sum(all_bools) in [0, len(all_bools)] or selectall.get():
                for bvar in array.values():
                    bvar.set(selectall.get())
        else:
            all_bools = [array[k].get() for k in array]
            if selectall.get():
                selectall.set(False)
            elif not selectall.get() and sum(all_bools) == len(all_bools):
                selectall.set(True)
            
        if selectall.get():
            num = len(kit.SQL_pull('*', tbl))
        else:
            to_count = [key for key in array if array[key].get()]
            in_str = '("' + '", "'.join(to_count) + '")'
            code = '{} IN {}'.format(rtag, in_str)
            num = len(kit.SQL_pull('*', tbl, code))
            
        if tbl == 'tvshows':
            label = 'TV Shows'
        else:
            label = tbl.capitalize()
            
        counter.configure(text = '{} {}'.format(num, label))
    
    ###########################################################################\
    ## FILTER THOUGHTS #########################################################)
    ###########################################################################/
    def filter_thoughts(self):
        """Refreshes self.refference and self.home_table with only the subjects
        that match the checked search boxes"""
        relevant_tbls = ['movies', 'tvshows', 'books', 'restaurants']
        relevant_bool = [self.all_movies.get(), self.all_tv.get(), 
                         self.all_books.get(), self.all_food.get()]
        
        filtered_tbls = [relevant_tbls[i] for i in range(len(relevant_tbls)) if relevant_bool[i]]
        self.refference = {}
        self.home_table = {}
        self.array_update(filtered_tbls)
        
        relevant_cols = ['genre', 'genre', 'genre', 'cuisine']
        tag_filter = [self.movie_boxes, self.tv_boxes, 
                      self.book_boxes, self.food_boxes]
        
        for array in tag_filter:
            dex = tag_filter.index(array)
            tbl = relevant_tbls[dex]
            col = relevant_cols[dex]
            allowed_tags = []
            for key in array:
                if array[key].get():
                    allowed_tags.append(key)
            
            in_str = '("' + '", "'.join(allowed_tags) + '")'
            code = '{} IN {}'.format(col, in_str)
            filtered = kit.SQL_pull('name, subject_id', tbl, code)
            r = {i[0]: i[1] for i in filtered}
            h = {i[1]: tbl for i in filtered}
            self.refference.update(r)
            self.home_table.update(h)
        
        if len(self.refference) == 0:
            self.array_update(jt.sql_tables)
        
        self.thoughts_lst.delete(0, tk.END)
        for thought in sorted(self.refference.keys()):
            self.thoughts_lst.insert(tk.END, thought)
            
#(==)##########################################################################\
##)(## ARRAY UPDATE ############################################################)
#(==)##########################################################################/
    def array_update(self, table_list):
        """Takes a list of tables and refreshes self.refference and 
        self.home_tables with all the entries in those tables"""
        for tbl in table_list:
            x = kit.SQL_pull('name, subject_id', tbl)
            r = {i[0]: i[1] for i in x}
            h = {i[1]: tbl for i in x}
                
            self.refference.update(r)
            self.home_table.update(h)
            
            self.counts[tbl] = len(x)
            
##|>|##########################################################################\
##|<|# OPEN CHOOSER ############################################################)
##|>|# Creates the frame with buttons for creating new entries.         #######/
##|<|# Creates one button for each table listen in jt.sql_table and     ######/
##|>|# changes the styling of the button based on its clicked condition #####/
##|<|#######################################################################/
    def open_chooser(self):
        if self.clicked:
            self.add_btn.configure(**jt.button_style)
            self.msg.configure(text = '')
            self.choose_frame.destroy()
            self.master.geometry(self.resize())
        elif self.pushed:
            self.msg.configure(text = 'Close the Search Window Please')
            self.clicked = not self.clicked
        else:
            self.add_btn.configure(**jt.active_button)
            self.msg.configure(text = "What are you thinking about?")
            self.choose_frame = tk.Frame(self.master, **jt.bframe_style)
            self.master.geometry(self.resize(yplus = 70))
            
            ###################################################################
            ## CHOOSER ########################################################
            stack = 0
            line = 0
            for tbl in jt.sql_tables:
                if tbl == 'tvshow':
                    txt = 'TV Show'
                else:
                    txt = tbl[:-1].capitalize()
                    
                b = tk.Button(self.choose_frame, 
                              text = txt, 
                              command = lambda x = tbl: self.open_editor(x),
                              **jt.button_style,
                              width = 15)
    
                b.grid(row = line,
                       column = stack,
                       pady = 2.5,
                       padx = 10)
    
                if stack:
                    line += 1
           
                stack = not stack
        
            self.choose_frame.grid(row = 1)
            
        self.clicked = not self.clicked
            
##|)###########################################################################\
#(|### OPEN EDITOR #############################################################)
##|)###########################################################################/
    def open_editor(self, tbl):
        """Opens a new editor window based on the button you press in the
        Chooser frame"""
        self.choose_frame.destroy()
        self.master.geometry(self.resize())
        self.session = tk.Toplevel(self.master, **jt.bframe_style)
        self.clicked = False
        je.Editor(self.session, tbl)
     
#\|/###########################################################################\
##X### OPEN VIEWER #############################################################)
#/|\###########################################################################/
    def open_viewer(self):
        """Loads the data for your selection, opens and populates a view window
        with that data"""
        choice = self.thoughts_lst.get(tk.ACTIVE)
        subject = self.refference[choice]
        tbl = self.home_table[subject]
        view = kit.SQL_pull('*', tbl, 'subject_id = "{}"'.format(subject))
        obj = kit.class_fill(tbl, view[0])
        self.session = tk.Toplevel(self.master, **jt.bframe_style)
        jv.Viewer(self.session, obj)
        
            
#[:]###########################################################################\
#|||## RESIZE ##################################################################)
#[:]###########################################################################/
    def resize(self, xplus = 0, yplus = 0):
        """Changes the window size or resets it super easily. I love it"""
        if xplus + yplus == 0:
            self.x, self.y = self.base_geo
        else:
            self.x += xplus
            self.y += yplus
        
        return '{}x{}'.format(self.x, self.y)
            
#############################################################################\
##      ######################################################################\
## MAIN #######################################################################)
##      ######################################################################/
#############################################################################/
def main():
    """They told me to make a main. So I did. I still don't know why..."""
    root = tk.Tk()
    app = Home(root)
    root.geometry(app.resize())
    root.configure(background = jt.color_background)
    root.mainloop()

###############################################################################
## IF NAME EQUALS EQUALS MAIN #################################################
if __name__ == '__main__': 
    main()  