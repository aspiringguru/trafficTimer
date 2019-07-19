import tools
from config import *
import googlemaps
import pandas as pd
import matplotlib.pyplot as plt

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
        for result in results:
            print(result)
            durations.append(result[4])
            #break
        plt.plot(durations)
        plt.ylabel('Trip Duration')
        plt.show()



if __name__ == '__main__':
    main()
