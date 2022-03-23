import sqlite3
import json

"""
import sqlite3
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE inventories (ItemID SMALLINT, UserID varchar(24), Count INT)")
connection.commit()
"""

with open("items.json") as item_data_file:
    item_data = json.load(item_data_file)

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def getItemCount(userID: int, itemID: int):
    userID = str(userID)
    cursor.execute("SELECT Count FROM inventories WHERE UserID=? AND ItemID=?", (userID, itemID))
    selection = cursor.fetchone()
    if selection:
        return selection[0]
    else:
        return 0

def setItem(userID: int, itemID: int, amount: int):
    userID = str(userID)
    cursor.execute("SELECT Count FROM inventories WHERE UserID=? AND ItemID=?", (userID, itemID))
    selection = cursor.fetchone()
    if selection:
        cursor.execute("UPDATE inventories SET Count=? WHERE UserID=? AND ItemID=?", (amount, userID, itemID))
    else:
        cursor.execute("INSERT INTO inventories (ItemID, UserID, Count) VALUES(?, ?, ?)", (itemID, userID, amount))
    connection.commit()

def addItem(userID: int, itemID: int, count=1):
    amount = getItemCount(userID, itemID)
    setItem(userID, itemID, amount+count)

def removeItem(userID: int, itemID: int, count=1):
    amount = getItemCount(userID, itemID)
    new_amount = amount - count if count <= amount else 0
    setItem(userID, itemID, new_amount)

def getInventory(userID: int):
    userID = str(userID)
    cursor.execute("SELECT ItemID, Count FROM inventories WHERE UserID=?", (userID,))
    inventory = cursor.fetchall()
    return inventory

def getItemData(id: int):
    return item_data[id]

def formatItemName(id: int, quantity=1):
    item = getItemData(id)
    return f"**{quantity} {item['name']} {item['emoji']}**"