# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 07:47:26 2019

@author: Devlin
"""
###############\_________
import json  ############\_______
import sqlite3 as sql  ##########\
import journal_template as jt  ###\_______________________________________________
##################################################################################
##!____________________________________________________________________________!##
##|     So one of the draws of this project is to help me learn SQL. I have no |##
##| prior experience with SQL or SQLite so these first few functions I found   |##
##| online. I forget where but I'm not smart enough to write it for myself yet.|##
##|____________________________________________________________________________|##
##################################################################################
def create_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file)
        print(sql.version_info)
    except sql.Error as e:
        print('----Connector----')
        print(e)
    finally:
        if conn:
            conn.close()

###############################################################################
###############################################################################           
def open_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file)
        return conn
    except sql.Error as e:
        print('----Opener----')
        print(e)
        
    return conn

###############################################################################
###############################################################################
def create_table(conn, layout):
    try:
        c = conn.cursor()
        c.execute(layout)
    except sql.Error as e:
        print('----Creator----')
        print(e)

###############################################################################
###############################################################################     
def create_row(conn, table, code):
    cur = conn.cursor()
    cur.execute(code, table)
    return cur.lastrowid

##################################################################################/
## SQLite CODE ##################################################################/ 
################################################################################/  
table_entries = """CREATE TABLE IF NOT EXISTS entries (
                   entry_id integer PRIMARY KEY,
                   subject_id text NOT NULL,
                   title text NOT NULL,
                   date text NOT NULL,
                   body text NOT NULL
                   );"""

insert_entry = """INSERT INTO entries(subject_id, title, date, body)
                  VALUES(?, ?, ?, ?)"""

table_notes = """CREATE TABLE IF NOT EXISTS notes (
                 note_id integer PRIMARY KEY,
                 subject_id text NOT NULL,
                 category text NOT NULL,
                 item1 text,
                 item2 text,
                 item3 text,
                 item4 text
                 );"""

# This one I modified after I ran this script. I changed the layout of the
# notes table in the sqlite3 shell, replacing category with home_tbl
insert_note = """INSERT INTO notes(subject_id, home_tbl, item1, item2, item3, item4)
                 VALUES(?, ?, ?, ?, ?, ?)"""

table_books = """CREATE TABLE IF NOT EXISTS books (
                 subject_id text PRIMARY KEY,
                 name text NOT NULL,
                 rating integer NOT NULL,
                 author text,
                 pub_year text,
                 pages text,
                 isbn text,
                 genre text
                 );"""

insert_book = """INSERT INTO books(subject_id, name, rating, author, pub_year, pages, isbn, genre)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""

table_movies = """CREATE TABLE IF NOT EXISTS movies (
                 subject_id text PRIMARY KEY,
                 name text NOT NULL,
                 rating integer NOT NULL,
                 release_year text,
                 director text,
                 lead text,
                 genre text,
                 budget text,
                 boxoffice text
                 );""" 

insert_movie = """INSERT INTO movies(subject_id, name, rating, release_year, director, lead, genre, budget, boxoffice)
                  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""

table_tvshow = """CREATE TABLE IF NOT EXISTS tvshows (
                  subject_id text PRIMARY KEY,
                  name text NOT NULL,
                  rating integer NOT NULL,
                  debut_year text,
                  num_episodes text,
                  creator text,
                  network text,
                  genre text
                  );""" 

insert_tvshow = """INSERT INTO tvshows(subject_id, name, rating, creator, network, debut_year, num_episodes, genre)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""

table_restaurant = """CREATE TABLE IF NOT EXISTS restaurants (
                      subject_id text PRIMARY KEY,
                      name text NOT NULL,
                      rating integer NOT NULL,
                      city text,
                      cuisine text,
                      experience text
                      );""" 

insert_restaurant = """INSERT INTO restaurants(subject_id, name, rating, city, cuisine, experience)
                       VALUES(?, ?, ?, ?, ?, ?)"""

all_tables = (table_entries, table_notes, table_books, 
              table_movies, table_tvshow, table_restaurant)

grouped_insert = {'Book': insert_book,
                  'Movie': insert_movie, 
                  'TV Show': insert_tvshow, 
                  'Restaurant': insert_restaurant}
#\___________________________________________________________________________/#
###\_______________________________________________________________________/###
#####\___________________________________________________________________/#####
#######\_______________________________________________________________/#######   
#########\___________________________________________________________/#########
###########\_______________________________________________________/###########  
###############################################################################
###############################################################################
def journal_setup(db_file):
    
    #---------------------------------------------------------------------#
    # So we start by restructuring the journal to fit the database tables #
    #---------------------------------------------------------------------#
    
    with open('journal.json') as file_obj:
        journal = json.load(file_obj)
     
    # The Notes Table
    note_mountain = [e['notes'] for e in journal]
    for i in range(len(note_mountain)):
        lst = note_mountain[i]
        eid = journal[i]['entry_id']
        cat = journal[i]['category']
        for note in lst:
            note['entry_id'] = eid
            note['category'] = cat
    
    notes = [n for l in note_mountain for n in l]
    
    # The Entries Table
    entry_cliff = [e['content'] for e in journal]
    for i in range(len(entry_cliff)):
        lst = entry_cliff[i]
        eid = journal[i]['entry_id']
        for entry in lst:
            entry['entry_id'] = eid
    
    entries = [e for l in entry_cliff for e in l]
    
    # The Subject Tables
    subjects = journal.copy()
    for sbjct in subjects:
        del sbjct['content']
        del sbjct['notes']
        
    grouped = {'Book': [e for e in subjects if e['category'] == 'Book'],
               'Movie': [e for e in subjects if e['category'] == 'Movie'],
               'TV Show': [e for e in subjects if e['category'] == 'TV Show'],
               'Restaurant': [e for e in subjects if e['category'] == 'Restaurant']}
    
    taged = {key: [e.pop('tags') for e in grouped[key]] for key in grouped}
    
    for key in grouped:
        lst = grouped[key]
        tags_lst = taged[key]
        for i in range(len(lst)):
            lst[i].update(tags_lst[i])
            
    
    
    #--------------------------------------------------------------------#
    # Then we create the tables using the CREATE TABLES statements above #
    #--------------------------------------------------------------------#
    
    link = open_connection(db_file)
    if link is None:
        print('Cannot connect to databse')

    for tbl in all_tables:
        create_table(link, tbl)
    
    #----------------------------------------------------------------------#
    # Last, load the current entries into the database with the code above #
    #----------------------------------------------------------------------#
    
    with link:
        # Populate Entries Table
        for e in entries:
            x = (e['entry_id'], e['title'], e['date'], e['body'])
            create_row(link, x, insert_entry)
        
        # Populate Notes Table
        deets = {'Book': jt.notes_book,
                 'Movie': jt.notes_movie,
                 'TV Show': jt.notes_tv,
                 'Restaurant': jt.notes_food}
        
        for n in notes:
            c = n['category']
            unpackable = [n[i] for i in deets[c]]
            y = (n['entry_id'], c, *unpackable)
            create_row(link, y, insert_note)
        
        # Populate Subject Tables
        info_template = {'Book': jt.tags_book,
                         'Movie': jt.tags_movie,
                         'TV Show': jt.tags_tvshow,
                         'Restaurant': jt.tags_food}
        
        for key in grouped:
            layout = info_template[key]
            for s in grouped[key]:
                info = [s[t] for t in layout if t in s.keys()]
                z = (s['entry_id'], s['name'], *info)
                create_row(link, z, grouped_insert[key])
    
###############################################################################
###############################################################################
run = False                       ## So I don't fuck up and reset everything ##
                                  #############################################

file_location = 'C:\\Users\\Devlin\\Documents\\scripts\\journal\\'
file_name = 'journal.db'
if __name__ == '__main__' and run:
    create_connection(file_location + file_name)
    journal_setup(file_location + file_name)
    