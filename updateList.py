import json, os
def update(entry):
    with open('UserList.json','r+') as f:
        data0 = json.load(f)
        f.close()
        data0["list"].append(entry)
    with open('temp.json','w+') as f:
        json.dump(data0,f)
        f.close()
    os.remove("UserList.json")
    os.rename('temp.json', 'UserList.json')

# update({"hasan":{
#                                         "password":1
#                                     }})