#Reddit API Top 50 Stocks Project
#input start date and number of days.
#capture daily top 50 from Reddit API
#Store these results in a dataframe
#Unique ID for each record
#Export as CSV
#API url = 'https://tradestie.com/api/v1/apps/reddit'

import pandas
import requests
import datetime
import argparse

parser = argparse.ArgumentParser(description = "Script will generate a csv file of Stock Data from Reddit", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--Number", "-N", help = "Number of days to be generated for Date Range", required = True, type=int)
parser.add_argument("--StartDate", "-D", help = "Start Date of Range", required = True)
parser.add_argument("--Output", "-O", help = "Name of output file. CSV format", required = True)
args = parser.parse_args()


def get_redditAPI_data():
    startDateV = datetime.datetime.strptime(args.StartDate, '%Y-%m-%d')
    datelist = ([startDateV + datetime.timedelta(days=i) for i in range(args.Number)])
    datelistf = ([d.strftime('%Y-%m-%d') for d in datelist])
    requestl = []
    reddit_data = []
    reddit_data_dfl = []
    urlpart = 'https://tradestie.com/api/v1/apps/reddit?date='
    for dt in datelistf:
        url = requests.get(urlpart + dt)
        requestl.append(url)
    for u in requestl:
        jsl = u.json()
        reddit_data.append(jsl)
    for i in reddit_data:
        reddit_dfp = pandas.DataFrame(i)
        reddit_data_dfl.append(reddit_dfp)
    reddit_df = pandas.concat(reddit_data_dfl)
    datelistn = [datetime.datetime.strptime(datelistf[i], '%Y-%m-%d') for i in range(len(datelistf))]
    datelistnm = datelistn * int(len(reddit_df)/len(datelistn))
    datelistnm_s = sorted(datelistnm)
    
    reddit_df['ID'] = reddit_df.index +1
    reddit_df["Date"] = datelistnm_s
    reddit_df.to_csv(args.Output, sep=',')
    return


if __name__ == '__main__':
    get_redditAPI_data()



