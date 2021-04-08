import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy

edges = pd.read_csv('concept_map_edges.csv')
nodes = pd.read_csv('concept_map_nodes.csv')



def find_most_relevant_topics(user_query):
    """takes in user input, returns most relevant topic's node id based on spacy's embeddings"""
    nlp = spacy.load("en_core_web_sm")
    similar = 0
    most_sim_topic = ''
    topic_embeddings = {}
    emb1 = nlp(user_query)

    for topic in nodes.d6:
        emb2 = nlp(topic) #gotta store these embeddings!!!!
        sim = emb1.similarity(emb2)
        topic_embeddings[sim] = topic

    relevant_topic_name = topic_embeddings[max(topic_embeddings.keys())]
    return nodes[nodes['d6']==relevant_topic_name]['Id'].values[0]

def find_prerequisites(node):
    try:
        prereqs = edges[edges['Target']==node]['Source'].values
        return nodes[nodes['Id'].isin(prereqs)]['Id'].values[0]
    except:
        return None

def find_children(node):
    try:
        prereqs = edges[edges['Source']==node]['Target'].values
        return nodes[nodes['Id'].isin(prereqs)]['Id'].values[0]
    except:
        None

#1st we have to find the prerequisite link
def find_url(node_name):
    return nodes[nodes['Id']==node_name]['d4'].values[0]


def return_articles(url):
    session = requests.Session()
    selectWikiPage = url

    """need to clean this i'll have to clean it so each #cite_ref gets its own array of references, bc it repeats"""

    if "wikipedia" in selectWikiPage:
        html = session.post(selectWikiPage)
        bsObj = BeautifulSoup(html.text, "html.parser")
        findReferences = bsObj.find('ol', {'class': 'references'})
        href = BeautifulSoup(str(findReferences), "html.parser")
        links = [a["href"] for a in href.find_all("a", href=True) ]
        return links[:20]
    else:
        print("Error: Please enter a valid Wikipedia URL")

rel_topic = find_most_relevant_topics('recurrent neural network')
prereq_node = find_prerequisites(rel_topic)
if prereq_node is None:
    prereq_node = find_children(rel_topic)
url = find_url(prereq_node)
return_articles(url)