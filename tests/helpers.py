"""
This file contains functions / classes helpful in testing an applicaiton.
"""
import csv
from datetime import datetime

from src.database.models import db


def insert_test_data_into_db_table(table_obj):
    """ Insert test data from CSV file into DB table.

    Args:
        table_obj (SQLAlchemy table object): database table object
    """
    csv_paths = {
        "resources": "tests/data/resources_data.csv",
        "users": "tests/data/users_data.csv",
        "bookings": "tests/data/bookings_data.csv",
    }
    with open(csv_paths[table_obj.__tablename__]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        param_dict = dict()
        for row in csv_reader:
            if table_obj.__tablename__ == "resources":
                param_dict["title"] = row[0]
                param_dict["created_at"] = datetime.strptime(
                    row[1], "%Y-%m-%d %H:%M:%S"
                )
                param_dict["updated_at"] = datetime.strptime(
                    row[2], "%Y-%m-%d %H:%M:%S"
                )
                param_dict["active"] = str2bool(row[3])
                param_dict["intervals"] = row[4]
                param_dict["opening_hours_mon"] = row[5]
                param_dict["opening_hours_tue"] = row[6]
                param_dict["opening_hours_wed"] = row[7]
                param_dict["opening_hours_thu"] = row[8]
                param_dict["opening_hours_fri"] = row[9]
                param_dict["opening_hours_sat"] = row[10]
                param_dict["opening_hours_sun"] = row[11]
            elif table_obj.__tablename__ == "users":
                param_dict["created_at"] = datetime.strptime(
                    row[0], "%Y-%m-%d %H:%M:%S"
                )
                param_dict["updated_at"] = datetime.strptime(
                    row[1], "%Y-%m-%d %H:%M:%S"
                )
                param_dict["name"] = row[2]
                param_dict["email"] = row[3]
                param_dict["phonenumber"] = row[4]
            elif table_obj.__tablename__ == "bookings":
                param_dict["resource_id"] = row[0]
                param_dict["user_id"] = row[1]
                param_dict["booked_from"] = datetime.strptime(
                    row[2], "%Y-%m-%d %H:%M:%S"
                )
                param_dict["booked_to"] = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
                param_dict["notes"] = row[4]
            db_data = table_obj(**param_dict)
            db.session.add(db_data)
            db.session.commit()


def str2bool(str_var):
    return str_var.lower() in ("true", "1")
