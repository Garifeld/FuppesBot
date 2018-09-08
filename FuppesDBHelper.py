import sqlite3
import time
import datetime

class DBHelper:
    def __init__(self, dbname="events.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)#sqlite3.connect(dbname, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)#

    evId=0
    chatId =1
    description=2
    place=3
    datime= 4
    repitition=5
    minplayers=6
    maxplayers=7
    alrreminded =8
    reminder=9
    
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS Events (EvId INTEGER PRIMARY KEY AUTOINCREMENT,chatID INT,description TEXT, place TEXT, datime TIMESTAMP, Repitition TEXT, minPlayers INT, maxPlayers INT,alreadyreminded INT, Reminder TIMESTAMP)"
        self.conn.execute(stmt)
        #self.conn.execute(stmt)        
        self.conn.commit()

    def add_item(self,args):
        stmt = "INSERT INTO Events (chatID,description, place, datime, Repitition, minPlayers, maxPlayers, alreadyreminded, Reminder) VALUES (?"+(",?" * (len(args)-1)) +")"
        print(str(args))
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, EventID):#TODO FIX
        stmt = "DELETE FROM Events WHERE EvId = (?)"
        args = (EventID,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM Events"
        return [x for x in self.conn.execute(stmt)]

    def get_Past_Events(self):
        datestr =datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=1), "%Y-%m-%d %H:%M:%S")#For testing purposes; delete the +1 day in the final version
        stmt = "SELECT * FROM Events WHERE '%s'> datime"%datestr
        print(stmt)
        return [x for x in self.conn.execute(stmt)]

    def update_Past_Events(self):
        #time.sleep(1)
        L= self.get_Past_Events()
        print("Past Events:%s"%str(L))
        for Ev in L:
            if Ev[self.repitition]=="None":
                self.delete_item(Ev[EvId])
                return
            elif Ev[self.repitition]=="Weekly":
                nuEv =[i for i in Ev[1:]]
                print("datime: %s"%type(nuEv[self.datime-1]))
                nuEv[self.datime-1]+=datetime.timedelta(days=7)
                nuEv[self.reminder-1] =nuEv[self.datime-1]+(Ev[self.reminder]-Ev[self.datime])
                if nuEv[self.reminder-1]!=nuEv[self.datime-1]:
                    nuEv[self.alrreminded-1]=0
                self.add_item(nuEv)
                self.delete_item(Ev[self.evId])

                   
 
    #def get_Announced_Events(self):
    #    curtime =time.time()
    #    stmt = "SELECT * FROM Events WHERE datime <"+str(curtime)
    #    return [x for x in self.conn.execute(stmt)]

    
    def close(self):
        self.conn.close()

TA = DBHelper()
TA.conn.execute("DROP TABLE IF EXISTS Events")
TA.setup()
#chatID ,description, place, datime, Repitition, minPlayers, Reminder, alreadyReminded,maxplayers
TA.add_item((123,"Fussball","Admi",datetime.datetime.now(),"Weekly",8," 2 Days",0,datetime.datetime(2018, 7, 12, 7, 0,1,1)))
#TA.add_item(16,-2,12.35,"Bier")
#TA.add_item(16,-3,12.2344,"Bear")
print(TA.get_items())
TA.update_Past_Events()
print(TA.get_items())
TA.close()

#con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
#cur = con.cursor()
#cur.execute("create table test(d date, ts timestamp)")

#today = datetime.date.today()
#now = datetime.datetime.now()

#cur.execute("insert into test(d, ts) values (?, ?)", (today, now))
#cur.execute("select d, ts from test")
#row = cur.fetchone()
#print(today, "=>", row[0], type(row[0]))
#print(now, "=>", row[1], type(row[1]))

#cur.execute('select current_date as "d [date]", current_timestamp as "ts [timestamp]"')
#row = cur.fetchone()
#print("current_date", row[0], type(row[0]))
#print("current_timestamp", row[1], type(row[1]))
