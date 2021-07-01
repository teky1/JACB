import sqlite3

"""
import sqlite3
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE prefixes (GuildID varchar(24) UNIQUE, Prefix varchar(16))")
connection.commit()
"""

DEFAULT_PREFIX = ";"

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def guildRecordExists(guild_id: int):
    guild_id_str = str(guild_id)
    cursor.execute("SELECT GuildID, Prefix FROM prefixes WHERE GuildID=?", (guild_id_str,))
    return not not cursor.fetchone()

def setPrefixGuild(guild_id: int, prefix: str):
    guild_id_str = str(guild_id)

    if guildRecordExists(guild_id):
        cursor.execute("UPDATE prefixes SET Prefix=? WHERE GuildID=?", (prefix, guild_id_str))
    else:
        cursor.execute("INSERT INTO prefixes (GuildID, Prefix) VALUES(?, ?)", (guild_id_str, prefix))
    connection.commit()

def getGuildPrefixFromID(guild_id: int):
    guild_id_str = str(guild_id)
    cursor.execute("SELECT Prefix FROM prefixes WHERE GuildID=?", (guild_id_str,))
    selection = cursor.fetchone()
    if selection:
        return selection[0]
    else:
        return DEFAULT_PREFIX

def get_prefix(client, message):
    if message.guild:
        return getGuildPrefixFromID(message.guild.id)
    else:
        return DEFAULT_PREFIX