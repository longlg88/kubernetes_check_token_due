#!/usr/bin/python

import os
import sys
import subprocess
import json
from datetime import datetime

def gen_duedate():
    """
    Get Secrets from all namespaces in kubernets environment
    """
    get_crt_list=[]
    crt_cmd = "kubectl get secret --all-namespaces -o json | jq -r ' .items[].data.\"ca.crt\"'"
    get_crt_info = subprocess.check_output(crt_cmd, shell=True)
    get_crt_list=get_crt_info.decode("utf-8").replace('\n',' ').split()

    dirName = ".set"
    try:
        os.mkdir(dirName)
    except FileExistsError:
        print("Directoy "+ dirName +" already exists")

    filename="File"

    cnt = 0
    for arg in get_crt_list:
        if arg == "null":
            print("============================ It it null value ==========================" )
        else:
            decode_file_cmd = "echo " + arg + " | base64 -d > " + dirName + "/" + filename + str(cnt)
            os.system(decode_file_cmd)
            get_due_date_cmd = "openssl x509 -enddate -noout -in " + dirName + "/" + filename + str(cnt)
            os.system(get_due_date_cmd)
        cnt += 1

    os.system("rm -rf .set")
        

if __name__ == "__main__":
    gen_duedate()
