import codecs
import os
import json
from Hyphenator import Hyphenator

def load_exceptions(language, region):
     lowercasedLanguage = language.lower()
     lowercasedRegion = region.lower() if isinstance(region, str) else ""
     directory = os.path.join(os.path.dirname(__file__), "hyphenation-rules")
     paths = []
     for filename in os.listdir(directory):
     	if os.path.isfile(os.path.join(directory, filename)) and f'hyph-{lowercasedLanguage}' in filename:
               paths.append(os.path.join(directory, filename))
     
     filePath = ""
     for candidate in paths:
          if f'{lowercasedLanguage}-{lowercasedRegion}.hyp.txt' in candidate:
               filePath = candidate
               break
          elif f'{lowercasedLanguage}.hyp.txt' in candidate:
              filePath = candidate
          elif len(filePath) == 0 and '.hyp.txt' in candidate:
              filePath = candidate
     if len(filePath) == 0:
         return ""
     
     file = open(filePath, "r", encoding="utf-8")
     return file.read()

def load_rules(language, region):
     lowercasedLanguage = language.lower()
     lowercasedRegion = region.lower() if isinstance(region, str) else ""
     directory = os.path.join(os.path.dirname(__file__), "hyphenation-rules")
     paths = []
     for filename in os.listdir(directory):
     	if os.path.isfile(os.path.join(directory, filename)) and f'hyph-{lowercasedLanguage}' in filename:
               paths.append(os.path.join(directory, filename))
     
     filePath = ""
     for candidate in paths:
          if f'{lowercasedLanguage}-{lowercasedRegion}.pat.txt' in candidate:
               filePath = candidate
               break
          elif f'{lowercasedLanguage}.pat.txt' in candidate:
              filePath = candidate
          elif len(filePath) == 0 and '.pat.txt' in candidate:
              filePath = candidate
     if len(filePath) == 0:
         raise Exception(f'Language not supported: {language}')
     
     file = open(filePath, "r", encoding="utf-8")
     return file.read()

def hyphenate_word(language, region, word):
    exceptions = load_exceptions(language, region)
    rules = load_rules(language, region)
    hyphenator = Hyphenator(rules, exceptions)
    result = hyphenator.hyphenate_word(word)
    hyphenation = {
        "result": result,
    }
    return json.dumps(hyphenation)
