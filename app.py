from flask import Flask, render_template, redirect
import pymysql
import datetime
import random

app = Flask(__name__)


class Database:
    def __init__(self):
        host = "35.224.130.29"
        user = "root"
        password = "scadmin"
        self.db = "sc_electronicsDB"
        self.con = pymysql.connect(host=host, user=user, password=password, db=self.db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def create_table(self, table_name, table_columns):
        sql_query = f"CREATE TABLE IF NOT EXISTS {table_name}"
        columns = ', '.join(table_columns)
        sql_query = f"{sql_query}({columns});"

        self.cur.execute(sql_query)

    def generate_entry(self, plant):

        time = str(datetime.datetime.now())
        status = "RUNNING" if random.uniform(0, 1) > 0.25 else "DOWN"
        sql_query = f"INSERT INTO {plant} (time, status) VALUES ('{time}', '{status}')"

        self.cur.execute(sql_query)
        self.con.commit()

    def list_entries(self):
        self.cur.execute("SELECT * FROM plant_1")
        result = self.cur.fetchall()

        return result

db = Database()
name = "plant_1"
db.create_table(name, ["entry INT NOT NULL AUTO_INCREMENT", "time VARCHAR(255)", "status VARCHAR(255)", "PRIMARY KEY (entry)"])

@app.route('/')
def entries():
    return render_template('entries.html', result=db.list_entries(), content_type='application/json')

@app.route('/acquire', methods=['GET', 'POST'])
def acquire():
    db.generate_entry(name)

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
