from CmdHelper import AdbCommandHelper
from tkinter import *
from pathlib import Path

def selectDevice():
    adb.setSelectedDevice(rb_selected_device.get())
    print("Device Selected: " + rb_selected_device.get())

def listAvailableDB():
    db_list = adb.listAvailableDB()

    db_frame = Frame(right_frame, bg="orange")
    db_frame.pack(fill="both", expand=True)

    canvas = Canvas(db_frame)
    scrollbar = Scrollbar(db_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.config(xscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)

    image = PhotoImage(file = (Path.cwd() / "images/ic_db.png").resolve()).subsample(8, 8)

    content_frame = Frame(canvas, bg="orange")
    canvas.create_window((0, 0), window=content_frame, anchor='nw')
    for i, db in enumerate(db_list):
        button = Button(content_frame, text=db, image=image, compound=TOP)
        button.image = image
        button.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky='nsew')

    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


root = Tk()
adb = AdbCommandHelper()

root.title("Android ADB Helper")
root.geometry('700x400')

left_frame = Frame(root, width=100, bg="blue")
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

right_frame = Frame(root, bg="pink")
right_frame.pack(fill="both", expand=True)

buttons_frame = Frame(right_frame, height=100, bg="green")
buttons_frame.pack(side="top", fill="x")
buttons_frame.pack_propagate(False)


Label(left_frame, text = "Device List").pack(fill="x")
Button(buttons_frame, text = "DB", fg = "red", command=listAvailableDB).pack()


rb_selected_device = StringVar()
for device in adb.listDevices():
    radio = Radiobutton(left_frame, text=device[0], variable=rb_selected_device,
                        value=device[0], indicator=0, background="light blue", command=selectDevice)
    radio.pack(fill=X, ipady=5)





#device_list_frame = Frame(left_frame, bg="purple")
#device_list_frame.pack(fill=BOTH)


#devices = adb.listDevices()
#var = StringVar()
#for device in devices:
#    radio = Radiobutton(device_list_frame, text=device[0], variable=var, value=device[0], command=selectDevice)
#    radio.pack(anchor=W)




#def clicked():
#    print(adb.listDevices())
    #lbl.configure(text = " Clicked ")

#btn = Button(root, text = "Click me", fg = "red", command=clicked)
# set Button grid
#btn.grid(column=1, row=0)


root.mainloop()




#import sqlite3
#import subprocess as cmd

# Get the result of the adb shell command
#result = cmd.check_output("adb shell ls /data/system/").splitlines()

# Filter strings that end with .db
#db_files = [s.decode('utf-8') for s in result if s.decode('utf-8').endswith(".db")]




#dbFile = "/data/system/enterprise.db"
#result = cmd.call("adb pull " + dbFile, shell=True)
#connection = sqlite3.connect("enterprise.db")
#cursor = connection.cursor()
#table_list = [a for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
#print(table_list)
#connection.close()