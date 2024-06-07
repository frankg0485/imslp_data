from media_wiki import MediaWikiIMSLP


def main():
    mw = MediaWikiIMSLP(
        prop=["images"]
    )
    print("--start querying imslp--")
    print(mw.query(num_pages=100))
    print("--finish querying imslp--")

if __name__ == "__main__":
    main()