import pprint
import os
import json

def flip_dict(dict):
    new_dict = {}
    for key, value in dict.iteritems():
        if key != "smartling":
            new_dict[value] = key
    return new_dict

def read_files(old_path, new_path):
    for file in os.listdir(old_path):
        with open(os.path.join(old_path, file), 'r') as f:
            dict = json.load(f)
            new_dict = flip_dict(dict)
        with open(os.path.join(new_path, file), 'w') as f:
            str = json.dumps(new_dict, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(str.encode('UTF-8'))

if __name__ == '__main__':
    old_path = "/Users/briancordonnier/repos/sandbox/new_target"
    new_path = "/Users/briancordonnier/repos/sandbox/target_fliped"
    read_files(old_path, new_path)