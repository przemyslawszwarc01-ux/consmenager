import sqlite3

conn = sqlite3.connect("construction.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('SELECT * FROM jobs')
jobs = c.fetchall()
print ("Create job-1 \nViev jobs-2 \nEdit job-3 \nChange job status-4")
menuchoice = input("enter your choice: ")
if menuchoice == "1":
    job_name = input("enter your job name: ")
    client_name = input("enter your client name: ")
    address = input("enter job address: ")
    discription = input("enter job description: ")
    job_start = input("enter job start time: ")
    job_end = input("enter job end time: ")
    if not job_end:
        job_end = 'T.B.D'
    job_status = input("enter job status: ")
    if not job_status:
        job_status = 'Planned'
    c.execute("""INSERT INTO jobs (job_name, client, address, description, start_date, end_date, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (job_name, client_name, address, discription, job_start, job_end, job_status))
    conn.commit()
    print("Job added")


if menuchoice == "2":
    jobchoiceviec = input("your jobs - 1 \n all jobs - 2 ")
    if jobchoiceviec == "2" :
        c.execute('SELECT * FROM jobs')
        jobs = c.fetchall()
        for num, job in enumerate(jobs, start=1):
            print(num, job["job_name"], job["address"], job["status"])
        jobchoice = input('choose job: ')

        c.execute('SELECT * FROM jobs WHERE job_id = ?', (jobchoice,))
        jb = c.fetchone()
        print(jb["job_name"],jb["client"],jb["address"],jb["description"],jb["start_date"],jb["end_date"], jb["status"])
        indjobchoice = input('assign workers = 1 \n remove workers = 2 ')
        if indjobchoice == "1" :




    #elif jobchoiceviec == "1" :
        #c.execute('SELECT * FROM jobs WHERE status = ?', (job_status,))


