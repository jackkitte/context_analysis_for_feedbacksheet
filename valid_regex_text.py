import json
import pprint
import regex


#with open("data/2956.json", "r") as f:
with open("data/14612.json", "r") as f:
    json_data = json.load(f)

#json_data.pop("id")
#for key, val in json_data.items():
#    print("{} : {}".format(key, val))

history = json_data.pop("history").strip("[]")
#history_list = regex.findall("(?<rec>\{(?:[^\{\}]+|(?&rec))*\})", history)
#history_list = regex.findall("\{(?>[^\{\}]+|(?R))*\}", history)
history_list = regex.findall("\{\".+?\"\}", history)

#print(history_list1[4])
print(len(history_list))
#for string in history_list:
#    try:
#        pprint.pprint(json.loads(string))
#    except:
#        print("正規表現失敗")