import os
import ptvsd
import json
import regex
import pprint

from elasticsearch import Elasticsearch
from pyknp import KNP

#ptvsd.enable_attach(address=("0.0.0.0", 3000))
#ptvsd.wait_for_attach()
#ptvsd.break_into_debugger()

knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
es = Elasticsearch("elasticsearch:9200")

result = es.search(index="feedbacksheet", 
                   body={"query": {
                            "query_string": {
                                "query": 'cause:1 AND phenomenon:"障害"'
                            }
                         },
                         "size": 10000,
                        }
                   )

file_name = "feedbacksheet.json"

if os.path.exists(file_name):
    os.remove(file_name)

predicate_term_structure_dic = {}
for doc in result["hits"]["hits"][:100]:
    index_json = {}
    feature_json = {}
    dependency_dic = {}
    with open("data/{}.json".format(doc["_id"]), "r") as f:
        json_data = json.load(f)

    history = json_data.pop("history").strip("[]")
    history_list = regex.findall("{(?>[^{}]+|(?R))*}", history)

    comment_2d_list = []
    for history_str in history_list:
        comment = json.loads(history_str)["ch_comment"]
        comment_list = comment.split("\n")
        comment_2d_list.append(comment_list)

    for sentence_list in comment_2d_list:
        for sentence in sentence_list:
            if sentence == "":
                break
            try:
                regex_sentence = regex.sub("^#", "", sentence)
                result = knp.parse(regex_sentence)
                for tag in result.tag_list():
                    if tag.pas is not None:
                        predicate = ''.join(mrph.midasi for mrph in tag.mrph_list())
                        for case, args in tag.pas.arguments.items(): # case: str, args: list of Argument class
                            for arg in args: # arg: Argument class
                                if regex.match("[ァ-ン]+", case):
                                    join_term = ""
                                    children_term = ""
                                    for children in result.tag_list()[arg.tid].children:
                                        children_term = children_term + children.midasi
                                    join_term = join_term +  children_term + arg.midasi + case
                                    term_list = dependency_dic.get(predicate, [])
                                    term_list.append(join_term)
                                    dependency_dic[predicate] = term_list
                                    #print("{} -> {}".format(join_term, predicate))
                                else:
                                    pass
#                                elif case == "外の関係":
#                                    for children in result.tag_list()[arg.tid].children[:-1]:
#                                        out_term = arg.midasi
#                                        out_term = children.midasi + predicate + out_term
#                                        term_list = dependency_dic.get(predicate, [])
#                                        term_list.append(out_term)
#                                        dependency_dic[predicate] = term_list
#                                        print("{} -> {}".format(out_term, predicate))
#                                else:
#                                    for children in result.tag_list()[arg.tid].children:
#                                        modification_term = arg.midasi
#                                        modification_term = children.midasi + modification_term
#                                        term_list = dependency_dic.get(predicate, [])
#                                        term_list.append(modification_term)
#                                        dependency_dic[predicate] = term_list
#                                        print("{} -> {}".format(modification_term, predicate))
                #print("「 {} 」".format(sentence))
            except:
                pass
                #print("失敗")
    predicate_term_structure_dic[doc["_id"]] = dependency_dic

with open("predicate_term_structure_history.json", "w") as f:
    json.dump(predicate_term_structure_dic, f)
#pprint.pprint(dependency_dic)