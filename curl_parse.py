from subprocess import check_output
import os
import stat
import argparse

RUN_FILE = 'curl_parse_run.sh'
READ_FILE = 'curl_parse_read.txt'


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


def curl_parse(local):
    curl = check_output('pbpaste')
    delim = " -H"
    splits = [e+delim for e in curl.split(delim) if e != ""]
    len_splits = len(splits) - 1
    splits[len_splits] = splits[len_splits].replace(delim, "")
    finished = ""
    for i, s in enumerate(splits):
        if local and i == 0:
            s = s.replace("https://app.sproutsocial.com", "http://localhost:8000")
            s = s.replace("https://tagging.test.sproutsocial.com", "http://localhost:8000")
        if "Cookie:" in s:
            new_delim = ";"
            connection_splits = [e+new_delim for e in s.split(new_delim) if e != ""]
            len_connection_splits = len(connection_splits) - 1
            connection_splits[len_connection_splits] = connection_splits[len_connection_splits].replace(new_delim, "")
            for new_i, new_s in enumerate(connection_splits):
                finished += "{0}{1}".format(new_s, "" if new_i == len_connection_splits else "\n")
        elif "WebKitFormBoundary" in s:
            new_delim = "form-data;"
            connection_splits = [e+new_delim for e in s.split(new_delim) if e != ""]
            len_connection_splits = len(connection_splits) - 1
            connection_splits[len_connection_splits] = connection_splits[len_connection_splits].replace(new_delim, "")
            for new_i, new_s in enumerate(connection_splits):
                finished += "{0}{1}".format(new_s, "" if new_i == len_connection_splits else "\n")
        else:
            finished += "{0}{1}".format(s, "" if i == len_splits else "\n")
    print finished
    with open(READ_FILE, 'w') as f:
        f.write(finished)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
 """This script was made to make inspecting/changing of our curl commands easier.
The general flow is to copy the curl command from your web browser and then run
    curl_parse.py -p
this will place the formatted curl request into the file {0}. You are free to modify that
file and when it is ready run
    curl_parse.py -g
to generate the bash file {1} to run. To run just call
    ./{1}
""".format(READ_FILE, RUN_FILE))
    parser.add_argument('-p', '--parse', action='store_true', help='Parse what is in your clipboard')
    parser.add_argument('-l', '--local', action='store_true', help='Change curl to go to your local machine')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate new bash file')


    args = parser.parse_args()
    if args.parse:
        curl_parse(args.local)
    if args.generate:
        print("Generate sh file and writting to {0}".format(RUN_FILE))
        curl_generate()
