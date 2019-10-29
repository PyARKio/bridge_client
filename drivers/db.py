# -- coding: utf-8 --
from __future__ import unicode_literals
import sqlite3
from drivers.log_settings import log


def init_db(name_db):
    try:
        conn = sqlite3.connect('{}.db'.format(name_db))  # или :memory: чтобы сохранить в RAM
    except Exception as err:
        print(err)
        log.error(err)
        return False, False
    else:
        log.info('Init db <{}>: successfully'.format(name_db))
        try:
            cursor = conn.cursor()
        except Exception as err:
            print(err)
            log.error(err)
            return False, False
        else:
            log.info('Create cursor for db <{}>: successfully'.format(name_db))
            return conn, cursor


def get_metadata(conn, cursor):
    # cursor.execute("CREATE DATABASE {} ;".format('test2'))
    print(conn.get_dsn_parameters(), "\n")
    cursor.execute("SELECT version();")
    # cursor.execute("SELECT all;")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")


def create_table_head_data_in_db(cursor):
    # Execute a command: this creates a new table
    try:
        cursor.execute("CREATE TABLE head_data ("
                       "battery_name varchar, "
                       "discharge_current int, "
                       "start_at_in_sec timestamp, "
                       "start_at_in_date timestamp);")
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Create table <head_data>: successfully')
        return True


def create_table_in_db(cursor):
    # Execute a command: this creates a new table
    try:
        cursor.execute("CREATE TABLE data ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "time_sec timestamp, "
                       "time_in_date timestamp, "
                       "back_up varchar );")
    except sqlite3.OperationalError as err:
        log.info(err)
        return True
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Create table <data>: successfully')
        return True


def insert_into_head_data(cursor, bat_name, dis, in_sec, in_date):
    try:
        cursor.execute("INSERT INTO head_data ("
                       "battery_name, "
                       "discharge_current, "
                       "start_at_in_sec, "
                       "start_at_in_date) VALUES(?, ?, ?, ?)", (bat_name, str(dis), in_sec, in_date))
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Insert in table <head_data> {} {} {} {}: successfully'.format(bat_name, str(dis), in_sec, in_date))
        return True


def insert_into_db(cursor, in_sec, in_date, back_up):
    try:
        cursor.execute("INSERT INTO data ("
                       "time_sec, "
                       "time_in_date, "
                       "back_up) VALUES(?, ?, ?)", (in_sec, in_date, back_up))
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info("INSERT INTO data ("
                 "time_sec, "
                 "time_in_date, "
                 "back_up) VALUES({}, {}, {})".format(in_sec, in_date, back_up))
        return True


def select_from_db(cursor, name_table_in_db, param='*'):
    try:
        cursor.execute("SELECT {} FROM {};".format(param, name_table_in_db))
        # cursor.execute("SELECT {} FROM {} WHERE volt > 2400;".format(param, name_table_in_db))
    except Exception as err:
        log.error(err)
        return False
    else:
        try:
            data = cursor.fetchall()
        except Exception as err:
            log.error(err)
            return False
        else:
            log.info('Select {} from table {}: successfully'.format(param, name_table_in_db))
            # print(len(data))
            # print(data)
            #
            # for line in data:
            #     print(line)

            return data


def delete_from_table_in_db(cursor, value, name_table_in_db=None, key=None):
    # sql = 'DELETE FROM {} WHERE {} = {}'.format(name_table_in_db, key, value)
    # cursor.execute(sql)
    cursor.execute("DELETE FROM data WHERE id = {}".format(value))


def commit_changes(conn):
    # Make the changes to the database persistent
    try:
        conn.commit()
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Commit: successfully')
        return True


def disconnect_from_db(conn, cursor):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")


def select_all_table(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    log.debug(tables)
    return tables


if __name__ == '__main__':
    name = 'Li-ion 1570524950.6613283'
    # db_conn, db_cursor = init_db('d:\qua\Check_battery_software\Energizer CR2 1568818428.4618394')
    db_conn, db_cursor = init_db('d:\qua\Check_battery_software\{}'.format(name))
    # db_conn, db_cursor = init_db('d:\QUA\Check_battery_software\\tr 1568881882.8805368')
    volt = select_from_db(db_cursor, name_table_in_db='battery_data', param='volt')
    print(volt[0][0])
    print(volt[-1][0])
    data_time = select_from_db(db_cursor, name_table_in_db='battery_data', param='time_sec')
    print(data_time[0])
    print(data_time[-1])
    delta_3600 = (int(data_time[-1][0]) - int(data_time[0][0])) / 3600
    print(delta_3600)
    print(delta_3600 * 32)
    data_time = select_from_db(db_cursor, name_table_in_db='battery_data', param='time_in_date')
    # select_from_db(db_cursor, name_table_in_db='head_data')
    select_from_db(db_cursor, name_table_in_db='sqlite_sequence')
    select_all_table(db_cursor)
    disconnect_from_db(db_conn, db_cursor)

    # plot_start = Process(target=one_plot, args=([volt, data_time], 'VOLT'))
    # plot_start.start()

    one_plot([volt, data_time], yLabel='VOLT', sensor_name='{} {} {}mA'.format(name.split(' ')[0],
                                                                               name.split(' ')[1],
                                                                               delta_3600 * 32))

    # import time

    # time.sleep(50)


