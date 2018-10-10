import os
import ptvsd
import json
import regex
import pprint

from pyknp import KNP

ptvsd.enable_attach(address=("0.0.0.0", 3000))
ptvsd.wait_for_attach()
ptvsd.break_into_debugger()

knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)

file_name = "feedbacksheet.json"

if os.path.exists(file_name):
    os.remove(file_name)

dependency_dic = {}
for index in range(2, 22):
    index_json = {}
    feature_json = {}
    with open("data/{}.json".format(index), "r") as f:
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
                for bnst in result.bnst_list():
                    parent = bnst.parent
                    if parent is not None:
                        child_rep = "".join(regex.findall("(.*)/", mrph.repname)[0] for mrph in bnst.mrph_list() if regex.findall("(.*)/", mrph.repname) != [])
                        parent_rep = "".join(regex.findall("(.*)/", mrph.repname)[0] for mrph in parent.mrph_list() if regex.findall("(.*)/", mrph.repname) != [])
                        parent_list = dependency_dic.get(child_rep, [])
                        parent_list.append(parent_rep)
                        dependency_dic[child_rep] = parent_list
                        print("追加")
                    else:
                        print("追加なし")
            except:
                print("失敗")

#pprint.pprint(dependency_dic)
print(len(dependency_dic))