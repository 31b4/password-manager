import random, string, sys, getpass, os
from termcolor import colored
import pyperclip
import sqlite3
conn = sqlite3.connect('1d4b.db')
c = conn.cursor()
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
PASSWORD ="123"
connect = getpass.getpass(".--. .- ... ... ..--..\n")
while connect != PASSWORD:
    clear()
    connect = getpass.getpass(".--. .- ... ... ..--..\n")
    if connect == "q":
        clear()
        sys.exit()

def PassGenerate():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(16))
def NewService(service,username):
    print("No "+colored(service,'blue')+"->"+colored(username,'red')+" was found.")
    crtPass = PassGenerate()
    print("Rnd password 4 "+colored(service,'blue')+":",colored(crtPass,'red'))
    return crtPass
def GetService():
    return input("Service: ")
def GetPass():
    clear()
    print("*********31b4*********")
    print("-------getPass-------")
    service = GetService()
    username = GetUsrName()
    if service == 'q' or username =='q':
        return
    if username =="*":
        c.execute('SELECT * FROM passes WHERE service=?',(service,))
        [print (row) for row in c.fetchall()]
        input()
        return
    c.execute('SELECT password FROM passes WHERE service=? AND username=? ',(service,username,))
    
    asd ="";
    for row in c.fetchall():
        asd = row
    if asd!='':
        pyperclip.copy(str(asd[0]))
        print("Copied to clipboard.")
    else:
        print("No "+colored(service,'blue')+" service found.")
    # ha nincs jelszo ennel a szolgaltatonal =>
    input()
    return
def GetUsrName():
    return input("UsrName: ")
def StorePass():
    clear()
    print("*********31b4*********")
    print("------storePass------")
    service = GetService()
    username = GetUsrName()
    if service == 'q' or username=='q':
        return
    c.execute('SELECT password FROM passes WHERE service=? AND username=? ',(service,username,))
    asd = c.fetchall()
    if len(asd) == 0:
        crtPass = NewService(service,username)
        answer =getpass.getpass("use it? y/n")
        if answer == "y":
            print("generated pass saved at "+ colored(service,'blue')+"->"+colored(username,'red'))
        elif answer == "n" or answer=="no":
            crtPass = input("type your pass 4 "+colored(service,'blue')+"->"+colored(username,'red')+": ")
            if crtPass=='q':
                return
        else:
            return
        c.execute('INSERT INTO passes(service,username,password) VALUES(?,?,?)',(service,username,crtPass))    
        conn.commit()
        print("saved.")
    else:
        clear()
        print("*********31b4*********")
        print("------updatePass------")
        crtPass = PassGenerate()
        answer = getpass.getpass("Do you want to update your pass at "+colored(service,'blue')+"->"+colored(username,'red')+" with: "+colored(crtPass,'red')+" y/n?")
        if answer == "y":
            print("generated pass updated at "+ colored(service,'blue')+"->"+colored(username,'red'))
        else:
            crtPass = input("type new pass 4 "+colored(service,'blue')+"->"+colored(username,'red')+": ")
        c.execute('UPDATE passes SET password = ? WHERE service = ? AND username=?',(crtPass,service,username,))
        conn.commit()
        print("updated.")
    input()
def CreateTable():
    c.execute('CREATE TABLE IF NOT EXISTS passes(service TEXT, username TEXT, password TEXT)')
def DeleteFrom():
    clear()
    print("*********31b4*********")
    print("------DeleteFrom------")
    service = GetService()
    username = GetUsrName()
    if username=='' or service =='':
        return
    if username=='*':
        c.execute('SELECT password FROM passes WHERE service=?',(service,))
        asd = c.fetchall()
        if len(asd) >0:
            print("Deleted all acc at "+colored(service,'blue'))
            c.execute('DELETE FROM passes WHERE service=?',(service,))
            conn.commit()
            return
        print("No "+colored(service,'blue')+" service found.")
    else:
        c.execute('SELECT password FROM passes WHERE service=? AND username=? ',(service,username,))
        asd = c.fetchall()
        if len(asd) >0:
            print("Deleted "+colored(username,'red')+" acc at "+colored(service,'blue'))
            c.execute('DELETE FROM passes WHERE service=? AND username=?',(service,username,))
            conn.commit()
            return
        print("not found "+ colored(service,'blue')+"->"+colored(username,'red'))

def GetAll():
    clear()
    print("*********31b4*********")
    print("All stored data")
    print(colored("at",'red')+ " / "+ colored("username",'green')+" / "+colored("password",'blue')+'\n')
    c.execute('SELECT * FROM passes ')
    if len(c.fetchall())==0:
        print("empty database")
    else:
        c.execute('SELECT * FROM passes ')
        for row in c.fetchall():
            print(colored(row[0],'red')+ " "+ colored(row[1],'green')+" "+colored(row[2],'blue'))
    input()
    return
def InMenu():
    while True:
        clear()
        print("*********31b4*********")
        
        CreateTable()

        command = getpass.getpass("Go on...  \n")
        if command=="q":
            clear()
            sys.exit()
        elif command == "404":
            clear()
            os.system('shutdown /s /t 0')
        elif command == "gp":# get pass
            GetPass()
        elif command == "sp": # store pass
            StorePass()
        elif command == "ga": # get all 
            GetAll()
            
        elif command == "gaf": # get all from
            c.execute('SELECT * FROM passes WHERE service =?',(GetService(),))
            [print (row) for row in c.fetchall()]
            input()
        elif command == "rf" or command == "df": # remove from \ delete from
            DeleteFrom()
            input()
InMenu()
input("press any key")