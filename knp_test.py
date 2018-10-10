import ptvsd
import json
import regex
import pprint

from pyknp import KNP

ptvsd.enable_attach(address=("0.0.0.0", 3000))
ptvsd.wait_for_attach()
ptvsd.break_into_debugger()

knp = KNP()     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)

with open("data/14612.json", "r") as f:
    json_data = json.load(f)

history = json_data.pop("history").strip("[]")
#history_list = regex.findall("\{(?>[^\{\}]+|(?R))*\}", history)
history_list = regex.findall("{(?:[^{}]+|(?R))*}", history)

comment_2d_list = []
for history_str in history_list:
    comment = json.loads(history_str)["ch_comment"]
    comment_list = comment.split("\n")
    comment_2d_list.append(comment_list)

for sentence in comment_2d_list[1]:
    result = knp.parse(sentence)
    for bnst in result.bnst_list():
        parent = bnst.parent
        if parent is not None:
            child_rep = " ".join(mrph.repname for mrph in bnst.mrph_list())
            parent_rep = " ".join(mrph.repname for mrph in parent.mrph_list())
            print(child_rep, "->", parent_rep)
    for tag in result.tag_list():
        if tag.pas is not None: # find predicate
            print('述語: %s' % ''.join(mrph.midasi for mrph in tag.mrph_list()))
            for case, args in tag.pas.arguments.items(): # case: str, args: list of Argument class
                for arg in args: # arg: Argument class
                    print('\t格: %s,  項: %s  (項の基本句ID: %d)' % (case, arg.midasi, arg.tid))
    print(sentence)
    print("")
    print("")

print("終了")