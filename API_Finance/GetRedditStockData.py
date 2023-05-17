#Reddit API Top 50 Stocks Project
#input start date and number of days.
#capture daily top 50 from Reddit API
#Store these results in a dataframe
#Unique ID for each record
#Export as CSV
#API url = 'https://tradestie.com/api/v1/apps/reddit'

import pandas
import numpy
import requests
import datetime

#adds amount of days to start date to compute a range
def add_date_range(d, n):
    date_range = [d + datetime.timedelta(days=i) for i in range(n)]
    return(date_range)

#retrieves Top 50 Stocks Data per Day from add_date_range function
#creates one df as csv export
def get_redditAPI_data(datelist):
    requestl = []
    reddit_data = []
    reddit_data_dfl = []
    urlpart = 'https://tradestie.com/api/v1/apps/reddit?date='
    for dt in datelist:
        url = requests.get(urlpart + dt)
        requestl.append(url)
    for u in requestl:
        jsl = u.json()
        reddit_data.append(jsl)
    for i in reddit_data:
        reddit_dfp = pandas.DataFrame(i)
        reddit_data_dfl.append(reddit_dfp)
    reddit_df = pandas.concat(reddit_data_dfl)
    datelistn = [datetime.datetime.strptime(datelist[i], '%Y-%m-%d') for i in range(len(datelist))]
    datelistnm = datelistn * int(len(reddit_df)/len(datelistn))
    datelistnm_s = sorted(datelistnm)
    
    reddit_df['ID'] = reddit_df.index +1
    reddit_df["Date"] = datelistnm_s
    print(reddit_df.head(n=10))
    reddit_df.to_csv('reddit_df.csv', sep='|')


dt_inpt = input("Enter date YYYY-MM-DD")
dt_inptf = datetime.datetime.strptime(dt_inpt, '%Y-%m-%d')
int_inpt = int(input("How many days of data?"))
date_range = add_date_range(dt_inptf,int_inpt)
date_rangef = []
for single_date in date_range:
     s = single_date.strftime("%Y-%m-%d")
     date_rangef.append(s)

get_redditAPI_data(date_rangef)

