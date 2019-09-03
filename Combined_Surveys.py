#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project "Jaded Thunder" 
Date started: 28AUG19
Version: 1.0
@authors: Louis Kerner and Faith ___

"""

import sys
import time
import os 
import csv
import colorsys
import pandas as pd
import numpy as np
import random
import math 
import psychopy 
import matplotlib
matplotlib.use("Agg")
from psychopy import event, core, logging, visual, data, gui
from psychopy.core import getTime
import pygame
from pygame.locals import *

from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED,
                                FINISHED, PRESSED, RELEASED, FOREVER)
from numpy import (sin, cos, tan, log, log10, pi, average, 
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle

surveyName = "Survey Information"
surveyInfo = {'id': ''}  #This is is called below and is needed for starting the GUI
dlg = gui.DlgFromDict(dictionary = surveyInfo, title = surveyName) #creat the GUI
if dlg.OK == False:
    core.quit() # user pressed cancel
surveyInfo['surveyName'] = surveyName  

#set what the user id input into subject ID and create the survey window

subject_id = surveyInfo['id']
win = visual.Window(size =[800, 600], fullscr = False)

file_name = "vin_ratings_" + str(subject_id) + ".csv" #create save file

#set up data frame using pandas 
# TO DO: write a change directory code line to look for the csv file in folder
vignett = pd.read_csv('VignettSentences.csv') 
RandVignett = vignett.sample(frac=0.2).reset_index(drop = True) #randomizes vignette csv keeping row integrity

#opening of survey states 'press spacebar to begin' only works if spacebar is pressed
win.flip()
message = visual.TextStim(win, text = 'press spacebar to begin')
message.setAutoDraw(True)
win.flip()
event.waitKeys(keyList='space')
message.setText('')
win.flip()

instruct = 'For each of the follwing sentences, please rate how positive or negative each situation would be the scale provided'
instructions = visual.TextStim(win, text = instruct, 
                               units = 'norm'
                               )
sp_text = visual.TextStim(win, text = "pres the spacebar to continue",
                          height = .06, units = 'norm',
                          pos = (0.0, -0.7))

instructions.draw()
sp_text.draw()
win.flip()
event.waitKeys(keyList = 'space') #keyList tells the program which key press makes the 
win.flip()                        #program continue. if keylist is not present it will continue on any button press 

message = visual.TextStim(win, text = "You will now begin rating the sentences.")

message.draw()
sp_text.draw()
win.flip()
event.waitKeys(keyList = 'space')
# takes the message draws it, takes the sp_text draws it and then winflip makes it show on the screen
nTrials = RandVignett.shape[0] #returns the amount of rows in my data frame 

#set up emptey arrays of variables
responses = []
ids = []
vinNums = []
vinTypes = []
vins = []

#start the trial loop
for n in range(0, nTrials):
    question = RandVignett.loc[n, 'questionText']
    vinNum = RandVignett.loc[n, 'VinNum']
    vinType = RandVignett.loc[n, 'VinType']
    
    s1 = visual.TextStim(win, text= 'very negative', height=.04, units='norm', pos =(-0.5, -0.45))
    s2 = visual.TextStim(win, text= 'slightly negative', height=.04, units='norm', pos = (-0.2, -0.45))
    s3 = visual.TextStim(win, text= 'slightly positive', height=.04, units='norm', pos = (0.2, -0.45))
    s4 = visual.TextStim(win, text= 'very positive', height=.04, units='norm', pos = (0.5, -0.45))

    q_scale = visual.RatingScale(win, low = 1, high = 4, stretch = 2, scale = False, labels = False, singleClick = True)

    q = visual.TextStim(win, text=question, height=.10, units='norm')
    
    while q_scale.noResponse: # show & update until a response has been made
        q.draw()
        s1.draw()
        s2.draw()
        s3.draw()
        s4.draw()
        q_scale.draw()
        win.flip()

    response = q_scale.getRating()
    
    responses.append(response)
    ids.append(subject_id)
    vinNums.append(vinNum)
    vinTypes.append(vinType)
    vins.append(question)
    
    win.flip()

#create data frame with responses and with their associated vignette     
vinData = pd.DataFrame({'id' : ids,
                     'response' : responses,
                     'vingette_type' : vinTypes,
                     'vignette_number' : vinNums,
                     'vignette' : vins})
#Take the data frame and turn it into a csv file
vinData.to_csv(file_name, sep = ',', index = False, na_rep = 'na', header = True)

win.close()
core.quit()