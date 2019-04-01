"""
This file contains functions / classes helpful in testing an applicaiton.
"""
import csv
from datetime import datetime

from src.database.models import db


def insert_test_data_into_db_table(table_obj):
    """ Insert test data from CSV file into DB table.

    Args:
        table_obj:

    Returns:

    """
    csv_paths = {
        "resources": "tests/data/resources_data.csv",
        "users": "tests/data/users_data.csv",
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
            db_data = table_obj(**param_dict)
            db.session.add(db_data)
            db.session.commit()


def str2bool(str_var):
    return str_var.lower() in ("true", "1")
