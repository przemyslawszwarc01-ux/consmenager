import sqlite3
import platform
import os
import time

conn = sqlite3.connect('construction.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


def cleaner():
    time.sleep(1.5)
    os.system('cls' if platform.system() == "Windows" else 'clear')


def admin_menu(user):
    print("you are an admin")
    choice = input("reset password - 1\nadd worker - 2\nedit worker - 3\nlogout - 4\n> ")
    if choice == "2":
        name = input("enter the name of the user: ").strip()
        surname = input("enter the surname of the user: ").strip()
        new_login = input("enter login: ").strip()
        phone = input("enter phone number: ").strip()
        role = input("enter role: ").strip()
        if not (name and surname and new_login):
            print("name, surname and login are required")
            return True
        try:
            c.execute(
                "INSERT INTO workers (login, first_name, last_name, phone, password, role, active) "
                "VALUES (?, ?, ?, ?, '', ?, 1)",
                (new_login, name, surname, phone or None, role or None),
            )
            conn.commit()
            print("Worker added (they will set their password at first login)")
        except sqlite3.IntegrityError:
            print("That login already exists")
        return True
    if choice == "1":
        c.execute("SELECT login FROM workers")
        for u in c.fetchall():
            print(u["login"])
        target = input("Which user? ")
        c.execute("UPDATE workers SET password = '' WHERE login = ?", (target,))
        conn.commit()
        if c.rowcount:
            print("Password reset (user must set a new one at next login)")
        else:
            print("No such user")
        return True
    if choice == "3":
        c.execute("SELECT first_name, last_name FROM workers ORDER BY worker_id")
        for i, w in enumerate(c.fetchall(), start=1):
            print(f"{i}. {w['first_name']} {w['last_name']}")

    editchoice = input("choose user")
    #
    #
    #
    #
    #
    #
    #
    return choice != "4"

def user_menu(user):
    print("you are not an admin")
    return input("logout - 1\n> ") != "1"


while True:
    login = input("enter login: ").strip()
    c.execute("SELECT * FROM workers WHERE login = ?", (login,))
    row = c.fetchone()
    if row is None:
        print("wrong login")
        continue
    if not row["active"]:
        print("account disabled")
        continue

    if not row["password"]:
        new_pw = input("please set your new password: ")
        if not new_pw:
            print("password can't be empty")
            continue
        c.execute("UPDATE workers SET password = ? WHERE login = ?", (new_pw, login))
        conn.commit()
        print("password set, please log in again")
        continue

    if input("enter password: ") != row["password"]:
        print("login failed")
        continue

    print("logging in")
    cleaner()
    time.sleep(1)
    is_admin = (row["role"] or "").lower() == "admin"
    while True:
        print("Welcome", row["first_name"], row["last_name"])
        if not (admin_menu(row) if is_admin else user_menu(row)):
            break
        cleaner()
    cleaner()
