from tkinter import *
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
#from create_job_vacancy import *
#vacancy_frame.destroy()
vacancy_update_frame = Tk()
vacancy_update_frame.geometry('500x500')
vacancy_update_frame.title("Update vacancy")

connector=sqlite3.connect('UserRegistrationDetails.db')
with connector:
    cursor=connector.cursor()

job_title=StringVar()
competencies=StringVar()
work_experience=StringVar()
salary=DoubleVar()
vacancy_expiry_date=StringVar()
vacancy_update=StringVar()

label_form = Label(vacancy_update_frame, text="Update Vacancy", width=20, font=("bold", 20))
label_form.place(x=90, y=33)

label_vacancy = Label(vacancy_update_frame, text="Job Vacancy", width=20, font=("bold", 10))
label_vacancy.place(x=80, y=86)

vacancy_temp = []
cursor.execute("select JobTitle from Vacancy_Details")
vacancy_temp=[item for t in cursor.fetchall() for item in t]
vacancy_update.set(vacancy_temp[0])
vacancy_options = OptionMenu(vacancy_update_frame, vacancy_update, *vacancy_temp)
vacancy_options.place(x=240, y=85)

class Update_Vacancy:

    def update_vacancy(self,profile,vacancy_expiry_date):
        skills = competencies.get()
        exp = work_experience.get()
        sal = salary.get()
        exp_date = vacancy_expiry_date

        fields_validity = 1
        if (skills is '' or exp is '' or sal is '' or exp_date is ''):
            messagebox.showinfo("Error", "All fields are required")
            fields_validity = 0

        temp=cursor.execute('Select Salary_Cap from Job_Profile where Profile_Name="{}"'.format(profile))
        salary_cap = int(list(temp.fetchall()[0])[0])

        if (salary_cap < sal and fields_validity == 1):
            messagebox.showinfo("Error", "Salary cap exceeded")
            fields_validity = 0

        if (fields_validity):
            print(profile)
            if profile=='Machine Learning':
                #obj=Machine_Learning()
                from create_job_vacancy import Machine_Learning
                Machine_Learning.update_vacancy(skills, exp, sal, exp_date, profile)

            if profile == 'Data Science':
                #obj = Data_Science()
                from create_job_vacancy import Data_Science
                Data_Science.update_vacancy(skills, exp, sal, exp_date, profile)

            #cursor.execute("Update Vacancy_Details set Competencies='{}', WorkExperience='{}', Salary='{}',Vacancy_Expiry_Date='{}' where JobProfile='{}'".format(skills, exp, sal, exp_date, profile))
            #connector.commit()
            #messagebox.showinfo("Success", "Vacancy Updated!")
            vacancy_update_frame.destroy()


def update_requirement(vacancy):
    print(vacancy)
    cursor.execute("select * from Vacancy_Details where JobTitle='{}'".format(vacancy))
    columns=[item for t in cursor.description for item in t]

    columns_final = list(filter(None, columns))
    values=[item for t in cursor.fetchall() for item in t]

    vacancy_dict=dict(zip(columns_final,values))

    print(vacancy_dict)

    label_competencies = Label(vacancy_update_frame, text="Competencies", width=20, font=("bold", 10))
    label_competencies.place(x=68, y=130)

    competencies_text = Entry(vacancy_update_frame, textvar=competencies)
    competencies_text.insert('end',vacancy_dict['Competencies'])
    competencies_text.place(x=240, y=130)

    label_work_experience = Label(vacancy_update_frame, text="Work Experience", width=20, font=("bold", 10))
    label_work_experience.place(x=68, y=175)

    experience_list = ['1-3', '3-5', '5-10', 'Above 10']
    work_experience.set(vacancy_dict['WorkExperience'])
    experience_options = OptionMenu(vacancy_update_frame, work_experience, *experience_list)
    experience_options.place(x=240, y=175)

    label_salary = Label(vacancy_update_frame, text="Salary per annum", width=20, font=("bold", 10))
    label_salary.place(x=68, y=220)

    salary_text = Entry(vacancy_update_frame, textvar=salary)
    salary_text.delete(0, 'end')
    salary_text.insert('end',vacancy_dict['Salary'])
    salary_text.place(x=240, y=220)

    label_vacancy_expiry_date = Label(vacancy_update_frame, text="Vacancy Expiry Date", width=20, font=("bold", 10))
    label_vacancy_expiry_date.place(x=68, y=265)

    vacancy_expiry_date = DateEntry(vacancy_update_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    vacancy_expiry_date.set_date(vacancy_dict['Vacancy_Expiry_Date'])
    vacancy_expiry_date.pack(padx=10, pady=10)
    vacancy_expiry_date.place(x=240, y=265)

    Button(vacancy_update_frame, text='Update Vacancy', width=20, bg='brown', fg='white',command=lambda:obj.update_vacancy(vacancy_dict['JobProfile'],vacancy_expiry_date.get())).place(x=180, y=310)


vacancy_update.trace('w', update_requirement(vacancy_update.get()))

obj=Update_Vacancy()
vacancy_update_frame.mainloop()