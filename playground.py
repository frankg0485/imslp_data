# Experimenting with things in the data folder
from media_wiki import MediaWikiIMSLP
import os
import pprint

def filter_composers(min_size=100):
    with open("data/composers_pageids.txt", 'r') as pageids_file:
        pageids = pageids_file.readlines()
    
    inc = 150
    for i in range(0, len(pageids), inc):
        mw = MediaWikiIMSLP(prop=["categoryinfo"], list="", pageids=pageids[i:i+inc])
        mw.query()

def test_list():
    mw = MediaWikiIMSLP(list=["allcategories"])
    res = mw.query(num_pages=5)
    print(res)
    pprint.pprint(res)
    
def main():
    try:
        os.remove("out.txt")
    except OSError:
        pass
    # test_list()
    filter_composers()

if __name__ == "__main__":
    main()