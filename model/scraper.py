""""
returns all the links on each wiki page
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

nodes = pd.read_csv('concept_map_nodes.csv')
edges = pd.read_csv('concept_map_edges.csv')

def return_articles(url):
    session = requests.Session()
    selectWikiPage = url

    """need to clean this i'll have to clean it so each #cite_ref gets its own array of references, bc it repeats"""
    links = []
    if "wikipedia" in selectWikiPage:
        html = session.post(selectWikiPage)
        bsObj = BeautifulSoup(html.text, "html.parser")
        findReferences = bsObj.find('ol', {'class': 'references'})
        href = BeautifulSoup(str(findReferences), "html.parser")
        #links = [a["href"] for a in href.find_all("a", href=True) if '#cite_ref-' not in a]
        for a in href.find_all("a", href=True):
            if '#cite_ref-' not in a["href"]:
                links.append(a["href"])
        return links
    else:
        print("Error: Please enter a valid Wikipedia URL")
        return

#1st we have to find the prerequisite link
def find_url(node_name):
    return nodes[nodes['Id']==node_name]['d4'].values[0]


data_sources = []
for topic in nodes.d6.values[:]:
    #rel_topic = find_most_relevant_topics(topic.lower)
    prereq_node = nodes[nodes['d6']==topic].Id.values[0]
    url = find_url(prereq_node)
    if type(url) is not float:
        lis = return_articles(url)
        if lis:
            for article in lis:
                data_sources.append((topic, prereq_node, article))


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
