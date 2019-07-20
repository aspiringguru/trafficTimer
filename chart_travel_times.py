import tools
from config import *
import googlemaps
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

#NB: needed upgrade from anaconda default version
#pip list | findstr matplotlib
#pip install --upgrade matplotlib
#upgrade from anaconda default version 3.0.3 to 3.1.1

#this below fixes warning message.
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def main():
    # initialise googlemaps.Client once, maybe add error trapping??
    print("API_KEY:", API_KEY)
    print("DATABASE_FILE:", DATABASE_FILE)
    gmaps = googlemaps.Client(key=API_KEY)
    print("gmaps: ", gmaps)
    # create a database connection
    conn = tools.create_connection(DATABASE_FILE)
    if conn is not None:
        # create projects table
        print("connected to database.")
        sql = """SELECT * FROM routeTimes
                WHERE StartAddress = ?
                AND EndAddress = ?
        """
        params = ("Metroad 5  Toowong QLD 4066","2 Rennies Rd Indooroopilly QLD 4068")
        results = tools.select_data_extended(conn, sql, params)
        print("type(results):", type(results))
        print("len(results):", len(results))
        df = pd.DataFrame(columns=['time', 'duration'])
        durations = []
        times = []
        for result in results:
            print(result)
            #time format = '2019-07-19 20:21:11.152823'
            # 'yyyy-mm-dd hh:mm:ss.123456'
            time = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S.%f')
            print("time:", time)
            times.append(time)
            durations.append(result[4])
            #break
        plt.plot(times, durations)
        plt.ylabel('Trip Duration (seconds)')
        plt.xlabel('Time of day.')
        xticksStepSize = (max(times) - min(times))/5.
        plt.xticks(rotation=45, ha='right')
        plt.xticks(np.arange(min(times), max(times), step=xticksStepSize))
        plt.title('Trip time from \n' + params[0] +"\n to "+ params[1])
        #save figure before plotting.
        #plt.savefig('test.png')
        plt.show()



if __name__ == '__main__':
    main()
