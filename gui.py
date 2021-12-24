# Python Spellcheck Application
# Andrew Flores
# Created for ECE528 Final Project FA21
# Colorado State University
# Last updated: 12/13/21


import re
import time
from tkinter import *
from autocorrect import SpellChecker
from generator import TextGeneration


# Flush outputs
def flush(event):
  clear_predictions()
  clear_suggestions()
  take_input()

# Return if word is in English dictionary
def spelled_correctly(word):
   return re.sub('[^a-zA-Z0-9\']+', '', word).lower() in checker.get_vocab()

# Replace word in input Text box
def replace(suggestion=None, word=None):
  if suggestion == None or word == None:
    return
  else:
    INPUT = input.get('1.0', END)
    input.replace('1.0', END, INPUT.replace(word, suggestion))
    take_input()

# Clears output and places text into output from input
def take_input():
  global result # Reference global result variable

  start_time = time.time()# Start execution timer

  INPUT = input.get("1.0", "end-1c").strip() # Grab all input
  # Split input into word list by whitespace
  inList = INPUT.split()
  for word in inList:
    if not spelled_correctly(word.lower()):
      offset = '+%dc' % len(word) # +5c (5 chars)
      pos1_start = input.search(word, '1.0', END)
      while pos1_start:
        pos1_end = pos1_start + offset
        # Add red tag to incorrect words
        input.tag_add('red_tag', pos1_start, pos1_end)
        pos1_start = input.search(word, pos1_end, END)
    else:
      offset = '+%dc' % len(word) # +5c (5 chars)
      pos2_start = input.search(word, '1.0', END)
      while pos2_start:
        pos2_end = pos2_start + offset
        # Remove red tag from correct words
        input.tag_remove('red_tag', pos2_start, pos2_end)
        pos2_start = input.search(word, pos2_end, END)

  result = checker.check(INPUT.lower()) # Acquire suggested words
  
  # Populate suggesiton boxes
  suggest(result)
  # Populate prediction boxes
  generate(INPUT)

  stop_time = time.time()# Stop execution timer

  # Update status bar with execution time for current word
  status = Label(root, text='{}ms'.format(str(1000 * round(stop_time - start_time, 8))), bd=2, relief=SUNKEN, anchor=E)
  status.grid(row=5, columnspan=3, sticky=W+E, pady=10)

# Input predictions to boxes
def generate(input):
  global predictions
  # Seed length is number of previous words to base off of
  seed_length = 5
  predictions = generator.get_last_three(input, seed_length)
  # Clear prediction boxes
  clear_predictions()

  if len(predictions) >= 1:
    predict1.config(state=NORMAL)
    predict1.insert(END, predictions[0])
    predict1['bg'] = "lightblue"
    predict1.config(state=DISABLED)
  if len(predictions) >= 2:
    predict2.config(state=NORMAL)
    predict2.insert(END, predictions[1])
    predict2['bg'] = "lightblue"
    predict2.config(state=DISABLED)
  if len(predictions) >= 3:
    predict3.config(state=NORMAL)
    predict3.insert(END, predictions[2])
    predict3['bg'] = "lightblue"
    predict3.config(state=DISABLED)

# Insert clicked prediction into input
def insert_prediction1(event):
  if len(predictions) >= 1:
    INPUT = input.get('1.0', END)
    result_str = INPUT.strip() + " " + predictions[0] + " "
    input.replace('1.0', END, result_str)
    take_input()
def insert_prediction2(event):
  if len(predictions) >= 2:
    INPUT = input.get('1.0', END)
    result_str = INPUT.strip() + " " + predictions[1] + " "
    input.replace('1.0', END, result_str)
    take_input()
def insert_prediction3(event):
  if len(predictions) >= 3:
    INPUT = input.get('1.0', END)
    result_str = INPUT.strip() + " " + predictions[2] + " "
    input.replace('1.0', END, result_str)
    take_input()

# Input suggestions to boxes 
def suggest(result): 
  # Print results
  # Clear suggestion boxes
  # Reset output background colors
  clear_suggestions()
  if type(result) == str: # If correctly spelled
    status = Label(root, text='No spelling errors.', bd=2, relief=SUNKEN, anchor=E)
    status.grid(row=5, columnspan=3, sticky=W+E, pady=10)
  else: # Print suggestions
    # result = [[a, "{}%".format(str(round(b, 2)))] for a,b in result]

    if len(result) >= 1:
      suggest1.insert(END, result[0][0])
      suggest1['bg'] = colors[int(result[0][1])]
    if len(result) >= 2:
      suggest2.insert(END, result[1][0])
      suggest2['bg'] = colors[int(result[1][1])]
    if len(result) >= 3:
      suggest3.insert(END, result[2][0])
      suggest3['bg'] = colors[int(result[2][1])]

# Right-click menu on highlighted words
def do_popup(event):
  global result
  start_time = time.time()

  cursor_pos = input.index(INSERT).split('.')
  tag_ranges = input.tag_ranges('red_tag')
 
  closest = int(cursor_pos[1]) - int(str(tag_ranges[0]).split('.')[1])
  for i in range(len(tag_ranges)):
    if i % 2 == 0:
      temp = str(tag_ranges[i]).split('.')
      distance = int(cursor_pos[1]) - int(temp[1])
      if distance >= 0 and distance < closest:
        closest = distance
  start_tag = cursor_pos[0] + '.' + str(int(cursor_pos[1]) - closest)
  tag_range = input.tag_nextrange('red_tag', start_tag)
  word = input.get(tag_range[0], tag_range[1])
  result = checker.check(word)

  # Update suggestion boxes
  suggest(result)
  
  stop_time = time.time()
  status = Label(root, text='{}ms'.format(str(1000 * round(stop_time - start_time, 8))), bd=2, relief=SUNKEN, anchor=E)
  status.grid(row=5, columnspan=3, sticky=W+E, pady=10)

  try:
    # Populate menu with corrected words if present
    if len(result) >= 3:
      m.delete(0, 2)
      m.add_command(label=result[0][0], command= lambda:replace(result[0][0], word))
      m.add_command(label=result[1][0], command= lambda:replace(result[1][0], word))
      m.add_command(label=result[2][0], command= lambda:replace(result[2][0], word))
    elif len(result) >= 2:
      m.delete(0, 2)
      m.add_command(label=result[0][0], command= lambda:replace(result[0][0], word))
      m.add_command(label=result[1][0], command= lambda:replace(result[1][0], word))
      m.add_command(label='...', command=replace)
    elif len(result) >= 1:
      m.delete(0, 2)
      m.add_command(label=result[0][0], command= lambda:replace(result[0][0], word))
      m.add_command(label='...', command=replace)
      m.add_command(label='...', command=replace)
    else:
      m.delete(0, 2)
      m.add_command(label='...', command=replace)
      m.add_command(label='...', command=replace)
      m.add_command(label='...', command=replace)

    # Popup relative to NW corner of screen
    m.tk_popup(event.x_root, event.y_root)

  finally:
    m.grab_release()

# Clear prediction boxes
def clear_predictions():
  predict1.config(state=NORMAL)
  predict2.config(state=NORMAL)
  predict3.config(state=NORMAL)
  predict1.delete("1.0", END)
  predict2.delete("1.0", END)
  predict3.delete("1.0", END)
  predict1['bg'] = "white"
  predict2['bg'] = "white"
  predict3['bg'] = "white"
  predict1.config(state=DISABLED)
  predict2.config(state=DISABLED)
  predict3.config(state=DISABLED)

# Clear suggestion boxes
def clear_suggestions():
  suggest1.delete("1.0", END)
  suggest2.delete("1.0", END)
  suggest3.delete("1.0", END)
  suggest1['bg'] = "white"
  suggest2['bg'] = "white"
  suggest3['bg'] = "white"

# ***** INITIALIZE GLOBAL VARIABLES ***** #
# Start execution timer
exec_start = time.time()
# Initialize global result variable
# *Must include 'global result' in each method that references it*
result = []
predictions = []
# Color Gradient based on certainty
from colour import Color
colors = list(Color("red").range_to(Color("green"), 101))

ngrams_path = 'everygrams15000_dict.txt'
generator = TextGeneration(ngrams_path)
wordlist_path = './english_dict.txt'
probabilities_path = './full_probs.json'
checker = SpellChecker(wordlist_path, probabilities_path)
exec_stop = time.time()
print("Started in {} seconds.".format(exec_stop - exec_start))








# Begin GUI Section
root = Tk() # Widget/window object
root.title("Python Spellcheck GUI")
# root.iconbitmap("./tf.ico")
root.geometry('525x260')

# Insert title
title = Label(root, text="Start typing...")
title.grid(row=0, columnspan=3)

# Add suggestion boxes
suggest1 = Text(height=1, width=15)
suggest2 = Text(height=1, width=15)
suggest3 = Text(height=1, width=15)
suggest1.grid(row=1, column=0, padx=5)
suggest2.grid(row=1, column=1, padx=5)
suggest3.grid(row=1, column=2, padx=5)

predict1 = Text(height=1, width=20, state=DISABLED)
predict2 = Text(height=1, width=20, state=DISABLED)
predict3 = Text(height=1, width=20, state=DISABLED)
predict1.grid(row=2, column=0, padx=5, pady=5)
predict2.grid(row=2, column=1, padx=5, pady=5)
predict3.grid(row=2, column=2, padx=5, pady=5)
predict1.bind('<Button-1>', insert_prediction1)
predict2.bind('<Button-1>', insert_prediction2)
predict3.bind('<Button-1>', insert_prediction3)



# Add input text box
input = Text(height=8, width=60) # Height/Width are number of lines/characters. Each character is 10px
input.grid(row=3, columnspan=3, pady=10)
input.tag_config('red_tag', foreground='red', underline=1)
input.tag_config('none_tag', foreground='black', underline=0)
input.tag_bind('red_tag', '<Button-3>', do_popup)

# Flush output with spacebar
root.bind('<space>', flush)

# Initialize status bar at bottom of window
status = Label(root, text='', bd=2, relief=SUNKEN, anchor=E)
status.grid(row=5, columnspan=3, sticky=W+E, padx=5, pady=10)

# Initialize right-click menu with ... for each suggestion
m = Menu(root, tearoff=0)
m.add_command(label= '...')
m.add_command(label= '...')
m.add_command(label= '...')

root.mainloop()
