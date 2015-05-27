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

def curl_generate():
    #add a comment
    with open(READ_FILE, 'r') as f:
        lines = f.readlines()
        lines = [s.replace("\n", "") for s in lines]
        final = " ".join(lines)
        with open('curl_parse_run.sh', 'w') as f2:
            f2.write(final)
    st = os.stat(RUN_FILE)
    os.chmod(RUN_FILE, st.st_mode | stat.S_IEXEC)

if __name__ == '__main__':
    old_path = "/Users/briancordonnier/repos/sandbox/new_target"
    new_path = "/Users/briancordonnier/repos/sandbox/target_fliped"
    read_files(old_path, new_path)
