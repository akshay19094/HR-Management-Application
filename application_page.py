from tkinter import *
import sqlite3
from tkinter import messagebox

class Applicant:
        connector=sqlite3.connect('UserRegistrationDetails.db')
        with connector:
            cursor=connector.cursor()

        def CreateUserApplication(self,applicant_name,applicant_email,vacancy,competencies,work_experience,salary,requirements):
            name=applicant_name
            email=applicant_email
            job_vacancy = vacancy
            skills = competencies
            exp = work_experience
            sal = salary
            requirement = requirements

            fields_validity = 1
            if (vacancy is '' or skills is '' or exp is '' or sal is ''):
                messagebox.showinfo("Error", "All fields are required")
                fields_validity = 0

            if(fields_validity):
                cursor.execute("Update Applicant_Login set VacancyApplied='{}', Competencies='{}', WorkExperience='{}', Salary='{}',Tools_Research_Papers='{}' where email='{}'".format(job_vacancy,skills,exp,sal,requirement,email))
                messagebox.showinfo('Success','Application submitted')
                connector.commit()
                applicant_login_frame.destroy()

applicant_login_frame = Tk()
applicant_login_frame.geometry('500x500')
applicant_login_frame.title("Applicant Login")

applicant_name=StringVar()
applicant_email=StringVar()
vacancy=StringVar()
competencies=StringVar()
work_experience=StringVar()
salary=DoubleVar()
requirements=StringVar()

label_form = Label(applicant_login_frame, text="Welcome!", width=20, font=("bold", 20))
label_form.place(x=90, y=43)

label_name = Label(applicant_login_frame, text="First Name", width=20, font=("bold", 10))
label_name.place(x=80, y=86)

connector=sqlite3.connect('UserRegistrationDetails.db')
with connector:
    cursor=connector.cursor()
cursor.execute("select * from Active_Session")
columns = [item for t in cursor.description for item in t]
columns_final = list(filter(None, columns))
values = [item for t in cursor.fetchall() for item in t]
applicant_dict = dict(zip(columns_final, values))

name_text = Entry(applicant_login_frame,textvar=applicant_name)
name_text.insert('end',applicant_dict['Name'])
name_text.config(state=DISABLED)
name_text.place(x=240, y=86)

label_email = Label(applicant_login_frame, text="Email", width=20, font=("bold", 10))
label_email.place(x=68, y=126)

email_text = Entry(applicant_login_frame,textvar=applicant_email)
email_text.insert('end',applicant_dict['Email'])
email_text.config(state=DISABLED)
email_text.place(x=240, y=126)

cursor.execute('delete from Active_Session')
connector.commit()

label_vacancy = Label(applicant_login_frame, text="Job Vacancy", width=20, font=("bold", 10))
label_vacancy.place(x=80, y=165)

vacancy_temp = []

cursor.execute("select JobTitle from Vacancy_Details")
vacancy_temp=[item for t in cursor.fetchall() for item in t]
vacancy.set(vacancy_temp[0])
vacancy_options = OptionMenu(applicant_login_frame, vacancy, *vacancy_temp)
vacancy_options.place(x=240, y=165)

def change_requirement(*args):
    cursor.execute("select ProfileCode from Vacancy_Details where JobTitle='{}'".format(vacancy.get()))
    profile=str(list(cursor.fetchall()[0])[0])
    cursor.execute("select Field from Profile_Fields where ProfileCode='{}'".format(profile))
    field=str(list(cursor.fetchall()[0])[0])

    label_requirement = Label(applicant_login_frame, text="{}".format(field), width=20, font=("bold", 10))
    label_requirement.place(x=68, y=345)
    requirement_text = Entry(applicant_login_frame, textvar=requirements)
    requirement_text.place(x=240, y=345)

vacancy.trace('w', change_requirement)

label_competencies = Label(applicant_login_frame, text="Competencies", width=20, font=("bold", 10))
label_competencies.place(x=68, y=210)

competencies_text = Entry(applicant_login_frame, textvar=competencies)
competencies_text.place(x=240, y=210)

label_work_experience = Label(applicant_login_frame, text="Work Experience", width=20, font=("bold", 10))
label_work_experience.place(x=68, y=255)

experience_list=['1-3','3-5','5-10','Above 10']
work_experience.set(experience_list[0])
experience_options = OptionMenu(applicant_login_frame, work_experience, *experience_list)
experience_options.place(x=240, y=255)


label_salary = Label(applicant_login_frame, text="Expected Salary per annum", width=20, font=("bold", 10))
label_salary.place(x=68, y=300)

salary_text = Entry(applicant_login_frame, textvar=salary)
salary_text.delete(0, 'end')
salary_text.place(x=240, y=300)

applicant=Applicant()

Button(applicant_login_frame, text='Submit Application', width=20, bg='brown', fg='white',command=lambda:applicant.CreateUserApplication(applicant_name.get(),applicant_email.get(),vacancy.get(),competencies.get(),work_experience.get(),salary.get(),requirements.get())).place(x=180, y=390)


applicant_login_frame.mainloop()