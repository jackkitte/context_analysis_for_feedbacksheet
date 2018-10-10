import json
import pprint

with open("bulk.log", "r") as f:
    json_data = json.load(f)

fail_list = []
for index in json_data["items"]:
    try:
        if "error" in index["index"].keys():
            fail_list.append("{} : {}".format(index["index"]["_id"], index["index"]["error"]["reason"]))
    except:
        print("{} : keyerror".format(index["index"]["_id"]))

join_text = "\n".join(fail_list)

with open("fail_list.txt", "w") as f:
    f.write(join_text)