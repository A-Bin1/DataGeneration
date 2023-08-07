#UserData retrieved from API source and stored in database
#create dataframe from dictionary data type
# Sample API URL: https://randomuser.me/api/

import requests
import pandas as pd
import argparse
import warnings
from sqlalchemy import create_engine
import multiprocessing
from multiprocessing import Pool

warnings.simplefilter(action='ignore', category=FutureWarning)


parser = argparse.ArgumentParser(description = "Script will generate a table in DB of contact information", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--Size", "-N", help = "Number of contacts to be generated", required = True, type=int)
args = parser.parse_args()


def main():
	#connect to PostgreSQL DB
    conn_string = 'postgresql://user:password@localhost'
    db = create_engine(conn_string)
    conn = db.connect()
    url = "https://randomuser.me/api/"
    requests_list= []
    for contact in range(args.Size):
        requests_list.append(requests.get(url).json())

    # Create Pandas Data Frame as Splash Table in PostGreSQL Database
    contacts = pd.json_normalize(requests_list.pop(0), record_path=["results"])
    for contact in requests_list:
        contacts = contacts._append(pd.json_normalize(contact, record_path=["results"]))
        contactsdb = contacts.filter(items=['login.username', 'login.password', 'email',
                                            'location.city', 'location.country', 'registered.date'])
    
    contactsdb = pd.DataFrame(contactsdb)
    contactsdb.rename(columns={'login.username': 'Username', 'login.password': 'Password',
                                   'location.city': 'City', 'location.country': 'Country',
                                   'registered.date': 'Registered_Date'}, inplace=True)
    
    
    #print(contactsdb['Registered_Date'].dtype)
    contactsdb["Registered_Date"] = pd.to_datetime(contactsdb["Registered_Date"], errors='coerce')
    #({'date': 'datetime64[ns]'})
    contactsdb.to_sql('accounts_splash', con = conn, if_exists='append', index = False)
    
    return






if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=main)
        jobs.append(p)
        p.start()


