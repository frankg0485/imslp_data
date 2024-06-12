# https://imslp.org/api.php
# Parameters:
#   format              - only allow json
#   action              - only allow query

# Subparams:
#   prop                - if this param is present, then must also have titles or pageids
#                       values: info, links, images, imageinfo, categories, categoryinfo
#   titles              - list of titels
#   pageids             - list of pageids
#
#   list                - allimages, allpages, alllinks, allcategories, categorymembers, search

# TODO: all props have a prefix - create a prefix map to easily set prop-specific params

import requests
import pprint

BASE_URL = "https://imslp.org/api.php"


class MediaWikiIMSLP:
    def __init__(
        self,
        prop: list[str] = [],
        list: list[str] = [],
        pageid=None,
        pageids: list[str] = [],
        title=None,
        titles: list[str] = [],
    ):
        self.format = "json"
        self.action = "query"
        self.prop = prop
        self.list = list
        self.pageid = pageid
        self.title = title
        self.pageids = pageids
        self.titles = titles

    # all props and lists have a prefix for their subparams
    pref_map = {
        # prop
        "info": "in",
        "images": "im",
        "imageinfo": "ii",
        "categories": "cl",
        "categoryinfo": "ci",

        # list
        "categorymembers": "cm",
        "allcategories": "ac",
        "allimages": "ai",
        "allpages": "ap",
        "alllinks": "al",
        "search": "sr"
    }

    def _get_prefix(self, prop):
        if pref := self.pref_map.get(prop):
            return pref
        else:
            raise ValueError("get_prefix(): no prefix found for {}, or invalid prop/list".format(prop))

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
        }

        prefs = []
        if len(self.prop):
            params["prop"] = "|".join(self.prop)
            prefs = [self._get_prefix(p) for p in self.prop]
        elif len(self.list):
            params["list"] = "|".join(self.list)
            prefs = [self._get_prefix(p) for p in self.list]
        else:
            raise ValueError("need either self.prop or self.list to be non-empty")

        # set the query limit to max
        for p in prefs:
            params["{}limit".format(p)] = 5000

        if params.get("prop"):
            if not (len(self.pageids) or len(self.titles)):
                raise ValueError(
                    "prop param must be accompanied by titles or pageids param"
                )
            if len(self.pageids):
                params["pageids"] = "|".join(self.pageids)
            if len(self.titles):
                params["titles"] = "|".join(self.titles)

        if "categorymembers" in self.list:
            if self.pageid:
                params["{}pageid".format(self._get_prefix("categorymembers"))] = (
                    self.pageid
                )
            elif self.title:
                params["{}title".format(self._get_prefix("categorymembers"))] = (
                    self.title
                )
            else:
                raise ValueError("list=categorymembers requires either pageid or title")

        return_res = []
        with open(out_path, "a") as outfile:
            for i in range(num_pages):
                res = requests.get(BASE_URL, params=params)
                print("finished querying url", res.url)

                res_json = res.json()
                if "error" in res_json:
                    raise ValueError(res_json["error"]["info"])
                if "warnings" in res_json:
                    print(res_json["warnings"])
                res_list = []
                if params.get("list"):
                    res_list = [res_json[self.action][l] for l in self.list]
                    for r in res_list:
                        for l in r:
                            return_res.append(l)
                            outfile.write("{}\n".format(pprint.pformat(l)))
                elif params.get("prop"):  # prop doesn't have query-continue
                    res_list = res_json[self.action]["pages"]
                    for _, val in res_list.items():
                        return_res.append(val)
                        outfile.write("{}\n".format(pprint.pformat(val)))
                    break

                outfile.flush()

                # continue querying if list param
                try:
                    continue_dicts = [res_json["query-continue"][l] for l in self.list]
                except ValueError:
                    print("Reached the end: queried {} pages total".format(i + 1))
                    break
                
                for cd in continue_dicts:
                    for param, val in cd.items():
                        params[param] = val
            else:
                print("Successfully queried {} pages".format(num_pages))

            outfile.flush()
        
        return return_res
