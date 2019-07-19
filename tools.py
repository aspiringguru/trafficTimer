import sqlite3
import sys
import googlemaps
from datetime import datetime
from config import *
import pandas as pd
import time


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
    #for row in rows:
    #    print(row)
    return rows


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
    sql = ''' INSERT INTO routeTimes(StartAddress, EndAddress, startTime, distance, duration)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, routeTimeDur)
    conn.commit()
    return cur.lastrowid


def setup_db(conn):
    """
    """
    print("in method setup_db(conn): type(conn)=", type(conn))
    sql_create_routes_table = """ CREATE TABLE IF NOT EXISTS routes (
                                        routeID INTEGER PRIMARY KEY,
                                        StartAddress TEXT NOT NULL,
                                        EndAddress TEXT NOT NULL
                                        );
                                    """

    sql_create_routeTimes_table = """CREATE TABLE IF NOT EXISTS routeTimes (
                                StartAddress TEXT NOT NULL,
                                EndAddress TEXT NOT NULL,
                                startTime TEXT  NOT NULL,
                                distance INTEGER NOT NULL,
                                duration INTEGER NOT NULL
                                );
                                """
                                #todo: fix this foreign key reference syntax.
                                #FOREIGN KEY (time_routeID) REFERENCES routes (routeID)
    print("in method setup_db(conn): type(sql_create_routes_table)=", type(sql_create_routes_table))
    print("sql_create_routes_table:", sql_create_routes_table)
    create_table(conn, sql_create_routes_table)
    print("table routes created.")
    # create tasks table
    print("sql_create_routeTimes_table:", sql_create_routeTimes_table)
    create_table(conn, sql_create_routeTimes_table)
    print("tables created.")


def load_routes():
    """
    load routes from csv file, store in database if not already there
    """
    print("loading ROUTES_CSV_FILE:", ROUTES_CSV_FILE)
    data = pd.read_csv(ROUTES_CSV_FILE)
    print("data.head(): \n", data.head())
    print("data.shape:", data.shape)
    return data

def get_route_data(gmaps, route):
    """
    """
    now = datetime.now()
    print("getting directions from "+route[0] +" to "+ route[1] + " at time = ", now)
    directions_result = gmaps.directions(route[0],
                                         route[1],
                                         mode="driving",
                                         departure_time=now)
    distance = directions_result[0]['legs'][0]['distance']['value']
    duration = directions_result[0]['legs'][0]['duration']['value']
    #
    print("start:", route[0])
    print("end:", route[1])
    print("now=", now)
    print("distance=", distance)
    print("duration=", duration)
    routeTimeDur = (route[0], route[1], now, distance, duration)
    return routeTimeDur
