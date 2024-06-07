# https://imslp.org/api.php
# Parameters:
#   format              - The format of the output
#                         One value: json, jsonfm, php, phpfm, wddx, wddxfm, xml, xmlfm, yaml, yamlfm, 
#                                    rawfm, txt, txtfm, dbg, dbgfm,
#                                    dump, dumpfm
#                         Default: xmlfm
#   action              - What action you would like to perform. See below for module help
#                         One value: login, logout, query, expandtemplates, parse, opensearch,      
#                               feedcontributions, feedwatchlist, help,
#                               paraminfo, rsd, compare, purge, rollback, delete, undelete, protect, 
#                               block, unblock, move, edit,
#                               upload, filerevert, emailuser, watch, patrol, import, userrights
#                         Default: help


import requests

BASE_URL = "https://imslp.org/api.php"

class MediaWikiIMSLP:
    def __init__(self,
                 format="json",
                 action="query",
                 prop: list[str]=[],
                 list="allcategories"):
        self.format = format
        self.action = action
        self.prop = prop
        self.list = list

    def query(self):
        params = {
            "format": self.format,
            "action": self.action,
            "prop": '|'.join(self.prop),
            "list": self.list
        }

        res = requests.get(BASE_URL, params=params)
        return res.json()

