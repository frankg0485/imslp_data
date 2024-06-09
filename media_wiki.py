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
                 list="allcategories",
                 pageid=None
                 ):
        self.format = format
        self.action = action
        self.prop = prop
        self.list = list
        self.pageid = pageid


    # result JSON:
    # {
    #   **OPTIONAL**
    #   warnings: {
    #   
    #   }
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
    # get all composers: https://imslp.org/api.php?action=query&list=categorymembers&format=json&cmpageid=1302
    # example composer: https://imslp.org/api.php?action=query&prop=categoryinfo&titles=Category:Abadie,%20Louis

    def query(self, out_path="out.txt", num_pages=1):
        params = {
            "format": self.format,
            "action": self.action,
            "prop": '|'.join(self.prop),
            "list": self.list
        }

        if params["list"] == "categorymembers":
            params["cmpageid"] = self.pageid
            params["cmlimit"] = 5000

        with open(out_path, 'w') as outfile:
            for i in range(num_pages):
                res = requests.get(BASE_URL, params=params)
                print("finished querying url", res.url)

                res_json = res.json()
                #print("RESULT:", res_json)
                if "error" in res_json:
                    raise ValueError(res_json["error"]["info"])
                res_list = res_json[self.action][self.list]
                for r in res_list:
                    outfile.write("{}\n".format(r["pageid"]))
                outfile.flush()
                try:
                    continue_dict = res_json["query-continue"][self.list]
                except ValueError:
                    print("Reached the end: queried {} pages total".format(i + 1))
                    break
                continue_param = list(continue_dict.keys())[0]
                params[continue_param] = continue_dict[continue_param]
            else:
                print("Successfully queried {} pages".format(num_pages()))
