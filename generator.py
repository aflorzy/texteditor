
import json
import re


class TextGeneration(object):
  n_dict = {}
  def __init__(self, ngrams_path):
      with open(ngrams_path, 'r') as inFile:
          self.n_dict = json.load(inFile)

  # Joins list of words into string
  def join_words(self, l):
      result = ''
      for w in l:
          result += w + ' '
      # Return string without trailing spaces
      return result.strip()

  # Find best match first (longest seed match with length >= words.len() + 1)
  # Gets last 3 words of string, or two or one
  def get_last_three(self, str, seed=3):
      words = str.strip(' ,.()\'\"').split(' ')
      subset = []
      suggestions = []
      # Get 3 suggestions, or stop if looking if no matches
      while len(suggestions) < 3 and seed > 0:
          subset = words[-seed:]
          subset_str = self.join_words(subset)
          for key in self.n_dict:
              if len(suggestions) == 3:
                  break
              if self.n_dict[key] == seed + 1:
                  # if subset is found in the FIRST part of the key
                  if re.search(r'\b' + subset_str + r'\b', key) and key.find(subset_str) == 0:
                    #   suggestions.append(key.removeprefix(subset_str).strip())
                      suggestions.append(key.lstrip(subset_str).strip())
          seed -= 1
      # Suggestions are formed with original prompt still included
      pared_suggestions = []
      for e in suggestions:
        #   pared_suggestions.append(e.removeprefix(subset_str).strip())
            pared_suggestions.append(e.lstrip(subset_str).strip())

      return pared_suggestions

if __name__ == '__main__':
    ngrams_path = 'everygrams15000_dict.txt'
    generator = TextGeneration(ngrams_path)
    sample_text = 'i'
    print(generator.get_last_three(sample_text))