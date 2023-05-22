
###### PACKAGES ######
import sys
import pandas as pd
import logging
import warnings
import pymysql
import ssl
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
import pytz
import time
import dateutil.parser
import flask
import datetime
from functools import wraps
from flask import Flask, request, Response, render_template
import numpy as np
import math
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mysqldb import MySQL

sys.path.append("/root/past-precipitation")
import initialize_mysql_rain
from local_settings import *
from initialize_mysql_rain import *

app = Flask(__name__)


def timetz(*args):
    return datetime.datetime.now(tz).timetuple()


# logging datetime in PST
tz = timezone("US/Pacific")
logging.Formatter.converter = timetz

logging.basicConfig(
    filename="/logs/myproject.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt=f"%Y-%m-%d %H:%M:%S ({tz})",
)

limiter = Limiter(app, default_limits=["500 per day", "50 per hour"])

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://%s:%s@%s/%s" % (
    MYSQL_AUTH["user"],
    MYSQL_AUTH["password"],
    MYSQL_AUTH["host"],
    "rain",
)

db = SQLAlchemy(app)


@app.route("/")
def base():
    return render_template("index.html")


@app.route("/research")
def research():
    return render_template("research.html")

@app.route("/rain")
def rain_app():
    return render_template("rain_service.html", location_names=location_names)


@app.route("/rain", methods=(["POST"]))
def rain_gen_html_table():
    i_location_name = str(request.form["i_location_name"])
    i_location_lat, i_location_lon = (
        lat_lon_dict[i_location_name]["lat"],
        lat_lon_dict[i_location_name]["lon"],
    )
    try:
        conn = db.engine.connect()
        df_pre = pd.read_sql_query(
            f"""
            SELECT  
                MIN(SUBSTR(CONVERT_TZ(FROM_UNIXTIME(dt),'UTC','US/Pacific'),1,13)) AS "First API Update Hour (PST)",
                MAX(SUBSTR(CONVERT_TZ(FROM_UNIXTIME(dt),'UTC','US/Pacific'),1,13)) AS "Last API Update Hour (PST)",
                MAX(CONVERT_TZ(FROM_UNIXTIME(requested_dt),'UTC','US/Pacific')) AS "Last API Request Time (PST)"
            FROM 
                rain.tblFactLatLon 
            WHERE 
                location_name = "{i_location_name}" 
                AND lat = {i_location_lat} 
                AND lon = {i_location_lon}
            """,
            conn,
        )
        df = pd.read_sql_query(
            f"""
        SELECT  
            location_name AS "Location Name",
            {i_location_lat} AS "Latitude",
            {i_location_lon} AS "Longitude",
            SUBSTR(CONVERT_TZ(FROM_UNIXTIME(dt),'UTC','US/Pacific'),1,13) AS "Weather Date Hour (PST)",
            MAX(rain_1h) AS "Rainfall (mm) Last 1 hour" 
        FROM 
            rain.tblFactLatLon 
        WHERE 
            location_name = "{i_location_name}" 
            AND lat = {i_location_lat} 
            AND lon = {i_location_lon} 
            AND (rain_1h > 0) 
        GROUP BY 
            1,2,3,4
        ORDER BY 
            4 DESC
        """,
            conn,
        )
    finally:
        conn.close()
    return render_template(
        "rain_service_result.html",
        tables=[df_pre.to_html(classes="data"), df.to_html(classes="data")],
        titles=np.concatenate([df_pre.columns.values, df.columns.values]),
    )


@app.route("/klaviyo")
def klaviyo():
    return "<h1 style='color:brown'>Klaviyo Weather App</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
