import json
import requests
import os
import csv

# This script generates a report of GitHub pull request details for a specified repository.

if not os.path.exists("data"):
    os.makedirs("data")

# load up token
token = os.environ.get("GITHUB_TOKEN", "").strip()
if not token:
    raise SystemExit("Set the GITHUB_TOKEN environment variable before running this script.")

# set working repo
repo = "apache/kafka"

# specify which PRs you want to retrieve details for
prs = [11791, 11686, 11591, 12159, 12073, 11981, 11867, 11991, 12207, 11926, 11847]

# GitHub Authentication function
def github_auth(url, token):
    jsonData = None
    try:
        headers = {'Authorization': 'Bearer {}'.format(token)}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
    except Exception as e:
        pass
        print(e)
    return jsonData

def get_pull_request_data(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    return github_auth(url, token)

def get_pull_request_files(repo, pr_number, token):
    files = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}"
        result = github_auth(url, token)
        if not isinstance(result, list):
            raise RuntimeError(f"Error retrieving files for PR {pr_number}, page {page}")
        files.extend(result)
        if len(result) < 100:
            return files
        page += 1

# retrieve and save pull request details for each specified PR
pr_details = []
for pr in prs:
    print(f"Retrieving details for PR {pr}...")
    result = get_pull_request_data(repo, pr, token)
    if result:
        author = (result.get("user") or {}).get("login", "")
        merged_at = result.get("merged_at") or ""
        for file_details in get_pull_request_files(repo, pr, token):
            pr_details.append([repo, pr, author, result.get("merge_commit_sha"), merged_at,
                               file_details["filename"], file_details["status"],
                               file_details["additions"], file_details["deletions"]])

with open(f"data/pr_details_{repo.split('/')[1]}.csv", "w", newline="") as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(["RepoName", "PR Number", "PR Author", "Merge Commit", "Merged At",
                     "Filename", "Status", "Added", "Deleted"])
    writer.writerows(pr_details)


