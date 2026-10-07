import matplotlib
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta
# This script is designed to create scatter plots from the data collected in JoshGerontis_authorsFileTouches.py
# need to load csv data, parse the week range, make a color for each author, and plot the scatter plot

# load data from CSV
repo = 'scottyab/rootbeer'
file_authors_csv = 'data/file_authors_' + repo.split('/')[1] + '.csv'
data = []
with open(file_authors_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        data.append(row)


def get_week(date_str, first_week_start):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (date_obj - first_week_start).days // 7 + 1

# append the week number to each row based on the date
earliest_date = min(datetime.strptime(row[2], "%Y-%m-%d") for row in data)
first_week_start = earliest_date - timedelta(days=earliest_date.weekday())
for row in data:
    row.append(get_week(row[2], first_week_start))
files = sorted(set(row[0] for row in data))
weeks = list(set(row[3] for row in data))
authors = list(set(row[1] for row in data))

# create a color mapping for each author
colors = matplotlib.colormaps['tab10'].resampled(len(authors))
author_color = {author: colors(i) for i, author in enumerate(authors)}

# plot the scatter plot
plt.figure(figsize=(10, 6), layout='constrained')
for row in data:
    file, author, date, week = row[0], row[1], row[2], row[3]
    plt.scatter(files.index(file), week, color=author_color[author], label=author)

# create a legend with unique authors
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))

plt.legend(by_label.values(), by_label.keys(),bbox_to_anchor=(1.05, 1), loc='upper left')

plt.xlabel('File')
plt.ylabel('Week')
plt.title('File Edits by Author and Week')
plt.show()






