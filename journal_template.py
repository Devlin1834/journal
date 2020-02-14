# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:32:20 2019

@author: Devlin
"""
#######################|
import time as t     ##|___
###########################|
import tkinter as tk     ##|______
##################################|   This is all the formatting code. The stuff
## SCHEME ########################| that makes the GUI look so pretty. It has 
hour = t.localtime().tm_hour    ##| A light mode and a dark mode for day/night
if hour == 0 or hour > 13:      ##| work - although I still need to learn how
    scheme = 'Dark'             ##| to color entry widgets any color but white.
else:                           ##| The dark scheme is programmed to run from
    scheme = 'Light'            ##| 7pm - 7am but my computers clock is set to
##################################| EST and I live in GMT so I adjusted for that 
##################################| to the left. Verdana is chosen becuase 
TFont = 'Verdana'              ###/ Sans-Serif fonts are easier to read, in my 
font_title = (TFont, 25)       ##/ opinion. I think it's a more natural shape,
font_message = (TFont, 12)     ##| although I do switch to TNR for the reader
font_button = (TFont, 10)      ##| windows. 
font_small = (TFont, 8)        ##|   
                               ##\_______   Besides containing all the pretty
#########################################\  formatting variables, this script
cbg_base = {'Light': '#dddddd',       #####\  also holds all my general use 
            'Dark': '#141521'}          #####\  variables, mostly defining the
                                          #####\  options available for entries
cbg_read = {'Light': '#f3f3f3',             #####\
            'Dark': '#f2f1fc'}                #####\   A note on something that
                                                 ##| is confusing. I use the 
cbg_active = {'Light': '#626262',                ##| terms entry subject source
              'Dark': '#717274'}                 ##| and thought interchangebly
                                                 ##| in some places. This isn't
color_background = cbg_base[scheme]              ##| helped by tk.Entry being a 
color_background_read = cbg_read[scheme]         ##| thing. In general Thoughts
color_background_active = cbg_active[scheme]     ##| are write ups, entries are
###################################################/ subjects and source is a 
##################################################( class defining the subject
###################################################\ and holding all the notes
cfg_base = {'Light': '#000000',                  ##| and writeups attributed to
            'Dark': '#faeded'}                   ##| it. BUT thoughts is hard to
                                                 ##| spell and takes a lot of
cfg_read = {'Light': '#000000',                  ##| linespace so I use entries
            'Dark': '#000000'}                   ##| for thoughts too. Think of
                                                 ##| it as an Entry about an 
cfg_active = {'Light': '#ffffff',                ##| Entry. Not to be confused
              'Dark': '#000000'}                 ##| with the Entry Widget which
                                                 ##| is used to add details to
color_foreground = cfg_base[scheme]              ##| the Entry about which we
color_foreground_read = cfg_read[scheme]         ##| have entries(which are 
color_foreground_active = cfg_active[scheme]     ##| technically thoughts).
###################################################/          ENJOY!

cselect = {'Light': '#ffffff',
           'Dark': '#000000'}
           
color_selector = cselect[scheme]

###############################################################################
## NORMAL STYLES ##############################################################
###############################################################################
base = dict(background = color_background,
            foreground = color_foreground)

active = dict(background = color_background_active,
              foreground = color_foreground_active)

reader_style = dict(font = ('Times', 12),
                    background = color_background_read,
                    foreground = color_foreground_read)

button_style = dict(font = font_button,
                    relief = tk.GROOVE)        

detail_style = dict(font = font_button)     

message_style = dict(font = font_message)

header_style = dict(font = font_title,
                    padx = 10,
                    pady = 10)

check_style = dict(font = font_button,
                   selectcolor = color_selector)

filter_style = dict(font = font_small,
                    selectcolor = color_selector)

scale_style = dict(highlightthickness = 0)

bframe_style = dict(background = color_background)

rframe_style = dict(background = color_background_read)

###############################################################################
## COMPLETING THE STYLES ######################################################
button_style.update(base) 
detail_style.update(base)                  
message_style.update(base)                    
header_style.update(base)                    
check_style.update(base)
scale_style.update(base)
filter_style.update(base)
active_button = button_style.copy()
active_button.update(active)

###############################################################################
## SQL TABLE COLUMN NAMES - IN ORDER ##########################################
###############################################################################   
sql_books = ('subject_id', 'name', 'rating', 'author', 'pub_year',
             'pages', 'isbn', 'genre')

sql_movies = ('subject_id', 'name', 'rating', 'release_year', 'director',
              'lead', 'genre', 'budget', 'boxoffice')

sql_tvshows = ('subject_id', 'name', 'rating', 'debut_year', 'num_episodes',
               'creator', 'network', 'genre')

sql_food = ('subject_id', 'name', 'rating', 'city', 'cuisine', 'experience')

sql_notes = ('note_id', 'subject_id', 'category', 'item1', 'item2', 'item3', 'item4')

###############################################################################
## GENERAL VARIABLE DEFINITION ################################################
###############################################################################
disallowed= ['?', '.', '/', '\\', '|', '`', '*', ':', '<', '>','!']
all_cats = ('Book', 'Movie', 'TV Show', 'Restaurant', 'Other')
sql_tables = ('books', 'movies', 'tvshows', 'restaurants')
file_location = 'C:\\Users\\Devlin\\Documents\\scripts\\journal\\'
file_name = 'journal.db'
                                             #--------------------------------#
presets = {'movies': len(sql_movies) - 1,    # Fills a blank class when we    #
           'tvshows': len(sql_tvshows) - 1,  # create a new subject. Counts   #
           'books': len(sql_books) - 1,      # the N of blank attributes to   #
           'restaurants': len(sql_food) - 1} # be filled. - 1 for subject_id  #
                                             #--------------------------------#

###############################################################################
## NOTE DESCRIPTION ###########################################################
###############################################################################
notes_book = ('Page', 'Quip', 'Quote', 'Interpretation')
notes_movie = ('Time', 'Quip', 'Quote', 'Interpretation')
notes_tv = ('Episode', 'Name', 'Rating', 'Description')
notes_food = ('Name', 'Course', 'Cost', 'Rating')
notes_other = ('Na', 'Na', 'Na', 'Na')

#############################################################################
## TAG DESCRIPTION #########################################################/ 
########################/         \_#_/            \#######################/   
tags_book = ('Book Name',           # ENTRY
             'Rating',  ############# SCALE
             'Author',              # ENTRY
             'Publication Year',  ### ENTRY
             'Page Count',          # ENTRY 
             'ISBN',  ############### ENTRY
             'Genre')               # ENTRY
                                    #------
tags_movie = ('Movie Name',  ######## ENTRY
              'Rating',             # SCALE
              'Release Year',  ###### ENTRY
              'Director',           # ENTRY 
              'Lead',  ############## ENTRY
              'Genre',              # ENTRY  
              'Budget',  ############ ENTRY
              'Box Office')         # ENTRY
                                    #------
tags_tvshow = ('Show Name',  ######## ENTRY
               'Rating',            # SCALE
               'Debut Year',  ####### ENTRY
               'No. Episodes',      # ENTRY
               'Creator',  ########## ENTRY
               'Network',           # ENTRY
               'Genre')  ############ ENTRY
                                    #------
tags_food = ('Restaurant Name',  #### ENTRY
             'Rating',              # SCALE
             'City',  ############### ENTRY
             'Cuisine',             # ENTRY
             'Experience')  ######### DROPBOX
                                    #------
tags_other = ('Name',  ############## ENTRY
              'Notes')              # ENTRY
                                    #
###############################################################################
###############################################################################