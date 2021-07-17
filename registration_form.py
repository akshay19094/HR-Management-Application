from tkinter import *
import sqlite3
from tkinter import messagebox
import re

registration_frame = Tk()
registration_frame.geometry('1000x600')
registration_frame.title("Registration Form")


######################################
class Applicant:
  def __init__(self,First_Name=None,Last_Name=None,password=None,Email_ID=None,Phone_Number=None,Requirement_Number=None,Job_Experience=None,Competencies=None,Expected_Salary=None,tools_papers=None):

    self.__First_Name=First_Name
    self.__Last_Name = Last_Name
    self.__Password=password

    self.__Email_ID=Email_ID
    self.__Phone_Number=Phone_Number
    self.__Requirement_Number=Requirement_Number
    self.__Job_Experience=Job_Experience
    self.__Competencies=Competencies
    self.__Expected_Salary=Expected_Salary
    self.__tools_papers=tools_papers

  def create_application(self):
    #code to create application to save entry in database
    connector=sqlite3.connect('UserRegistrationDetails.db')
    with connector:
        cursor=connector.cursor()

    cursor.execute('INSERT INTO Applicant_Login (FirstName,LastName,Email,Password) VALUES(?,?,?,?)',
                   (self.__First_Name,self.__Last_Name,self.__Email_ID,self.__Password))
    connector.commit()
    messagebox.showinfo("Success", "Registration Successful!")
    #registration_frame.destroy()

  def update_application(self,Applicant_Name,Phone_Number,Requirement_Number,Job_Experience,Competencies,Expected_Salary,tools_papers):
    #code to create application to save entry in database
    pass


######################################

class Auth:



    #@classmethod
    def UserRegistrationDetailsDB(self,f,l,m,p,c):
        self.__first = f
        self.__last = l
        self.__mail = m
        self.__passw = p
        self.__confirm_passw = c
        connector=sqlite3.connect('UserRegistrationDetails.db')
        with connector:
            cursor=connector.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Applicant_Login (ID INTEGER PRIMARY KEY AUTOINCREMENT,FirstName TEXT,LastName TEXT,Email TEXT,Password TEXT)')


        fields_validity=1
        if((self.__first is '') or (self.__last is '') or (self.__mail is '') or (self.__passw is '') or (self.__confirm_passw is '')):
            print(self.__first,self.__last,self.__mail,self.__passw ,self.__confirm_passw)
            messagebox.showinfo("Error","All fields are required")
            fields_validity=0
        email_regex='^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

        if(re.search(email_regex,self.__mail)):
            cursor.execute('Select count(*) from Applicant_Login where Email="{}"'.format(self.__mail))
            match=cursor.fetchall()
            if(int(list(match[0])[0])>0 and fields_validity==1):
                messagebox.showinfo("Error","User entry already exists")
                fields_validity=0
        else:
            if(fields_validity==1):
                messagebox.showinfo("Error","Invalid email ID")
            fields_validity=0

        if(self.__passw!=self.__confirm_passw):
            messagebox.showinfo("Error","Passwords don't match. Please recheck.")
            fields_validity=0

    #print("{},{},{}".format(first, last, mail))
        if(fields_validity):
            obj=Applicant(First_Name=self.__first,Last_Name=self.__last,Email_ID=self.__mail,password=self.__passw)
            obj.create_application()

    #@classmethod
    def ValidateLogin(self,l,p,u):
        connector=sqlite3.connect('UserRegistrationDetails.db')
        with connector:
            cursor=connector.cursor()

        mail = l
        passw = p
        type = u

        flag=1

        if (type == ''):
            messagebox.showinfo("Error", "Select atleast one user type")
            flag = 0

        else:
            if(mail is '' or passw is ''):
                messagebox.showinfo("Error","Please enter you login credentials")
                flag=0

            temp=cursor.execute('Select count(*) from {}_Login where Email="{}"'.format(usertype.get(),mail))

            if int(list(temp.fetchall()[0])[0])==0:
                if(flag==1):
                    messagebox.showinfo("Error","No such user exists")
                flag=0
            else:
                passw_db=cursor.execute("Select Password from {}_Login where Email='{}'".format(usertype.get(),mail))
                passw_tmp=str(list(passw_db.fetchall()[0])[0])

                if flag==1:
                    if(passw_tmp==passw):
                        messagebox.showinfo("Success","Login Successful")
                        if(usertype.get()=='Applicant'):
                            temp=cursor.execute("select FirstName from Applicant_Login where email='{}'".format(mail))
                            name=str(list(temp.fetchall()[0])[0])
                            cursor.execute("insert into Active_Session (Name,Email) values(?,?)",(name,mail))
                            connector.commit()
                            registration_frame.destroy()
                            from applicant_landing_page import applicant_landing_frame
                            applicant_landing_frame.mainloop()
                        else:
                            temp = cursor.execute("select Name from HR_Login where email='{}'".format(mail))
                            name = str(list(temp.fetchall()[0])[0])
                            cursor.execute("insert into Active_Session (Name,Email) values(?,?)", (name, mail))
                            connector.commit()
                            registration_frame.destroy()
                            from hr_landing_page import hr_login_frame
                            hr_login_frame.mainloop()

                    else:
                        messagebox.showinfo("Error","Wrong password")
                        flag=0


first_name = StringVar()
last_name = StringVar()
email = StringVar()
password = StringVar()
confirm_password = StringVar()


label_form_header = Label(registration_frame, text="Welcome to Application Portal!", width=30, font=("bold", 20))
label_form_header.place(x=250, y=33)

label_form = Label(registration_frame, text="New User Registration", width=20, font=("bold", 20))
label_form.place(x=90, y=103)

label_first_name = Label(registration_frame, text="Legal First Name", width=20, font=("bold", 10))
label_first_name.place(x=80, y=180)

first_name_text = Entry(registration_frame, textvar=first_name)
first_name_text.place(x=240, y=180)

label_last_name = Label(registration_frame, text="Legal Last Name", width=20, font=("bold", 10))
label_last_name.place(x=80, y=225)

last_name_text = Entry(registration_frame, textvar=last_name)
last_name_text.place(x=240, y=225)

label_email = Label(registration_frame, text="Email", width=20, font=("bold", 10))
label_email.place(x=68, y=270)

email_text = Entry(registration_frame, textvar=email)
email_text.place(x=240, y=270)

label_password = Label(registration_frame, text="Password", width=20, font=("bold", 10))
label_password.place(x=68, y=315)

password_text = Entry(registration_frame, textvar=password, show="*")
password_text.place(x=240, y=315)

label_confirm_password = Label(registration_frame, text="Retype Password", width=20, font=("bold", 10))
label_confirm_password.place(x=68, y=360)

confirm_password_text = Entry(registration_frame, textvar=confirm_password, show="*")
confirm_password_text.place(x=240, y=360)

label_form = Label(registration_frame, text="Login", width=20, font=("bold", 20))
label_form.place(x=500, y=103)


login_email = StringVar()
login_password = StringVar()
usertype = StringVar()

label_email = Label(registration_frame, text="Email", width=20, font=("bold", 10))
label_email.place(x=500, y=180)
login_email_text = Entry(registration_frame, textvar=login_email)

login_email_text.place(x=650, y=180)

label_password = Label(registration_frame, text="Password", width=20, font=("bold", 10))
label_password.place(x=500, y=225)

login_password_text = Entry(registration_frame, textvar=login_password, show="*")
login_password_text.place(x=650, y=225)

R1 = Radiobutton(registration_frame, text="Applicant", variable=usertype, value='Applicant')
R1.place(x=650,y=275)

R2 = Radiobutton(registration_frame, text="HR", variable=usertype, value='HR')
R2.place(x=750,y=275)


A=Auth()
Button(registration_frame, text='Register', width=20, bg='brown', fg='white', command=lambda:A.UserRegistrationDetailsDB(first_name.get(),last_name.get(),email.get(),password.get(),confirm_password.get())).place(x=180, y=430)

Button(registration_frame, text='Login', width=20, bg='brown', fg='white', command=lambda:A.ValidateLogin(login_email.get(),login_password.get(),usertype.get())).place(x=580, y=320)

registration_frame.mainloop()

