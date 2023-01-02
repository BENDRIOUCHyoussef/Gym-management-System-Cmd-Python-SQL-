import sqlite3 

conn = sqlite3.connect('gym_data.db')

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS members")
c.execute("DROP TABLE IF EXISTS Workout_plan")
c.execute("DROP TABLE IF EXISTS Admins")

table_1 = """CREATE TABLE IF NOT EXISTS members (
            Mobile_number int primary key,
            Name text,
            Age text,
            gender text,          
            Email text,
            Goal text,
            Date_Time DATETIME,
            Membership_Duration integer,
            Paid_bill Float,
            Password text
            );"""

table_2 = """CREATE TABLE IF NOT EXISTS Workout_plan (
            Phone int PRIMARY KEY,
            Monday text,
            Tuesday text,          
            Wednesday text,
            Thursday text,
            Friday text,
            saturday text,
            Sunday text,
            FOREIGN KEY (Phone) REFERENCES members(Mobile_number)
            );"""


table_3 = """CREATE TABLE IF NOT EXISTS Admins (Name text, Password text);"""

# Query = "INSERT INTO Admins VALUES (?,?)", ("Youssef", "1263")

c.execute(table_1)
c.execute(table_2)
c.execute(table_3)
c.execute("INSERT INTO Admins VALUES (?,?)", ("Youssef", "1263"))

conn.commit()

print("Database Created !")

##conn.close()