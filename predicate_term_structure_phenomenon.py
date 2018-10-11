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

    phenomenon = json_data.pop("phenomenon")
    sentence_list = phenomenon.split("\r\n")

    for sentence in sentence_list:
        if sentence == "":
            continue
        try:
            regex_sentence = regex.sub("^#", "", sentence)
            result = knp.parse(regex_sentence)
            for tag in result.tag_list():
                if tag.pas is not None:
                    predicate = ''.join(mrph.midasi for mrph in tag.mrph_list())
                    if predicate == "." or regex.match("[!-/:-@[-`{-~]+", predicate):
                        continue
                    term_type = {"ガ":"", "ガ2":"", "ト":"", "ヲ":"", "デ":"", "ニ":""}
                    for case, args in tag.pas.arguments.items(): # case: str, args: list of Argument class
                        for arg in args: # arg: Argument class
                            children_term = ""
                            for children in result.tag_list()[arg.tid].children:
                                children_term = children_term + children.midasi
                            if arg.midasi == ".":
                                continue
                            if regex.match("[ァ-ン]+", case):
                                join_term = children_term + arg.midasi + case
                                term_type[case] = join_term
                            elif case == "外の関係":
                                out_term = predicate + result.tag_list()[arg.tid].midasi
                                term_list = dependency_dic.get(predicate, [])
                                term_list.append(out_term)
                                dependency_dic[predicate] = term_list
                            else:
                                modification_term = children_term + result.tag_list()[arg.tid].midasi
                                term_list = dependency_dic.get(predicate, [])
                                term_list.append(modification_term)
                                dependency_dic[predicate] = term_list
                    join_term_type = term_type["ガ"] + term_type["ヲ"] + term_type["デ"] + term_type["ニ"] + term_type["ト"]
                    if join_term_type != "":
                        term_list = dependency_dic.get(predicate, [])
                        term_list.append(join_term_type)
                        dependency_dic[predicate] = term_list
                        if term_type.get("ガ2", False):
                            join_term_type = term_type["ガ2"] + term_type["ヲ"] + term_type["デ"] + term_type["ニ"] + term_type["ト"]
                            term_list = dependency_dic.get(predicate, [])
                            term_list.append(join_term_type)
                            dependency_dic[predicate] = term_list

        except:
            pass
            #print("失敗")
    predicate_term_structure_dic[doc["_id"]] = dependency_dic

with open("predicate_term_structure_phenomenon.json", "w") as f:
    json.dump(predicate_term_structure_dic, f)
