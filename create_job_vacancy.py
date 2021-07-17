from tkinter import *
from tkcalendar import Calendar, DateEntry
import sqlite3
from tkinter import messagebox

vacancy_frame=Tk()
vacancy_frame.geometry('500x500')
vacancy_frame.title('Create Job Vacancy')
##############################################
class Job_Profile:
    def __init__(self, ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date):
        self.ProfileCode = ProfileCode
        self.__JobTitle = JobTitle
        self.__Competencies = Competencies
        self.__WorkExperience = WorkExperience
        self.__Salary= Salary
        self.__Vacancy_Expiry_Date=Vacancy_Expiry_Date
        self.__JobProfile = JobProfile
    def create_vacancy(self):
        pass

    def update_vacancy(self):
        pass

    def delete_vacancy(self):
        pass


class Machine_Learning(Job_Profile):
    def __init__(self, ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date):
        Job_Profile.__init__(self, ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date)
        self.ProfileCode = ProfileCode
        self.__JobTitle = JobTitle
        self.__JobProfile=JobProfile
        self.__Competencies = Competencies
        self.__WorkExperience = WorkExperience
        self.__Salary = Salary
        self.__Vacancy_Expiry_Date = Vacancy_Expiry_Date

    def create_vacancy(self):
        connector = sqlite3.connect('UserRegistrationDetails.db')
        with connector:
            cursor = connector.cursor()

        cursor.execute('INSERT INTO Vacancy_Details (ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date) VALUES(?,?,?,?,?,?,?)',
            (self.ProfileCode , self.__JobTitle,self.__JobProfile,self.__Competencies,self.__WorkExperience,self.__Salary , self.__Vacancy_Expiry_Date))
        connector.commit()
        messagebox.showinfo("Success", "Vacancy Created!")
        vacancy_frame.destroy()

    # Write here the code to creat1e vacancy in database
    @classmethod
    def update_vacancy(self,skills, exp,sal,exp_date,profile):
        cursor.execute(
            "Update Vacancy_Details set Competencies='{}', WorkExperience='{}', Salary='{}',Vacancy_Expiry_Date='{}' where JobProfile='{}'".format(
                skills, exp, sal, exp_date, profile))
        connector.commit()
        messagebox.showinfo("Success", "Vacancy Updated!")

    # write here the code to update vacancy in database

    def delete_vacancy(self, requirement_number):
        pass


# write here the code to delete vacancy in database using requirement_number


class Data_Science(Job_Profile):
    def __init__(self,ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date):
        Job_Profile.__init__(self, ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date)
        self.ProfileCode = ProfileCode
        self.__JobTitle = JobTitle
        self.__JobProfile = JobProfile
        self.__Competencies = Competencies
        self.__WorkExperience = WorkExperience
        self.__Salary = Salary
        self.__Vacancy_Expiry_Date = Vacancy_Expiry_Date


    def create_vacancy(self):
        connector = sqlite3.connect('UserRegistrationDetails.db')
        with connector:
            cursor = connector.cursor()

        cursor.execute(
            'INSERT INTO Vacancy_Details (ProfileCode,JobTitle,JobProfile,Competencies,WorkExperience,Salary,Vacancy_Expiry_Date) VALUES(?,?,?,?,?,?,?)',
            (self.ProfileCode, self.__JobTitle, self.__JobProfile, self.__Competencies, self.__WorkExperience,
             self.__Salary, self.__Vacancy_Expiry_Date))
        connector.commit()
        messagebox.showinfo("Success", "Vacancy Created!")
        vacancy_frame.destroy()

    # Write here the code to create vacancy in database
    # you can add int type field in database to distinguish all sub classes
    @classmethod
    def update_vacancy(self,skills, exp,sal,exp_date,profile):
        cursor.execute(
            "Update Vacancy_Details set Competencies='{}', WorkExperience='{}', Salary='{}',Vacancy_Expiry_Date='{}' where JobProfile='{}'".format(
                skills, exp, sal, exp_date, profile))
        connector.commit()
        messagebox.showinfo("Success", "Vacancy Updated!")

    # write here the code to update vacancy in database

    def delete_vacancy(self, requirement_number):
        pass


# write here the code to delete vacancy in database using requirement_number


##############################################

class VACANCY:
    def Create_Vacancy(self,a,b,c,d,e,f):
        connector = sqlite3.connect('UserRegistrationDetails.db')
        with connector:
            cursor = connector.cursor()

        title = a
        profile = b
        skills = c
        exp = d
        sal = e
        exp_date = f


        code="".join([word[0] for word in profile.split()])

        cursor.execute('CREATE TABLE IF NOT EXISTS Vacancy_Details (ID INTEGER PRIMARY KEY AUTOINCREMENT,ProfileCode TEXT,JobTitle TEXT,JobProfile TEXT,Competencies TEXT,WorkExperience TEXT,Salary INT,Vacancy_Expiry_Date TEXT)')

        fields_validity = 1
        if(title is '' or profile is '' or skills is '' or exp is '' or sal is '' or exp_date is ''):
            messagebox.showinfo("Error", "All fields are required")
            fields_validity = 0

        cursor.execute('Select Salary_Cap from Job_Profile where Profile_Name="{}"'.format(profile))
        salary_cap=int(list(cursor.fetchall()[0])[0])

        if (salary_cap < sal and fields_validity==1):
            messagebox.showinfo("Error", "Salary cap exceeded")
            fields_validity = 0

        if(fields_validity):
            print(b)
            if b == 'Data Science':
                DS=Data_Science(code,title,profile,skills,exp,sal,exp_date)
                DS.create_vacancy()

            if b == 'Machine Learning':
                ML = Machine_Learning(code,title,profile,skills,exp,sal,exp_date )
                ML.create_vacancy()


job_title=StringVar()
job_profile=StringVar()
competencies=StringVar()
work_experience=StringVar()
salary=DoubleVar()
vacancy_expiry_date=StringVar()


label_form = Label(vacancy_frame, text="Create New Vacancy", width=20, font=("bold", 20))
label_form.place(x=90, y=43)

label_job_title = Label(vacancy_frame, text="Job Title", width=20, font=("bold", 10))
label_job_title.place(x=80, y=120)

job_title_text = Entry(vacancy_frame, textvar=job_title)
job_title_text.place(x=240, y=120)

label_job_profile = Label(vacancy_frame, text="Job Profile", width=20, font=("bold", 10))
label_job_profile.place(x=80, y=165)

profile_temp = []
connector = sqlite3.connect('UserRegistrationDetails.db')
with connector:
    cursor = connector.cursor()
cursor.execute("select profile_name from Job_Profile")
profile_temp=[item for t in cursor.fetchall() for item in t]
job_profile.set(profile_temp[0])


job_profile_options = OptionMenu(vacancy_frame, job_profile, *profile_temp)
job_profile_options.place(x=240, y=165)

label_competencies = Label(vacancy_frame, text="Competencies", width=20, font=("bold", 10))
label_competencies.place(x=68, y=210)

competencies_text = Entry(vacancy_frame, textvar=competencies)
competencies_text.place(x=240, y=210)

label_work_experience = Label(vacancy_frame, text="Work Experience", width=20, font=("bold", 10))
label_work_experience.place(x=68, y=255)

experience_list=['1-3','3-5','5-10','Above 10']
work_experience.set(experience_list[0])
experience_options = OptionMenu(vacancy_frame, work_experience, *experience_list)
experience_options.place(x=240, y=255)

label_salary = Label(vacancy_frame, text="Salary per annum", width=20, font=("bold", 10))
label_salary.place(x=68, y=300)

salary_text = Entry(vacancy_frame, textvar=salary)
salary_text.place(x=240, y=300)

label_vacancy_expiry_date = Label(vacancy_frame, text="Vacancy Expiry Date", width=20, font=("bold", 10))
label_vacancy_expiry_date.place(x=68, y=345)

vacancy_expiry_date = DateEntry(vacancy_frame, width=12, background='darkblue',foreground='white', borderwidth=2)
vacancy_expiry_date.pack(padx=10, pady=10)
vacancy_expiry_date.place(x=240, y=345)

obj=VACANCY()

Button(vacancy_frame, text='Submit', width=20, bg='brown', fg='white',command=lambda:obj.Create_Vacancy(job_title.get(),job_profile.get(),competencies.get(),work_experience.get(),salary.get(),vacancy_expiry_date.get())).place(x=180, y=390)

vacancy_frame.mainloop()