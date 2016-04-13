#!/usr/bin/python

import os, shlex
import sys, getopt
import subprocess

port = "29418"
project = "gerrit.ovirt.org"

# Commands
cmd_git_log = "git log "
cmd_pretty ="--pretty=format:\"%h\" -n 1 "
cmd_oneline="--pretty=oneline -n 1 "
cmd_skip = " --skip 1 "
cmd_branch = "git rev-parse "
add_reviewers = "ssh -p "+ port + " " + project + " " + "gerrit set-reviewers -a "
add_verify = "ssh -p "+ port + " " + project + " " + "gerrit review --verified +1 "

def __add_reviewers(commit, reviewers):
    print "[DEUBG] Commit %s is being added with reviewers : %s" %(commit, reviewers)
    add_reviewers_cmd = add_reviewers + reviewers + " " + commit
    os.popen(add_reviewers_cmd)

def __add_verify(commit):
    print "[DEBUG] Commit %s is being added with verify flag" %commit
    add_verify_flag = add_verify + " " + commit
    print add_verify_flag
    os.popen(add_verify_flag)

def change_patches(reviewers, verify, branch, send_mail):
    print "[DEBUG] Fetching commit hash code for branch %s. " %branch
    commit_hash = subprocess.Popen(shlex.split(cmd_branch + branch), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    commit = subprocess.Popen(shlex.split(cmd_git_log + cmd_pretty), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    pretty_commit = subprocess.Popen(shlex.split(cmd_git_log + commit_hash[0] + cmd_pretty), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print "[DEBUG] The rebased commit hash code for branch %s is: %s" %(branch, pretty_commit[0])
    list_commits = []
    while commit[0] != pretty_commit[0]:
        __add_reviewers(commit[0], reviewers) if reviewers else None
        __add_verify(commit[0]) if (verify == 1) else None
        list_commits.append(subprocess.Popen(shlex.split(cmd_git_log + cmd_oneline), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0])
        commit = subprocess.Popen(shlex.split(cmd_git_log + commit[0] + cmd_skip + cmd_pretty), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    mail_message = "echo -e \"Hi,\nCan you please review the follwing patches:\n\n" + str(list_commits) + "\n\nRegards, Maor. \" |mail -r " + reviewers + " -s \"please review patches\" -b mlipchuk@redhat.com " + reviewers
    print mail_message
    subprocess.Popen(shlex.split(mail_message), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def main(argv):
   reviewers, verify, brnach_name, send_mail = '', 0, '', 0
   try:
      opts, args = getopt.getopt(argv,"r:v:b:s",["reviewers=","verify=","branch=", "send_mail="])
   except getopt.GetoptError:
      print 'gerrit.py -r <reviewers_list> -v <true/false> -b <branch_name>, -s <true/false>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'gerrit.py -r <reviewers_list> -v <true/false> -b <branch_name>'
         sys.exit()
      elif opt in ("-r", "--reviewers"):
         reviewers = arg
      elif opt in ("-v", "--verify"):
         if arg == 'true':
             verify = 1;
      elif opt in ("-b", "--branch"):
         branch_name = arg;
      elif opt in ("-s", "--send_mail"):
         send_mail = 1
   print("[DEBUG] verify flag is: %i.  Reviewers list are: \"%s\".  Branch is \"%s\". Send mail is %i." %(verify, reviewers, branch_name, send_mail))
   change_patches(reviewers, verify, branch_name, send_mail)

if __name__ == "__main__":
   main(sys.argv[1:])

