from ast import Str
import sqlite3 
import time


tm = time.strftime('%Y-%m-%d %H:%M')
print(tm)
conn = sqlite3.connect('gym_data.db')

c = conn.cursor()


class Admin:
    def __init__(self):
        self.member=dict([])
        self.regimen=dict([])

    def Add_member(self,name,age,gender,mobile_no,email,G,membership_duration,paid,password):
        self.member[mobile_no]={}    
        self.member[mobile_no]["name"]=name
        self.member[mobile_no]["age"]=age
        self.member[mobile_no]["gender"]=gender
        self.member[mobile_no]["mobile_no"]=mobile_no
        self.member[mobile_no]["email"]=email
        
        if G == 1:
            goal = "Build muscles"
            self.member[mobile_no]["goal"] = goal
        elif G == 2:
            goal = "Build strength"
            self.member[mobile_no]["goal"] = goal
        elif G == 3:
            goal = "Lose fat"
            self.member[mobile_no]["goal"] = goal
        elif G == 4:
            goal = "Improve cardio"
            self.member[mobile_no]["goal"] = goal
        
        self.member[mobile_no]["membership_duration"]=int(membership_duration)
        self.member[mobile_no]["paid"]=float(paid)
        self.member[mobile_no]["password"]=str(password)
        c.execute("INSERT INTO members VALUES (?,?,?,?,?,?,?,?,?,?)", ( mobile_no, name, age, gender, email, goal, tm, membership_duration, paid, password))
        
        if G == 1:
            c.execute("INSERT INTO Workout_plan VALUES (?,'CHEST','BICEPS','REST','Back','LEGS','TRICEPS','REST')", ( mobile_no,))
        elif G == 2:
            c.execute("INSERT INTO Workout_plan VALUES (?,'LEGS','PUSH','REST','PULL','REST','ARMS','REST')", ( mobile_no, ))
        elif G == 3:
            c.execute("INSERT INTO Workout_plan VALUES (?,'CARDIO','FULL BODY','REST','CARDIO','REST','CARDIO','REST')", ( mobile_no, ))
        elif G == 4:
            c.execute("INSERT INTO Workout_plan VALUES (?,'CARDIO','REST','CARDIO','REST','CARDIO','REST','CARDIO')", ( mobile_no, ))
        
        conn.commit()
        

    def view_member(self):
        c.execute("SELECT * FROM members")
        RESULT = c.fetchall()
        
        n = 1
        for row in RESULT:
                print("\n   Member {}:".format(n))
                print("Mobile number : {0}      Name : {1}      Age : {2}".format(row[0], row[1], row[2]))
                print("Gender : {0}               Email : {1}   Goal : {2}".format(row[3], row[4], row[5]))
                print("Date : {0}      Membership_duration : {1} months     Amount paid : {2} Yuan".format(row[6], row[7], row[8],"\n\n"))
                n = n+1
        
    def search_member(self,mobile_no):
        c.execute("SELECT * FROM members WHERE Mobile_number LIKE {} ".format(mobile_no))
        RESULT = c.fetchall()

        for r in RESULT:
            print("\n   Result for Mobile number {0}:".format(r[0]))
            print("Name : {0}                   Age : {1}".format(r[1], r[2]))
            print("Gender : {0}               Email : {1}   Goal : {2}".format(r[3], r[4], r[5]))
            print("Date of registration : {0}    Membership_duration : {1} months      Amount paid : {2} Yuan".format(r[6], r[7], r[8], "\n"))

    def delete_member(self,mobile_no):
        c.execute("""DELETE FROM members WHERE Mobile_number LIKE {} """.format(mobile_no))
        c.execute("""DELETE FROM Workout_plan WHERE Phone LIKE {} """.format(mobile_no))
        conn.commit()
        print("Member deleted !")
        
    
    def update_membership(self,paid, mobile_no,membership_duration):
        c.execute("""UPDATE members SET Membership_Duration = ? WHERE Mobile_number LIKE ? """, (membership_duration , mobile_no))
        c.execute("""UPDATE members SET Paid_bill = ? WHERE Mobile_number LIKE ? """, (paid , mobile_no))
        
        conn.commit()

        print("Membership Updated !")

    def check_Admin_password(self,password, Name):
        c.execute("SELECT Password FROM Admins WHERE Name = ?", (Name,))
        RES = c.fetchall()
        for row in RES:
            if row[0] == password:
                return True
            else:
                return False
    
    def Creat_New_Admin(self,password, Name):
        c.execute("INSERT INTO Admins VALUES (?,?)", ( Name, password))
        conn.commit()

        print('Admin Added Successfully !!')
      

def check_phone(ph_numb):
    c.execute("SELECT Mobile_number FROM members WHERE Mobile_number = ?", (ph_numb,))
    RESULT = c.fetchall()
    for row in RESULT:
        if row[0] == ph_numb:
            return True
        else:
            return False 


def check_password(password, num_p):
        c.execute("SELECT Password FROM members WHERE Mobile_number = ?", (num_p,))
        RES = c.fetchall()
        for row in RES:
            if row[0] == password:
                return True
            else:
                return False

def view_user_regimen(num_r):
        c.execute("SELECT * FROM Workout_plan WHERE Phone = ?", (num_r,))
        RES = c.fetchall()
        

        for row in RES:
            print("\n   This is your Workout plan for the week:\n")
            print("Monday = {0}      Tuesday = {1}      Wednesday = {2}    Thursday = {3}".format( row[1], row[2], row[3], row[4]))
            print("Friday= {1}                 Saturday = {2}               Sunday = {0}".format(row[5], row[6], row[7]), "\n")
            
    
def view_user_profile(num_p):
        c.execute("SELECT * FROM members WHERE Mobile_number = ?", (num_p,))
        RESULT = c.fetchall()
        

        for row in RESULT:
            print("\n   These are your personal information:\n")
            print("Mobile number = {0}      Name = {1}      Age = {2}".format(row[0], row[1], row[2]))
            print("Gender = {0}               Email = {1}   Goal = {2}".format(row[3], row[4], row[5]))
            print("Date = {0}                Membership_duration : {1} months      Amount paid : {2} Yuan".format(row[6], row[7], row[8], "\n\n"))

def update_password(mobile_no,password):
        c.execute("""UPDATE members SET Password = ? WHERE Mobile_number LIKE ? """, (password , mobile_no))
        conn.commit()

        print('Password Updated!')

    



S=Admin()
opt=True
while (opt==True):
    print("\n -------------------Welcome To the gym management system ! ------------------- \n")
    print("Press 1 if you are an  Admin")
    print("Press 2 if you are a Member")
    val=int(input())
    ###if val != 1 or val != 2:
        ###print("please enter 1 for admin or 2 for user")
    if val==1:
        name=str(input("Please enter you name:"))    
        psswd=input("enter your password :")
        val = S.check_Admin_password(psswd, name)
        if val == True:

            sup=True
            print("Welcome Admin !")
            while(sup==True):
                print()
                print("Admin Menu:\n 1.Create member\n 2.View all members\n 3.Delete member\n 4.Update membership\n 5.Search for a member\n 6.Create new admin \n 7.Logout")
                
                num=int(input())
                if num==1:
                    mobile_no=int(input("Enter mobile number:"))
                    name=input("Enter Full Name:")
                    age=str(input("Enter age:"))
                    gender=input("Gender(M/F):")
                    email=input("Enter your Email ID:")
                    goal=float(input("Enter your Goal(1.Gain Muscules 2.Gain strength 3.Lose fat 4.Improve endurance ):"))
                    membership_duration=int(input("Enter the duration(1/3/6/12):"))
                    bill = float(input("Enter how much the member paid: "))
                    password = str(input("Enter a password: "))
                    if membership_duration in [1,3,6,12]:
                        S.Add_member(name,age,gender,mobile_no,email,goal,membership_duration,bill,password)
                        ##S.create_regimen(VAR)
                    else:
                        print("membership duration can only be 1,3,6 & 12-->Try again")
                
                elif num==2:
                    print(S.view_member())

                elif num==3:
                    mob=int(input("Please enter the mobile number of user to be deleted:"))
                    S.delete_member(mob)
                
                elif num==4:
                    mob=int(input("Please enter the mobile number of user to be updated:"))
                    
                    check = check_phone (mob)

                    if check == True:
                        memb_duration=int(input("Please enter the duration upto which you want to extend:"))
                        Sal = float(input("Please enter how much the member paid:"))
                        S.update_membership(Sal, mob, memb_duration)
                    
                    else:
                        print('Phone number is not found !')
                    
                elif num==5:
                    numb=int(input("Please enter the phone number of the member you are searching:"))
                    S.search_member(numb)

                elif num==6:
                    name = str(input('Please enter new admin name:'))
                    pswd = str(input('Please enter new admin password:'))
                    S.Creat_New_Admin(pswd, name)
               

                elif num==7:
                    break

                else:
                    print("Invalid input")
                print("\n Want to go back to the admin MENU ? (Y/N)")
                sup=input().upper()=="Y"
        else: #if val == False:
            print('Your login information are not correct !!')        
            
    elif val==2:
        
        try:
            phone=int(input("Please enter you mobile number:"))
            
            check = check_phone (phone)

            if check == True:

                passwd=input("enter password :")
                F = check_password(passwd, phone)
                
                if F == True:
                    # print("Congratulations You are logged in as User")
                    user1=True
                    while(user1==True):
                        print("\nMember Menu:\n 1.View my workout plan \n 2.View my profile \n 3.Change password \n 4.Log out")
                        val=int(input())
                        if val==1:
                            try:
                                view_user_regimen(phone)
                            except:
                                print("You do not have any workout plan currently")
                        elif val==2:
                            try:
                                print(view_user_profile(phone))
                            except:
                                print("The profile does not exist")
                        elif val==3:
                            psw = str(input("enter the new password:"))
                            update_password(phone,psw)
                           
                        elif val==4:
                            break
                else:
                    print("Invalid password")

            else:
                print("Invalid number")
            
                
        except:
                print("either user not registered or invalid entry")
                print("Want to go back to the member MENU ? (Y/N)")
                user1=input().upper()=="Y"
