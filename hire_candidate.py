from tkinter import *
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

hire_candidate_frame = Tk()
hire_candidate_frame.geometry('500x500')
hire_candidate_frame.title("Hire Candidate")

connector=sqlite3.connect('UserRegistrationDetails.db')
with connector:
    cursor=connector.cursor()

applicants=StringVar()
location=StringVar()

label_form = Label(hire_candidate_frame, text="Hire Candidate", width=20, font=("bold", 20))
label_form.place(x=90, y=43)


class Hire_Candidate:
    applicant_temp = []
    cursor.execute("select FirstName from Applicant_Login where isShortlisted=1 and InterviewScore>3")
    applicant_temp = [item for t in cursor.fetchall() for item in t]
    if(len(applicant_temp)!=0):
        applicants.set(applicant_temp[0])
        applicant_options = OptionMenu(hire_candidate_frame, applicants, *applicant_temp)
        applicant_options.place(x=220, y=85)

        def generateJoiningLetter(self,email, doj,full_name,salary,profile,hr,location):
            field_validity = 1
            if(doj=='' or location==''):
                messagebox.showinfo('Error', 'All fields are required')
                field_validity = 0
            if(field_validity):
                cursor.execute('INSERT INTO New_Employee (Name,Email,DateofJoining,Salary,Role,Location,HR_assigned) VALUES(?,?,?,?,?,?,?)',(full_name, email, doj, salary, profile, location, hr))
                messagebox.showinfo('Success','Candidate Hired!!')
                connector.commit()
                hire_candidate_frame.destroy()


        def hireCandidate(*args):
            cursor.execute(
                "select FirstName, LastName, Email, VacancyApplied,HR_Assigned,VacancyApplied from Applicant_Login where FirstName='{}'".format(
                    applicants.get()))
            columns = [item for t in cursor.description for item in t]
            columns_final = list(filter(None, columns))
            values = [item for t in cursor.fetchall() for item in t]
            applicant_dict = dict(zip(columns_final, values))

            print(applicant_dict)

            label_name = Label(hire_candidate_frame, text="Name", width=20, font=("bold", 10))
            label_name.place(x=80, y=140)

            full_name=applicant_dict['FirstName'] + applicant_dict['LastName']

            name_text = Entry(hire_candidate_frame)
            name_text.insert('end', applicant_dict['FirstName'] + applicant_dict['LastName'])
            name_text.config(state=DISABLED)
            name_text.place(x=240, y=140)

            label_vacancy = Label(hire_candidate_frame, text="Vacancy applied", width=20, font=("bold", 10))
            label_vacancy.place(x=80, y=165)

            vacancy_text = Entry(hire_candidate_frame)
            vacancy_text.insert('end', applicant_dict['VacancyApplied'])
            vacancy_text.config(state=DISABLED)
            vacancy_text.place(x=240, y=165)

            label_hr = Label(hire_candidate_frame, text="HR", width=20, font=("bold", 10))
            label_hr.place(x=80, y=195)

            hr_text = Entry(hire_candidate_frame)
            hr_text.insert('end', applicant_dict['HR_Assigned'])
            hr_text.config(state=DISABLED)
            hr_text.place(x=240, y=195)

            cursor.execute("select salary from Vacancy_Details where JobTitle='{}'".format(applicant_dict['VacancyApplied']))
            salary=int(list(cursor.fetchall()[0])[0])

            label_salary = Label(hire_candidate_frame, text="Salary", width=20, font=("bold", 10))
            label_salary.place(x=80, y=220)

            salary_text = Entry(hire_candidate_frame)
            salary_text.insert('end', salary)
            salary_text.config(state=DISABLED)
            salary_text.place(x=240, y=220)

            label_doj = Label(hire_candidate_frame, text="Date of Joining", width=20, font=("bold", 10))
            label_doj.place(x=68, y=250)

            doj = DateEntry(hire_candidate_frame, width=12, background='darkblue', foreground='white',
                                       borderwidth=2)
            doj.pack(padx=10, pady=10)
            doj.place(x=240, y=250)

            label_location = Label(hire_candidate_frame, text="Location", width=20, font=("bold", 10))
            label_location.place(x=80, y=275)

            location_text = Entry(hire_candidate_frame, textvar=location)
            location_text.place(x=240, y=275)

            Button(hire_candidate_frame, text='Hire Candidate', width=20, bg='brown', fg='white',
                   command=lambda:obj.generateJoiningLetter(applicant_dict['Email'], doj.get(),full_name,salary,applicant_dict['VacancyApplied'],applicant_dict['HR_Assigned'],location.get())).place(x=160, y=320)

        applicants.trace('w', hireCandidate())

    else:
        label_none = Label(hire_candidate_frame, text="No Interviewed Candidates", width=20, font=("bold", 12))
        label_none.place(x=150, y=140)

obj=Hire_Candidate()
hire_candidate_frame.mainloop()