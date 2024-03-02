from tkinter import *
import customtkinter
from tkinter import messagebox
import sqlite3
from tkcalendar import *
from datetime import date
import pickle
"""from python import UG"""

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.title("Login page")
app.geometry("400x600")
app.resizable(False, False)


# ==========================define table========================================
def submit():
    global input_username

    # add sqlite3 function=====================
    users = sqlite3.connect("users.db")
    db = users.cursor()
    # create table========================
    db.execute("CREATE TABLE IF NOT EXISTS usernames(user_name text)")
    users.commit()

    # authentication=======================================
    data = db.execute("SELECT user_name FROM usernames").fetchall()
    result = []
    # loop to add a new user name if it doesn't`t exist========================
    for t in data:
        result.append(t[0])
    # get username and save it to this variable to be used throughout the program
    input_username = login_entry.get()

    # function to check if the username exist else it will add=======================
    if input_username in result:
        global new
        new = ""
        # clear textbox after submission and open second window=======================
        login_entry.delete(0, END)
        messagebox.showinfo("Welcome", "Welcome back" + " " + input_username)
        app.withdraw()
        planningboard()

        users.close()
    # check if the entry box is empty=====
    elif input_username == " " or "":
        messagebox.showerror("Oh no!", "Incorrect login attributes, Put down a name")
    elif len(input_username) == 0:
        messagebox.showerror("Oh no!", "Incorrect login attributes, Put down a name")




    # if the user does not exist, add him
    else:
        try:
            # open the database and insert the username and create a dat file for the user
            db = users.cursor()
            db.execute("INSERT INTO usernames (user_name) VALUES (:u_name)",
                       {"u_name": login_entry.get()
                        })
            new = "Exists"
            users.commit()
            users.close()
            # Open the file
            output_file = open(input_username, "wb")

            # add the stuff to the file
            pickle.dump("", output_file)

            messagebox.showinfo("Welcome", "Welcome" + " " + input_username)
            app.withdraw()
            planningboard()
        except Exception as error:
            messagebox.showerror("Oh no!", "An error was encountered Try again")


# =========================================create the planning board======================================
def planningboard():
    global if_saved
    app2 = customtkinter.CTkToplevel()
    app2.title("mummy's planner")
    app2.geometry("1050x400")
    app2.resizable(False, False)
    if_saved = False

    # Check if the user has saved
    def destroy_all():
        if if_saved == False:
            response = messagebox.askyesnocancel("Oh no!", "You haven't saved! Do you want to save?")
            if response == True:
                return
            elif response == False:
                app.destroy()
            else:
                return
        else:
            app.destroy()

    app2.protocol("WM_DELETE_WINDOW", destroy_all)

    # create frame
    my_frame = customtkinter.CTkFrame(app2, corner_radius=10)
    my_frame.place(x=10, y=155)

    # create list box
    my_list = Listbox(my_frame, width=110, height=12, bg="#292929",  # the default color of most tkinter apps
                      bd=0, fg="white", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none")
    my_list.grid(row=0, column=0)

    stuff = []
    # Add dummy list to list box
    if new == "Exists":
        for item in stuff:
            my_list.insert(END, item)
    else:
        # Open the file
        input_file = open(input_username, "rb")

        # load the data from the file
        stuff = pickle.load(input_file)

        # output stuff to the list
        for item in stuff:
            my_list.insert(END, item)

    # create scrollbar
    my_scroll = Scrollbar(my_frame)
    my_scroll.grid(row=0, column=1, sticky=NS)

    # add scrollbar
    my_list.config(yscrollcommand=my_scroll.set)
    my_scroll.config(command=my_list.yview)

    # create horizontal scrollbar
    my_scroll2 = Scrollbar(my_frame)
    my_scroll2.grid(row=1, column=0, sticky=EW)

    # add horizontal scrollbar
    my_list.config(xscrollcommand=my_scroll2.set)
    my_scroll2.config(orient=HORIZONTAL, command=my_list.xview)

    # ===============================create add button=====================================
    def add():
        global if_updated, updated, selected
        try:
            # checks if the user is updating or adding
            if if_updated == True:
                # this are moving parts and the second past is the function clicker() if you scroll down
                updated = planning_entry.get(1.0, "end-1c")
                my_list.delete(selected)
                my_list.insert(selected, cal.get_date() + " : " + updated)
                planning_entry.delete(1.0, "end-1c")
                if_updated = False
            else:
                # this adds and not update
                my_list.insert(END, cal.get_date() + " : " + planning_entry.get(1.0, "end-1c"))
                planning_entry.delete(1.0, "end-1c")

        except Exception as a:
            messagebox.showerror("Oh no!", "There was an issue with updating the database, Try again")

    # --------------------------------------------------------------------------------------------------------------------------------

    # =========================================create reset button=================================
    def reset():
        try:
            my_list.delete(0, END)
        except Exception as e:
            messagebox.showerror("Oh no!", "Database reset wasn't successful, Try again")

    # --------------------------------------------------------------------------------------------------------------------------
    # this logs the user out
    def logout():
        # grab everything in our list
        stuff = my_list.get(0, END)
        # Open the file
        output_file = open(input_username, "wb")

        # add the stuff to the file
        pickle.dump(stuff, output_file)
        app2.withdraw()
        app.deiconify()

    # this saves the list
    def save():
        global if_saved
        if_saved = True
        try:
            # grab everything in our list
            stuff = my_list.get(0, END)
            # Open the file
            output_file = open(input_username, "wb")

            # add the stuff to the file
            pickle.dump(stuff, output_file)
            messagebox.showinfo("Success", "List has been saved")
        except Exception as s:
            messagebox.showerror("Oh no!", "An error was encountered while trying to save, Please Try again")

    # this crosses off a selected item as finished
    def cross_off():
        # we get the item that is currently selected
        for i in my_list.curselection():
            c = my_list.get(i)
            # inserts into the listbox the same item with an update of (finished)
            my_list.insert(my_list.curselection(), c + "  (finished)")
            my_list.delete(my_list.curselection())

    # this deletes a selected item
    def delete():
        my_list.delete(ANCHOR)

    # this is the double click binding which enables us to update the selected item
    global if_updated
    if_updated = False

    def clicker(e):
        global if_updated, selected
        if_updated = True
        for i in my_list.curselection():
            selected = my_list.curselection()
            c = my_list.get(i)
            planning_entry.insert(INSERT, "(You can erase the date)" + "  " + c)

    # this is the right click menu function
    def my_popup(e):
        # this sets the menu to popup wherever the mouse icon is
        my_menu.tk_popup(e.x_root, e.y_root)

    # -------------------------------------------------------------------------------------------------------------------------------

    # =======================================dashboard board widgets====================================================
    dashboard_label = customtkinter.CTkLabel(app2, text="DashBoard", text_font=("Courier, 30"))
    dashboard_label.place(x=5, anchor=NW)

    user_id_label = customtkinter.CTkLabel(app2, text="Current User :  " + str(input_username),
                                           text_font=("Courier, 10"))
    user_id_label.place(x=215, y=370)

    logout_btn = customtkinter.CTkButton(app2, text="Log out", fg_color="black", hover_color="dark grey",
                                         border_width=2, corner_radius=6,
                                         border_color="black", command=logout)
    logout_btn.place(x=5, y=370)

    planning_entry_label = customtkinter.CTkLabel(app2, text="What are your plans today?", text_font=("Courier, 10"))
    planning_entry_label.place(x=10, y=80)

    planning_entry_frame = customtkinter.CTkFrame(app2, corner_radius=10)
    planning_entry_frame.place(x=190, y=80)

    planning_entry = Text(planning_entry_frame, height=3, width=68, wrap=WORD, bd=0, bg="#292929", fg="silver",
                          font=("Helvetica", 10))
    planning_entry.pack(padx=10, pady=10)
    planning_entry.configure(insertbackground="white")

    add_entry_button = customtkinter.CTkButton(app2, text="Update", fg_color="black", hover_color="dark grey",
                                               border_width=2, corner_radius=6,
                                               border_color="black", command=add, width=10)
    add_entry_button.place(x=695, y=80)

    reset_button = customtkinter.CTkButton(app2, text="Reset the list", fg_color="black", hover_color="dark grey",
                                           border_width=2, corner_radius=6,
                                           border_color="black", command=reset, width=15)
    reset_button.place(x=935, y=370)

    save_btn = customtkinter.CTkButton(app2, text="Save the list", fg_color="black", hover_color="dark grey",
                                       border_width=2, corner_radius=6,
                                       border_color="black", command=save, width=15)
    save_btn.place(x=800, y=370)

    # this was old code but if you scroll to bindings, you'll see that instead of buttons i used the right click binding
    """

    crossoff_btn = customtkinter.CTkButton(app2, text="Finished a plan", fg_color="black", hover_color="dark grey",
                                           border_width=2, corner_radius=6,
                                           border_color="black", command=cross_off, width=15)
    crossoff_btn.place(x=650, y=370)

    delete_btn = customtkinter.CTkButton(app2, text="Delete a plan", fg_color="black", hover_color="dark grey",
                                         border_width=2, corner_radius=6,
                                         border_color="black", command=delete, width=15)
    delete_btn.place(x=500, y=370)
    """

    # -------------------------------------------------------------------------------------------------------------------------------
    # CREATE CALENDER OPTION========================================================
    cal_lbl = customtkinter.CTkLabel(app2, text="Select the date of the plan", text_font=("Courier, 10"))
    cal_lbl.place(x=800, y=55)
    # today = the command to get the systems date
    today = date.today()
    dateOS = today.strftime("%d")
    convert_dateOS = int(dateOS)
    monthOS = today.strftime("%m")
    convert_monthOS = int(monthOS)
    yearOS = today.strftime("%Y")
    convert_yearOS = int(yearOS)
    # we display the calendar widget and set the automatic date to the system date
    cal = Calendar(app2, selectmode="day", year=convert_yearOS, month=convert_monthOS, day=convert_dateOS)
    cal.place(x=780, y=80)

    # create update binding
    my_list.bind("<Double-1>", clicker)

    # Create a menu and right click binding options
    my_menu = Menu(app2, tearoff=False)
    my_menu.add_command(label="Finished", command=cross_off)
    my_menu.add_separator()
    my_menu.add_command(label="Delete", command=delete)
    my_list.bind("<Button-3>", my_popup)


# =======================login window============================
welcome_label = customtkinter.CTkLabel(app, text="Daily Planner", text_font=("Courier, 15"))
welcome_label.place(relx=0.5, y=30, anchor=CENTER)

show_login_img_frame = customtkinter.CTkFrame(app, corner_radius=10, width=390, height=290)
show_login_img_frame.place(relx=0.5, y=200, anchor=CENTER)

login_img = PhotoImage(file="plans_image/login_img2.png")
show_login_img = customtkinter.CTkLabel(show_login_img_frame, text="", image=login_img, bg_color="black",
                                        fg_color="black")
show_login_img.place(relx=0.5, y=140, anchor=CENTER)

login_entry = customtkinter.CTkEntry(app, border_width=2, placeholder_text="Enter your username", corner_radius=6,
                                     width=250)
login_entry.place(relx=0.5, y=400, anchor=CENTER)

login_btn = customtkinter.CTkButton(app, text="Login", corner_radius=6, border_width=2, border_color="black",
                                    fg_color="black", hover_color="dark grey",
                                    command=submit)
login_btn.place(relx=0.5, y=450, anchor=CENTER)

app.mainloop()
