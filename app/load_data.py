import os
from subprocess import run
import pandas as pd
from sqlalchemy import create_engine

def load_data(csv_path, table_name):
    run('echo loading ' + csv_path + ' to table ' + table_name, shell=True, check=True)
    uri=os.environ.get('SQLALCHEMY_DATABASE_URI')
    engine = create_engine(uri)
    data = pd.read_csv(csv_path)
    data.to_sql(name=table_name,
                con=engine,
                if_exists="replace",
                index=False)

load_data("data/manufacturers.csv", 'manufacturers')
#load_data("data/manufacturer_dtcs.csv", 'manufacturer_dtcs')
