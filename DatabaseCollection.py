import HypixelData
import mysql.connector
import time
import locale
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()

locale.setlocale(locale.LC_ALL, 'en_US')

'''
Opens the database connection
'''


def db_open() -> dict:

    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")

    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS, database=DB_NAME)
    cursor = cnx.cursor()
    return {"Cursor": cursor, "Connection": cnx}


'''
Closes the database connection
'''


def db_close(cnx) -> None:
    cnx.commit()
    cnx.close()


'''
Appends the Data Request to the database for future exploration.
'''


def update_dld_data(data: dict) -> bool:
    db = db_open()
    cursor = db["Cursor"]

    with open("scuffedNames.json", 'r') as file:
        scuffNames = json.load(file)

    SQL = "INSERT INTO `allproducts` " \
          "(`allProdID`, `buyVolume`, `sellVolume`, `sellOrders`, `buyOrders`, `buyPrice`, `sellPrice`, " \
          "`buyMovingWeekly`, `sellMovingWeekly`, `RoI`, `margin`, `reliability`, `avgVolume`, `event`, `datetime`," \
          "`productName`) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    currentTime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


    for product in data:

        if product in scuffNames:
            productName = scuffNames[product]

            product = data[product]
            inputs = (0,
                      int(product['buyVolume']),
                      int(product['sellVolume']),
                      int(product['sellOrders']),
                      int(product['buyOrders']),
                      int(product['buyPrice']),
                      int(product['sellPrice']),
                      int(product['buyMovingWeek']),
                      int(product['sellMovingWeek']),
                      round(product['RoI'], 2),
                      round(product['margin'], 2),
                      int(product['reliability']),
                      int(product['avgVolume']),
                      int(product['event']),
                      currentTime,
                      productName)

            cursor.execute(SQL, inputs)
    
    db_close(db["Connection"])
    return True


'''
Infinite Run of db collection to continue doing this every 2 minutes.
Error catching is there just in case (Nothing has or should ever prompt an error)
'''

def run_db() -> None:
    while True:
        try:

            files = ["models/abc.sav", "models/bagging.sav", "models/extratrees.sav", "models/KNN.sav",
                     "models/randomforest.sav", "models/gradientboosting.sav"]
            # Get Data from API Call
            currentData = HypixelData.gather_bazaar_data(API_KEY="", fileList=files)

            # Add Data to "OLD" Data Table
            update_dld_data(data=currentData)

            print("DB Update Completed on ", datetime.now())

            time.sleep(120)
        except ValueError:

            run_db()


if __name__ == '__main__':
    run_db()
