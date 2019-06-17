"""
This file contains
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import select
from datetimerange import DateTimeRange
from dateutil.relativedelta import relativedelta
import subprocess

from src.database.models import Resources, Slots
from src.cli import DB_ENGINE

connection = DB_ENGINE.connect()
Session = sessionmaker(bind=DB_ENGINE)
session = Session()


def ensure_cron_service_is_running():
    """ Make sure cron Linux service is up and running. """
    try:
        subprocess.run(['service', 'cron', 'status'], stdout=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        print("Cron service is not running, starting procedure launched...")
        try:
            subprocess.run(['service', 'cron', 'start'], stdout=subprocess.DEVNULL,
                           check=True)
        except subprocess.CalledProcessError as err:
            print('Cannot start cron service. Error: ', err)


def generate_timeslots_dict(work_hours_list, interval):
    """

    Args:
        work_hours_list:
        interval:

    Returns:

    """
    timeslots_dict = dict()
    if len(work_hours_list) == 1:
        time_range = DateTimeRange(work_hours_list[0], work_hours_list[-1])
        timeslots_dict = {value: 1 for value in
                          time_range.range(relativedelta(minutes=+int(interval)))}
    elif len(work_hours_list) == 4:
        first_time_range = DateTimeRange(work_hours_list[0], work_hours_list[1])
        first_timeslots_dict = {value: 1 for value in first_time_range.range(
                                relativedelta(minutes=+int(interval)))}
        second_time_range = DateTimeRange(work_hours_list[1], work_hours_list[2])
        second_timeslots_dict = {value: 0 for value in second_time_range.range(
                                relativedelta(minutes=+int(interval)))}
        third_time_range = DateTimeRange(work_hours_list[2], work_hours_list[3])
        third_timeslots_dict = {value: 1 for value in third_time_range.range(
                                relativedelta(minutes=+int(interval)))}
        timeslots_dict.update(first_timeslots_dict)
        timeslots_dict.update(second_timeslots_dict)
        timeslots_dict.update(third_timeslots_dict)
    return timeslots_dict


def resultproxy_to_dict_list(sql_alchemy_rowset):
    """ Convert ResultProxy SQLAlchemy object to list of dictionaries.

    Args:
        sql_alchemy_rowset (ResultProxy): ResultProxy query result object

    Returns:

    """
    return [{tuple[0]: tuple[1] for tuple in rowproxy.items()}
                                for rowproxy in sql_alchemy_rowset]


def add_slots_every_day():
    """ Add slots to the database once a day. """
    ensure_cron_service_is_running()
    meta = MetaData(DB_ENGINE, reflect=True)
    resources_table = meta.tables['resources']
    s = select([resources_table])
    resources_query_result = connection.execute(s)
    base = datetime.today()
    end = base + timedelta(days=90)
    end_str = end.strftime('%Y-%m-%d')
    day_name = end.strftime("%A")
    resources_num = len(resultproxy_to_dict_list(resources_query_result))
    print(resultproxy_to_dict_list(resources_query_result), '<<<')
    resources_query_result = connection.execute(s)
    for resource_data in resources_query_result:
        days_culumns_dict = {
            "Monday": resource_data.opening_hours_mon,
            "Tuesday": resource_data.opening_hours_tue,
            "Wednesday": resource_data.opening_hours_wed,
            "Thursday": resource_data.opening_hours_thu,
            "Friday": resource_data.opening_hours_fri,
            "Saturday": resource_data.opening_hours_sat,
            "Sunday": resource_data.opening_hours_sun
        }
        dash_count = days_culumns_dict[day_name].count('-')
        hours = days_culumns_dict[day_name].split('-')

        # do nothing when dash_count == 0, resource does not work this day
        if dash_count != 0:
            dates = [datetime.strptime(end_str + " " + hour + ":00", "%Y-%m-%d %H:%M:%S")
                     for hour in hours]
            timeslots_dict = generate_timeslots_dict(dates, resource_data.intervals)

            # TODO: get available resources and check if given slot exists
            for timestamp, free in timeslots_dict.items():
                # TODO: bug, last slot should not be added
                timestamp_end = timestamp + timedelta(minutes=int(resource_data.intervals))
                db_data = Slots(
                    timestamp=timestamp,
                    timestamp_end=timestamp_end,
                    formatted_timestamp=timestamp.strftime("%A, %B, %d, %Y, %H:%M %p"),
                    formatted_timestamp_end=timestamp_end.strftime("%A, %B, %d, %Y, %H:%M %p"),
                    free=free,
                    available_resources="2",
                    maximum_capacity=resources_num,
                )
                session.add(db_data)
                session.commit()


if __name__ == "__main__":
    add_slots_every_day()
