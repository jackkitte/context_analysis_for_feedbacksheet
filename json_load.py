import json
import regex
import os


file_name = "feedbacksheet.json"

if os.path.exists(file_name):
    os.remove(file_name)

for index in range(2, 16831):
    index_json = {}
    feature_json = {}
    with open("data/{}.json".format(index), "r") as f:
        json_data = json.load(f)

    history = json_data.pop("history").strip("[]")
    #history_list = regex.findall("{.+?}", history)
    history_list = regex.findall("{(?>[^{}]+|(?R))*}", history)

    date = None
    regex_switch = False
    join_list = []
    for string in history_list:
        try:
            dic = json.loads(string)
            if date == None:
                date = dic["ch_datetime"]
            join_list.append(dic["ch_comment"])
        except:
            regex_switch = True
            print("{} : 正規表現失敗".format(index))
            break

    if regex_switch:
        history_list = regex.findall("{\".+?\"}", history)
        date = None
        join_list = []
        for string in history_list:
            try:
                dic = json.loads(string)
                if date == None:
                    date = dic["ch_datetime"]
                join_list.append(dic["ch_comment"])
            except:
                print("{} : 正規表現失敗(if文)".format(index))

    join_text = "\n".join(join_list)

    index = json_data.pop("id")
    index_json.update({"index": {"_index": "feedbacksheet", "_type": "_doc", "_id": index}})

    for key, val in json_data.items():
        feature_json.update({key: val})
    feature_json.update({"datetime": date, "history": join_text})
    #feature_json.update({"datetime": date, "category_id": json_data["category"], "category": json_data["category_str"],
    #                  "phenomenon": json_data["phenomenon"], "history": history, "assigned_to_person": json_data["assigned_to_person"],
    #                  "reported_by_person": json_data["reported_by_person"]})

    with open(file_name, "a") as f:
        f.write(json.dumps(index_json, ensure_ascii=False, sort_keys=True))
        f.write("\n")
        f.write(json.dumps(feature_json, ensure_ascii=False, sort_keys=True))
        f.write("\n")