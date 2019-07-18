import sqlite3
import sys
import googlemaps
from datetime import datetime
from config import *


database = "D:\\2018_working\\coding\\googleMapsStreetview\\google_maps_data.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    print("method create_table called with create_table_sql:", create_table_sql)
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    #except Error as e:
    except:
        print("Unexpected error:", sys.exc_info()[0])
        #print(e)

def select_data(conn, sql):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    print("method select_data called with sql:", sql)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows
    #return data as dataframe??


def create_route(conn, route):
    """
    """
    sql = ''' INSERT INTO routes(StartAddress, EndAddress)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, route)
    conn.commit()
    return cur.lastrowid

def record_route_time(conn, routeTimeDur):
    """
    """
    sql = ''' INSERT INTO routeTimes(timeRouteID, startTime, distance, duration)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, routeTimeDur)
    conn.commit()
    return cur.lastrowid


def main():
    sql_create_routes_table = """ CREATE TABLE IF NOT EXISTS routes (
                                        routeID INTEGER PRIMARY KEY,
                                        StartAddress TEXT NOT NULL,
                                        EndAddress TEXT NOT NULL
                                        );
                                    """

    sql_create_routeTimes_table = """CREATE TABLE IF NOT EXISTS routeTimes (
                                timeRouteID INTEGER PRIMARY KEY,
                                startTime STRING  NOT NULL,
                                totDistance INTEGER NOT NULL,
                                totDuration INTEGER NOT NULL
                                );"""
                                #todo: fix this foreign key reference syntax.
                                #FOREIGN KEY (time_routeID) REFERENCES routes (routeID)

    sql_select_routes = """SELECT * FROM routes;"""

    # create a database connection
    print("opening database file : ", database)
    conn = sqlite3.connect(database)
    print("database opened.")
    if conn is not None:
        # create projects table
        print("connected to database.")
        print("sql_create_routes_table:", sql_create_routes_table)
        create_table(conn, sql_create_routes_table)
        # create tasks table
        print("sql_create_routeTimes_table:", sql_create_routeTimes_table)
        create_table(conn, sql_create_routeTimes_table)
        print("tables created.")
        #insert data into routes table
        #todo: prevent duplicates by using primary keys or ?
        route1 = ("Metroad 5, Toowong QLD 4066", "2 Rennies Rd, Indooroopilly QLD 4068")
        create_route(conn, route1)
        route2 = ("575 Moggill Rd, Chapel Hill QLD 4069", "Metroad 5, Toowong QLD 4066")
        create_route(conn, route2)
        routes = select_data(conn, sql_select_routes);
        #
        print("API_KEY:", API_KEY)
        gmaps = googlemaps.Client(key=API_KEY)
        for i in range(len(routes)):
            now = datetime.now()
            print("gettiing directions from "+routes[i][1] +" to "+ routes[i][2])
            directions_result = gmaps.directions(routes[i][1],
                                                 routes[i][2],
                                                 mode="driving",
                                                 departure_time=now)
            distance = directions_result[0]['legs'][0]['distance']['value']
            duration = directions_result[0]['legs'][0]['duration']['value']
            #
            print("i=", i)
            print("routeID:", routes[i][0])
            print("now=", now)
            print("distance=", distance)
            print("duration=", duration)
            routeTimeDur = (routes[i][0], now, distance, duration)
            record_route_time(conn, routeTimeDur)







    else:
        print("Error! cannot create the database connection.")

    #now get start & end points from database.


    print("end.")

if __name__ == '__main__':
    main()
