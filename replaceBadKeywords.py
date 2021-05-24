import re

def ReplaceBadKeywords(string):
    string = re.sub(r'\([^()]*\)', '', string)
    string = re.sub(r'\[[^()]*\]', '', string)
    string = re.sub(r'\[[^()]*', '', string)
    string = re.sub('Studio Sessions: ', '', string)
    return string
    