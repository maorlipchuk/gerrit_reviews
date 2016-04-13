# gerrit_reviews
Use "./add_reviewers.py --help" to know all the commands:
Should give you the following output:

add_reviewers.py -r <reviewers_list> -v <true/false> -b <branch_name>, -s <true/false>

r is for a list of reviewers to add to the patch
v is for verify flag
b is for branch - the first commit to start from (same as you indicate when you rebase your patchset)
s is for sending an automatic mail to the reviewers to remind them to start reviewing

For example if you want to add reviewer to your project and mark it as verify,
from your root folder in your project you can just execute the following command:
  ../gerrit_reviews/add_reviewers.py -r mlipchuk@redhat.com -v true -b origin/master
  
