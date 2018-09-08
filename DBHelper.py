import sqlite3


class DBHelper:
    def __init__(self, dbname="transac.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS Transactions (TAId INT,chatID INT, payerid INT,amount FLOAT(2),description TEXT,bene TEXT)"
        self.conn.execute(stmt)
        #self.conn.execute(stmt)
        
        self.conn.commit()

    def add_item(self, chatID,payerid,amount,description,bene="(,)"):
        stmt = "INSERT INTO Transactions (chatID, payerid, amount,description, bene) VALUES (?,?,?,?,?)"
        args = (chatID,payerid,amount,description,bene)
        print(str(args))
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):#TODO FIX
        stmt = "DELETE FROM Transactions WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM Transactions"
        return [x for x in self.conn.execute(stmt)]

    def close(self):
        self.conn.close()

TA = DBHelper()
TA.conn.execute("DROP TABLE Transactions")
TA.setup()
TA.add_item(15,-1,12,"Beer")
TA.add_item(16,-2,12.35,"Bier")
TA.add_item(16,-3,12.2344,"Bear")
print(TA.get_items())
TA.close()
