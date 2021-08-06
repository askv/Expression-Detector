import sqlite3
import ctypes                       #foreign function library,provides C compatible data types, and allows calling functions in DLLs or shared libraries.
                                    # It can be used to wrap these libraries in pure Python. (here for generating alert)

class databaseclass(object):

    def __init__(self):
        self.conn = sqlite3.connect("C:/Users/Deeksha/PycharmProjects/test2/data.db")
        self.cursor = self.conn.cursor()

    def update_db(self,pred,id):
        if ((pred == "Happy") or (pred == "Neutral")):
            self.cursor.execute(
                "Insert into stud_track (id,hcount,scount,flag,entry_date) select (?),0,0,0,date('now','localtime') where not exists (select 1 from stud_track where id = (?))",
                (id, id,))
            self.cursor.execute("SELECT cast(julianday('now') as int)-cast(julianday(entry_date) as int) FROM stud_track")
            diff = self.cursor.fetchone()
            if (diff[0] >= 15):
                self.cursor.execute(
                    "Update stud_track set hcount=0,scount=0,flag=0,entry_date=date('now','localtime') where id = (?)", (id,))

            self.cursor.execute("Update stud_track set hcount=hcount+1 where id = (?)", (id,))
            self.conn.commit()
            self.cursor.execute("Select flag from stud_track where id = (?)", (id,))
            flag = self.cursor.fetchone()
            if (flag[0] == 1):
                self.cursor.execute("Update stud_track set scount=(scount-2) where id=(?)", (id,))
                self.conn.commit()

            self.cursor.execute("Update stud_track set flag=0 where id=(?)", (id,))
            self.conn.commit()
            self.cursor.execute("Select hcount from stud_track where id = (?)", (id,))
            hcount = self.cursor.fetchone()
            self.cursor.execute("Select scount from stud_track where id = (?)", (id,))
            scount = self.cursor.fetchone()
            self.conn.commit()
            self.cursor.execute("Select exists(Select 1 from stud_help where id=(?))", (id,))
            e = self.cursor.fetchone()
            if ((scount[0] >= (3 * hcount[0])) and e[0] == 0):
                self.cursor.execute("Insert into stud_help values(?)", (id,))
                self.conn.commit()
                ctypes.windll.user32.MessageBoxW(0, id + " needs help", "Alert!", 1)



        else:
            self.cursor.execute(
                "Insert into stud_track (id,hcount,scount,flag,entry_date) select (?),0,0,1,date('now','localtime') where not exists (select 1 from stud_track where id = (?))",
                (id, id,))
            self.cursor.execute("SELECT cast(julianday('now') as int)-cast(julianday(entry_date) as int) FROM stud_track")
            diff = self.cursor.fetchone()
            if (diff[0] >= 15):
                self.cursor.execute(
                    "Update stud_track set hcount=0,scount=0,flag=1,entry_date=date('now','localtime') where id = (?)",
                    (id,))
            self.conn.commit()

            self.cursor.execute("Update stud_track set scount=scount+1 where id=(?)", (id,))
            self.conn.commit()
            self.cursor.execute("Select flag from stud_track where id=(?)", (id,))
            flag = self.cursor.fetchone()
            if (flag[0] == 0):
                self.cursor.execute("Update stud_track set hcount=(hcount-2) where id=(?)", (id,))
                self.conn.commit()

            self.cursor.execute("Update stud_track set flag=1 where id=(?)", (id,))
            self.conn.commit()
            self.cursor.execute("Select hcount from stud_track where id = (?)", (id,))
            hcount = self.cursor.fetchone()
            self.cursor.execute("Select scount from stud_track where id = (?)", (id,))
            scount = self.cursor.fetchone()
            self.conn.commit()
            self.cursor.execute("Select exists(Select 1 from stud_help where id=(?))", (id,))
            e = self.cursor.fetchone()
            if ((scount[0] >= (3 * hcount[0])) and e[0] == 0):
                self.cursor.execute("Insert into stud_help values(?)", (id,))
                self.conn.commit()
                ctypes.windll.user32.MessageBoxW(0, id + " needs help", "Alert!", 1)