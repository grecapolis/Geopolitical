from asyncio.windows_events import NULL
from http.client import MOVED_PERMANENTLY
import os
import sqlite3
import time

class Database_Handler():
    def __init__(self, database_name : str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row
        
    def register(self, discord_id : str):
        cursor = self.con.cursor()
        query = f"INSERT INTO Person (discord_id) VALUES ('" + discord_id + "') ;"
        print(query)
        cursor.execute(query)
        cursor.close()
        self.con.commit()
    
    def test_inscription(self, discord_id : str):
        cursor = self.con.cursor()
        query = f"SELECT discord_id FROM person WHERE discord_id = ?;"
        cursor.execute(query, (discord_id,))
        result = cursor.fetchall()
        cursor.close()
        
        return len(result) > 0
    
    def modification(self, parametre : str, new_value, discord_id):
        cursor = self.con.cursor()
        query = f"UPDATE Person SET "+ parametre +" = ? WHERE discord_id = ?;"
        cursor.execute(query, (new_value, discord_id))
        cursor.close()
        self.con.commit()

        cursor = self.con.cursor()
        actualTime = str(int(time.time()))
        query = f"UPDATE Person SET date_last_taxes = " + actualTime + " WHERE discord_id = '"+ discord_id +"' ;"
        cursor.execute(query)
        cursor.close()
        self.con.commit()
    
    def selectall(self, discord_id):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Person WHERE discord_id = '" +  str(discord_id) + "';"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        result = dict(result[0])
        print(result)
        return result
    
    def salary(self, ajout, discord_id):
        cursor = self.con.cursor()
        query = f"UPDATE Person SET argent = argent + {str(ajout)} WHERE discord_id = '{str(discord_id)}';"
        cursor.execute(query)
        ti = time.time()
        query2 = f"UPDATE Person SET date_last_taxes = {ti} WHERE discord_id = '{str(discord_id)}';"
        cursor.execute(query2)
        cursor.close()
        self.con.commit()
    
    def newhab(self, ajout, discord_id):
        cursor = self.con.cursor()
        query = f"UPDATE Person SET population = population + {str(ajout)} WHERE discord_id = (?);"
        cursor.execute(query, (str(discord_id),))
        cursor.close()
        self.con.commit()
    
    def setname(self, newname, discord_id):
        cursor = self.con.cursor()
        query = f"UPDATE Person SET nom = (?) WHERE discord_id = (?);"
        cursor.execute(query, (newname, discord_id,))
        cursor.close()
        self.con.commit()
    
    def listpays(self):
        cursor = self.con.cursor()
        query = "SELECT nom FROM Person ;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        resultfinal = []

        for i in range(len(result)):
            print(result[i]['nom'])
            resultfinal = resultfinal + [result[i]['nom']]

        return resultfinal