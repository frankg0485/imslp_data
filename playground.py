# Experimenting with things in the data folder
from media_wiki import MediaWikiIMSLP

def filter_composers(min_size=100):
    with open("data/composers_pageids.txt", 'r') as pageids_file:
        pageids = pageids_file.readlines()
    
    pageids = pageids[:50]
    mw = MediaWikiIMSLP(prop=["categoryinfo"], list="", pageids=pageids)
    mw.query(num_pages=1000)

def main():
    filter_composers()
if __name__ == "__main__":
    main()