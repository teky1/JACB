import sqlite3

"""
import sqlite3
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE balances (UserID varchar(24) UNIQUE, Balance varchar(32))")
connection.commit()
"""

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def getBalance(userID: int):
    userID = str(userID)
    cursor.execute("SELECT Balance FROM balances WHERE UserID=?", (userID,))
    selection = cursor.fetchone()
    if selection:
        return int(selection[0])
    else:
        cursor.execute("INSERT INTO balances (UserID, Balance) VALUES(?, ?)", (userID, str(0)))
        connection.commit()
        cursor.execute("SELECT Balance FROM balances WHERE UserID=?", (userID,))
        return int(cursor.fetchone()[0])

def setBalance(userID: int, newBal: int):
    # run getBalance just to create an entry in the database if it doesn't already exist
    getBalance(userID)

    userID = str(userID)
    newBal = str(newBal)

    cursor.execute("UPDATE balances SET Balance=? WHERE UserID=?", (newBal, userID))
    connection.commit()


