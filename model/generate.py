import pandas as pd
from fuzzywuzzy import process
prereqs = pd.read_csv(r'C:\Users\nour_\IdeaProjects\shortlist_generator\model\prereqs.csv')

def getRelevantTopics(user_input):
    x = process.extractOne(user_input, prereqs['name'].values)
    return x[0]

def generate_shortlist(user_input):
    return {'articles': list(prereqs[prereqs['name'].str.lower() == user_input]['url'].values)}
