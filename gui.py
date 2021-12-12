import re
import time
import numpy as np
import string
from collections import Counter

from tkinter import *
from PIL import ImageTk, Image


class SpellChecker(object):
  def __init__(self, wordlist_path, probabilities_path):
    import json
    # Import probabilities
    with open(probabilities_path, 'r') as inFile:
      self.probs = json.load(inFile)

    # Import set of all english words
    import ast
    with open(wordlist_path,'r') as f:
      self.vocab = set(ast.literal_eval(f.read()))

  def _level_one_edits(self, word): # Words misspelled by one letter
    letters = string.ascii_lowercase + "\'" # List of all 26 letters
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)] # Find all ways to split a word [(w, ord), (wo, rd), (wor, d)]
    deletes = [l + r[1:] for l, r in splits if r] # Find all ways of having a missing letter [ord, wrd, wod, wor]
    swaps = [l + r[1] + r[0] + r[2:] for l,r in splits if len(r) > 1] # Find all ways of swapping letters [owrd, wrod, wodr]
    replaces = [l + c + r[1:] for l,r in splits if r for c in letters] # Find all ways of replacing a letter [aord, bord,..., worz]
    inserts = [l + c + r for l,r in splits for c in letters] # Find all ways of inserting a letter [aword, bword,..., wordz]
    return set(deletes + swaps + replaces + inserts) # Return set of all unique possibilities

  def _level_two_edits(self, word): # Words misspelled by two letters
    return set([e2 for e1 in self._level_one_edits(word) for e2 in self._level_one_edits(e1)]) # Run level_one_edits twice to get words two letters off

  def _level_three_edits(self, word): # Words misspelled by three letters
    return set([e2 for e1 in self._level_one_edits(word) for e2 in self._level_two_edits(e1)]) # Run L1edits for each L2edit to get words 3 letters off

  def check(self, word): # Spellcheck algorithm
    present = word in self.vocab
    if present:
      return 'Spelled correctly.'
    print(present)
    candidates = self._level_one_edits(word) or self._level_two_edits(word) or self._level_three_edits(word) or [word] # Gather all possible mispellings
    best_guesses = [w for w in candidates if w in self.vocab] # Only suggest spellings that are real words
    sorted_tuples = sorted([(w, self.probs[w]) for w in best_guesses], key = lambda x: x[1], reverse=True) # Sort possible words
    print(best_guesses)
    sum_probs = 0
    for e in sorted_tuples:
      sum_probs += e[1]
    confidence_tuples = []
    for e in range(len(sorted_tuples)):
       c = 100 * sorted_tuples[e][1] / sum_probs # Calculate and store confidence
       w = sorted_tuples[e][0] # Store word
       t = (w, c)# Create tuple
       confidence_tuples.append(t) # Add (word, confidence) to result
    if word in self.vocab:
      return "Spelled Correctly."
    else:
      return confidence_tuples[:3]



wordlist_path = './english_dict.txt'
probabilities_path = './word_probs.json'
checker = SpellChecker(wordlist_path, probabilities_path)


# Begin GUI Section
root = Tk() # Widget/window object
root.title("Text Editor GUI")
root.iconbitmap("./tf.ico")
root.geometry('500x175')

# Grab all text in box
# Split into tuple of words with (word, spelledcorrectly)
def spelled_correctly(word):
   return word in SpellChecker.vocab

# Clears output and places text into output from input
def take_input():
   output.delete("1.0", END) # Clear text in output
   INPUT = input.get("1.0", "end-1c") # Grab all input
   start_time = time.time()# Start execution timer
   result = checker.check(INPUT) # Acquire suggested words
   stop_time = time.time()# Stop execution timer# ** Stop execution timer
   # ** Put execution time in status bar
   execution_time = Label(root, text="In {} seconds".format(str(round(stop_time - start_time, 6)))).pack()
   if type(result) == str: # If correctly spelled
      output.insert(END, result) # Print "correctly spelled"
   else: # Print suggestions
      result = [[a, "{}%".format(str(round(b, 2)))] for a,b in result]
      output.insert(END, result)
   print(result)

title = Label(root, text="Start typing...")
title.pack()

input = Text(root, height=1, width=15) # Height/Width are number of lines/characters. Each character is 10px
input.pack()

show = Button(root, height=2, width=20, text='Check', command= lambda:take_input())
show.pack()

output = Text(root, height=1, width=60)
output.pack()

root.mainloop()

