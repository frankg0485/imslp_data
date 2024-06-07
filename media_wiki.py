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
                 prop: list[str]=["images"],
                 list="allcategories"):
        self.format = format
        self.action = action
        self.prop = prop
        self.list = list


    # result JSON:
    # {
    #   self.action: {
    #       self.list: {
    #       
    #       }
    #   }
    # 
    #   "query-continue": {
    #       self.list: {
    #           query continue param name : value
    #       }
    #   }
    # 
    # }
    def query(self, num_pages=1):
        params = {
            "format": self.format,
            "action": self.action,
            "prop": '|'.join(self.prop),
            "list": self.list
        }

        results_list = []
        for _ in range(num_pages):
            res = requests.get(BASE_URL, params=params)
            print("finished querying url", res.url)

            res_json = res.json()
            print("RESULT:", res_json)
            results_list.extend(res_json[self.action][self.list])
            
            continue_dict = res_json["query-continue"][self.list]
            continue_param = list(continue_dict.keys())[0]
            print("continuing with param {}, value {}".format(continue_param, continue_dict[continue_param]))
            params[continue_param] = continue_dict[continue_param]

        return res.json()

