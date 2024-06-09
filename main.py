from media_wiki import MediaWikiIMSLP


def main():
    mw = MediaWikiIMSLP(
        list="categorymembers",
        pageid=1302
    )
    print("--start querying imslp--")
    mw.query(num_pages=10000)
    print("--finish querying imslp--")

if __name__ == "__main__":
    main()