import os
import json
import requests
import csv

# This script is designed to run after JoshGerontis_CollectFiles.py to analyze authorship of file touches

# load up token
token = os.environ.get("GITHUB_TOKEN", "").strip()
if not token:
    raise SystemExit("Set the GITHUB_TOKEN environment variable before running this script.")

# set repo
repo = 'scottyab/rootbeer'

# GitHub Authentication function
# @param url: The GitHub API URL to fetch data from
# @param token: The GitHub authentication token
# @return: json data
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


def get_edit_authors_for_file(repo, filename, token):
    # get commits first
    url = f"https://api.github.com/repos/{repo}/commits?path={filename}"
    commits = github_auth(url, token)
    edit_authors = {}
    if commits:
        for commit in commits:
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date'].split('T')[0]
            if author not in edit_authors:
                edit_authors[author] = []
            edit_authors[author].append(date)
    return edit_authors

# unique list of authors
authors = []

# store each file's edits by whom and when
# e.g. {'example.java': {'author1': ['2024-01-01', '2024-01-02'], 'author2': ['2024-01-03']}}
file_edits = {}

# get list of files from file_touches_count CSV
file_touches_count = 'data/file_touches_count_' + repo.split('/')[1] + '.csv'    
files = []
with open(file_touches_count, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        files.append(row[0])

# find all the editors of each file
for file in files:
    edit_authors = get_edit_authors_for_file(repo, file, token)
    file_edits[file] = edit_authors
    for author in edit_authors:
        if author not in authors:
            authors.append(author)
    print(f"File: {file}")
    for author, dates in edit_authors.items():
        print(f"  Author: {author}")
        for date in dates:
            print(f"    Date: {date}")

# store results to csv
fileOutput = 'data/file_authors_' + repo.split('/')[1] + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)
for file, edit_authors in file_edits.items():
    for author, dates in edit_authors.items():
        for date in dates:
            writer.writerow([file, author, date])
fileCSV.close()