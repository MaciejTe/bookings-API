"""
This file contains functions / classes helpful in testing an applicaiton.
"""
import csv
from datetime import datetime

from src.database.models import db


def insert_data_into_resources_table(table_obj):
    with open('tests/resources_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            title = row[0]
            created_at = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            updated_at = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            active = str2bool(row[3])
            db_data = table_obj(title=title, created_at=created_at, active=active,
                                updated_at=updated_at)
            db.session.add(db_data)
            db.session.commit()


def str2bool(str_var):
    return str_var.lower() in ('true', '1')
