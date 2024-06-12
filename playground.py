# Experimenting with things in the data folder
from media_wiki import MediaWikiIMSLP
import os
import pprint

def filter_composers(min_size=50):
    with open("data/composers_pageids.txt", 'r') as pageids_file:
        pageids = pageids_file.readlines()
    
    inc = 50
    composers = []
    for i in range(0, len(pageids), inc):
        mw = MediaWikiIMSLP(prop=["categoryinfo"], list="", pageids=pageids[i:i+inc])#, titles=["testing"])
        res = mw.query()
        print("{}% done".format(i / len(pageids) * 100))
        composers.extend(filter(lambda c: c["categoryinfo"]["size"] >= min_size, res))

    # remove "Category:"
    return [c["title"][9:] for c in composers]

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
    composers = filter_composers()
    for c in composers:
        print(c)

if __name__ == "__main__":
    main()