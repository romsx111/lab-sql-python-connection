import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME")
)

engine = create_engine(url)


def rentals_month(engine, month, year):
    query = f"""
    SELECT *
    FROM rental
    WHERE MONTH(rental_date) = {month}
    AND YEAR(rental_date) = {year};
    """
    
    return pd.read_sql(query, engine)


def rental_count_month(df, month, year):
    column_name = f"rentals_{month:02d}_{year}"
    
    return (
        df.groupby("customer_id")
          .size()
          .reset_index(name=column_name)
    )


def compare_rentals(df1, df2):
    comparison = pd.merge(
        df1,
        df2,
        on="customer_id",
        how="outer"
    ).fillna(0)

    col1 = df1.columns[1]
    col2 = df2.columns[1]

    comparison["difference"] = comparison[col2] - comparison[col1]

    return comparison