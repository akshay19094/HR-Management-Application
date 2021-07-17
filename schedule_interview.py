from datetime import datetime
from tkinter import *
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

schedule_interview_frame = Tk()
schedule_interview_frame.geometry('500x500')
schedule_interview_frame.title("Schedule Interview")

connector=sqlite3.connect('UserRegistrationDetails.db')
with connector:
    cursor=connector.cursor()

applicants=StringVar()
assigned_hr=StringVar()
interview_date=StringVar()
time_picker=StringVar()

label_form = Label(schedule_interview_frame, text="Schedule Interview", width=20, font=("bold", 20))
label_form.place(x=90, y=43)

applicant_temp = []
cursor.execute("select FirstName from Applicant_Login where isShortlisted=1")
applicant_temp=[item for t in cursor.fetchall() for item in t]

class Schedule_Interview:

    if(len(applicant_temp)!=0):
        applicants.set(applicant_temp[0])
        applicant_options = OptionMenu(schedule_interview_frame, applicants, *applicant_temp)
        applicant_options.place(x=220, y=85)

        def scheduleInterview(self,email,datepicker):
            hr=assigned_hr.get()
            interview_d=datepicker
            interview_time=time_picker.get()

            field_validity = 1
            if(hr=='' or interview_d=='' or interview_time==''):
                messagebox.showinfo('Error','All fields are required')
                field_validity=0


            if(field_validity):
                cursor.execute("update Applicant_login set HR_Assigned='{}',InterviewDate='{}',InterviewTime='{}' where Email='{}'".format(hr,interview_d,interview_time,email))
                connector.commit()
                messagebox.showinfo("Success","Interview scheduled!")
                schedule_interview_frame.destroy()

        def populate_user_details(*args):
            cursor.execute("select FirstName, LastName, Email, VacancyApplied,Competencies,WorkExperience,Salary,Tools_Research_Papers from Applicant_Login where FirstName='{}'".format(
                    applicants.get()))
            columns = [item for t in cursor.description for item in t]
            columns_final = list(filter(None, columns))
            values = [item for t in cursor.fetchall() for item in t]
            applicant_dict = dict(zip(columns_final, values))

            label_name = Label(schedule_interview_frame, text="Name", width=20, font=("bold", 10))
            label_name.place(x=80, y=140)

            name_text = Entry(schedule_interview_frame)
            name_text.insert('end', applicant_dict['FirstName'] + applicant_dict['LastName'])
            name_text.config(state=DISABLED)
            name_text.place(x=240, y=140)

            label_vacancy = Label(schedule_interview_frame, text="Vacancy applied", width=20, font=("bold", 10))
            label_vacancy.place(x=80, y=165)

            vacancy_text = Entry(schedule_interview_frame)
            vacancy_text.insert('end', applicant_dict['VacancyApplied'])
            vacancy_text.config(state=DISABLED)
            vacancy_text.place(x=240, y=165)

            label_hr = Label(schedule_interview_frame, text="HR", width=20, font=("bold", 10))
            label_hr.place(x=80, y=195)

            hr_temp = []
            cursor.execute("select Name from HR_Login")
            hr_temp = [item for t in cursor.fetchall() for item in t]
            assigned_hr.set(hr_temp[0])

            hr_options = OptionMenu(schedule_interview_frame, assigned_hr, *hr_temp)
            hr_options.place(x=240, y=190)

            label_interview_date = Label(schedule_interview_frame, text="Interview Date", width=20, font=("bold", 10))
            label_interview_date.place(x=68, y=225)

            interview_date = DateEntry(schedule_interview_frame, width=12, background='darkblue', foreground='white',borderwidth=2)
            interview_date.pack(padx=10, pady=10)
            interview_date.place(x=240, y=225)

            label_time_list = Label(schedule_interview_frame, text="Time Picker", width=20, font=("bold", 10))
            label_time_list.place(x=80, y=260)

            time_list=['9 AM','11 AM','1 PM','3 PM']
            time_picker.set(time_list[0])
            time_picker_options = OptionMenu(schedule_interview_frame, time_picker, *time_list)
            time_picker_options.place(x=240, y=260)


            Button(schedule_interview_frame, text='Schedule Interview', width=20, bg='brown', fg='white',command=lambda:obj.scheduleInterview(applicant_dict['Email'],interview_date.get())).place(x=80, y=320)

        applicants.trace('w', populate_user_details)

    else:
        label_none = Label(schedule_interview_frame, text="No Shortlisted Candidates", width=20, font=("bold", 12))
        label_none.place(x=150, y=140)
obj=Schedule_Interview()
schedule_interview_frame.mainloop()