from tkinter import *
import sqlite3
from tkinter import messagebox

hr_login_frame = Tk()
hr_login_frame.geometry('500x500')
hr_login_frame.title("HR Login")

connector=sqlite3.connect('UserRegistrationDetails.db')
with connector:
    cursor=connector.cursor()


class Hr_Landing:

    def checkEligibility(self):
        cursor.execute('select Email, VacancyApplied, WorkExperience, Tools_Research_Papers from Applicant_Login where VacancyApplied is not null')
        columns = [item for t in cursor.description for item in t]
        columns_final = list(filter(None, columns))
        for row in cursor.fetchall():
            values = [t for t in row]
            applicant_dict = dict(zip(columns_final, values))
            exp=cursor.execute("select WorkExperience from Vacancy_Details where JobTitle='{}'".format(applicant_dict['VacancyApplied']))

            email=applicant_dict['Email']
            temp=str(list(exp.fetchall()[0])[0])

            if((temp!=applicant_dict['WorkExperience']) or applicant_dict['Tools_Research_Papers'] is None):
                cursor.execute("update Applicant_Login set isEligible=0 where email='{}'".format(email))
            else:
                cursor.execute("update Applicant_Login set isEligible=1 where email='{}'".format(email))

            connector.commit()
        messagebox.showinfo('Success','Candidates are filtered')

    def createVacancy(self):
        hr_login_frame.destroy()
        from create_job_vacancy import vacancy_frame
        vacancy_frame.mainloop()

    def updateVacancy(self):
        hr_login_frame.destroy()
        from update_vacancy import vacancy_update_frame
        vacancy_update_frame.mainloop()

    def initiateInterview(self):
        from initiate_interview import initiate_interview_frame
        initiate_interview_frame.mainloop()

    def scheduleInterview(self):
        from schedule_interview import schedule_interview_frame
        schedule_interview_frame.mainloop()

    def storeResults(self):
        from result_store import result_store_frame
        result_store_frame.mainloop()

    def hireCandidate(self):
        hr_login_frame.destroy()
        from hire_candidate import hire_candidate_frame
        hire_candidate_frame.mainloop()


cursor.execute("select * from Active_Session")
columns = [item for t in cursor.description for item in t]
columns_final = list(filter(None, columns))
values = [item for t in cursor.fetchall() for item in t]
applicant_dict = dict(zip(columns_final, values))

label_form = Label(hr_login_frame, text="Welcome {}!".format(applicant_dict['Name']), width=20, font=("bold", 20))
label_form.place(x=90, y=43)

cursor.execute('delete from Active_Session')
connector.commit()
obj=Hr_Landing()

Button(hr_login_frame, text='Create Vacancy', width=20, bg='brown', fg='white', command=lambda:obj.createVacancy()).place(x=160, y=100)

Button(hr_login_frame, text='Update Vacancy', width=20, bg='brown', fg='white', command=lambda:obj.updateVacancy()).place(x=160, y=130)

Button(hr_login_frame, text='Filter candidates', width=20, bg='brown', fg='white', command=lambda:obj.checkEligibility()).place(x=160, y=160)

Button(hr_login_frame, text='Initiate Interview', width=20, bg='brown', fg='white', command=lambda:obj.initiateInterview()).place(x=160, y=190)

Button(hr_login_frame, text='Schedule Interview', width=20, bg='brown', fg='white', command=lambda:obj.scheduleInterview()).place(x=160, y=220)

Button(hr_login_frame, text='Rate Candidate', width=20, bg='brown', fg='white', command=lambda:obj.storeResults()).place(x=160, y=250)

Button(hr_login_frame, text='Hire Candidate', width=20, bg='brown', fg='white', command=lambda:obj.hireCandidate()).place(x=160, y=280)

hr_login_frame.mainloop()
