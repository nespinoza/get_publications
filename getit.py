import os
import json

def read_json(fname):
    with open(fname) as f:
        data = json.load(f)
    return data

token = 'your token'
library = 'your library'
last_name = 'your last name'

# First, get all papers from the library:
os.system('curl -H "Authorization: Bearer {0:}" https://api.adsabs.harvard.edu/v1/biblib/libraries/{1:}?rows=1000 | python -m json.tool  > all_papers.json'.format(token,library))

# Read json to dict:
data = read_json('all_papers.json')

for paper in list(data['documents']):
    # Iterate, extract names, title, save:
    os.system('curl -H "Authorization: Bearer {0:}" "https://api.adsabs.harvard.edu/v1/search/query?q={1:}&fl=title,author,journal,volume,page,year" | python -m json.tool  > paper_data.json'.format(token,paper))
    paper_data = read_json('paper_data.json')
    #print(paper_data.keys())
    title = paper_data['response']['docs'][0]['title']
    authors = paper_data['response']['docs'][0]['author']
    try:
        volume = paper_data['response']['docs'][0]['volume']
    except:
        print('Volume not found for ',paper)
        if 'A&A' in paper:
            yr,volume,p = paper.replace('.',' ').split()
            volume = volume[:-1]
        elif 'MNRAS' in paper:
            yr,volume,p = paper.replace('.',' ').split()
        elif 'PASP' in paper:
            yr,volume = paper.replace('.',' ').split()
            volume = volume[:3]
        print('Replacing by ',volume)
    try:
        page = paper_data['response']['docs'][0]['page']
    except:
        print('Page not found for ',paper)
        x = paper.replace('.',' ').split()
        page = x[-1][:]
        print('Replacing with ',page)
    year = paper_data['response']['docs'][0]['year']
    if 'AJ' in paper:
        journal = 'Astronomical Journal'
    elif 'PASP' in paper:
        journal = 'Publications of The Astronomical Society of the Pacific'
    elif 'ApJ' in paper:
        journal = 'Astrophysical Journal'
    elif 'A&A' in paper:
        journal = 'Astronomy \& Astrophysics'
    elif 'MNRAS' in paper:
        journal = 'Monthly Notices of the Royal Astronomical Society'
    elif 'Natur' in paper:
        journal = 'Nature'
    else:
        print('Journal not recognized for ',paper,'. Filling with: UKKNOWN JOURNAL')
        journal = 'UKKNOWN JOURNAL'
    
    #print(paper_data)
    #print(title,authors,journal)
