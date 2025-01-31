import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DbManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASSWORD"), 
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.connection.cursor()
    

    def savdo_select(self, selected_date, user_id):
        self.cursor.execute("SELECT * FROM savdolar WHERE sana = %s AND chat_id = %s", (selected_date, user_id))
        existing_savdo = self.cursor.fetchall()
        return existing_savdo
    
    def harajat_update(self, harajat_name, harajat_summa, selected_date, user_id):
        # self.cursor.execute("SELECT * FROM harajatlar WHERE sana = %s AND nom = %s AND chat_id = %s", (selected_date, harajat_name, user_id))
        # existing_harajat = self.cursor.fetchall()

        # # if existing_harajat:
        # #     self.cursor.execute("UPDATE harajatlar SET summa = %s WHERE sana = %s AND nom = %s AND chat_id = %s", (harajat_summa, selected_date, harajat_name, user_id))
        # #     self.connection.commit()
            
        # # else:
        self.cursor.execute("INSERT INTO harajatlar (sana, nom, summa, chat_id) VALUES (%s, %s, %s, %s)", (selected_date, harajat_name, harajat_summa, user_id))
        self.connection.commit()

    def harajat_by_sana(self,selected_date, user_id):
        self.cursor.execute("SELECT * FROM harajatlar WHERE sana = %s AND chat_id = %s", (selected_date, user_id))  
        harajat_rows = self.cursor.fetchall()
        return harajat_rows
    
    def harajat_sanasi(self):
        sql = """select sana, sum(summa)
                from harajatlar
                group by sana
                order by sana desc
                limit 5"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    

