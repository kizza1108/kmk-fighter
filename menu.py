import sys, os, random, re
from tkinter import *
from tkinter import ttk, messagebox
from main import run_fighter_game
from Database import DB
from email_sender import Send_email

db = DB()


#  validating an Email function
def email_validation(mail):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat, mail):
        return True
    else:
        return False


def widget_enter(event, widget, text):
    if widget.get() == text:
        widget.delete(0, END)
    if text == 'Password' or text == 'Confirm Password':
        widget.config(show='*')


def widget_focus_out(evnet, widget, text):
    if widget.get() == '':
        widget.insert(0, text)
    if text == 'Password' or text == 'Confirm Password':
        if widget.get() in ('Password', 'Confirm Password', ''):
            widget.config(show='')


class GUI(Tk):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.font_name = 'Microsoft Yahei UI Light'
        self.font_size = 12
        self._1st_player_logged = False
        self._2nd_player_logged = False
        self.font = (self.font_name, self.font_size)
        self.font_bold = (self.font_name, self.font_size, 'bold')
        # for open tkinter window at center point
        w = 1000  # Width
        h = 600  # Height

        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # self.geometry('1000x600+100+100')
        self.title("KMK-Fighting")
        self.resizable(False, False)
        self.Menu_Page()  # Menu_Page()
        self.Select_Character_Page()
        self.Login()
        self.Signup()
        self.character_images = []
        self.load_character_images()
        self.mainloop()

    def Menu_Page(self):
        self.menu_frame = Frame(self)
        self.menu_frame.pack(fill=BOTH, expand=True)
        self.bg_image = PhotoImage(file='assets/images/bg1.png')
        Label(self.menu_frame, image=self.bg_image).place(x=-2, y=-2)

        Button(self.menu_frame, text='Play', font=self.font_bold, fg='White', bg='gray40', width=13,
               command=lambda: [self.menu_frame.pack_forget(), self.login_frame.pack(fill=BOTH, expand=1)]).place(
            x=635, y=215)

        Button(self.menu_frame, text='Sign Up', font=self.font_bold, fg='White', bg='gray40', width=13,
               command=lambda: [self.menu_frame.pack_forget(), self.signup_frame.pack(fill=BOTH, expand=1)]).place(
            x=635, y=280)

        Button(self.menu_frame, text='LeaderBoard', font=self.font_bold, fg='White', bg='gray40', width=13,
               command=lambda: messagebox.showinfo("LeaderBoard", db.get_leader_board())).place(
            x=635, y=345)

        Button(self.menu_frame, text='Exit', font=self.font_bold, fg='White', bg='gray40', width=13,
               command=lambda: sys.exit()).place(x=635, y=410)

    def Select_Character_Page(self):
        self.select_charater = Frame(self)
        # self.select_charater.pack(fill=BOTH, expand=1)
        self.sc_img = PhotoImage(file='assets/images/cs.png')
        Label(self.select_charater, image=self.sc_img).place(x=-2, y=-2)
        Button(self.select_charater, text='Start', width=10, bg='#1c74f7', fg='White',
               font=self.font_bold, command=lambda: self.start_game()).place(x=425, y=524)
        Button(self.select_charater, text='Back', width=10, bg='#1c74f7', fg='White',
               font=self.font_bold, command=lambda: [self.select_charater.pack_forget(),
                                                     self.login_frame.pack(fill=BOTH, expand=1)]).place(x=425, y=564)

        player_one_frame = Frame(self.select_charater, bg='#1c74f7', width=300)
        player_one_frame.pack(side=LEFT, fill=Y)
        player_one_frame.propagate(False)
        player_two_frame = Frame(self.select_charater, width=300, bg='#1c74f7')
        player_two_frame.pack(side=RIGHT, fill=Y)
        player_two_frame.propagate(False)

        Label(player_one_frame, text='Player 1', font=(self.font_name, self.font_size + 8, 'bold'), fg='White',
              bg='#1c74f7').pack(pady=30)
        self.player_one = ttk.Combobox(player_one_frame, width=12, font=self.font, state='readonly',
                                       values=['Human', 'Huntress', 'King', 'Samurai', 'Warrior', 'Wizard'])
        self.player_one.pack(pady=(0, 10))
        self.player_one.bind("<<ComboboxSelected>>", self.show_character_image)

        self.player_one_img = Label(player_one_frame, image='', bg='#1c74f7')
        self.player_one_img.pack(pady=0)

        Label(player_two_frame, text='Player 2', font=(self.font_name, self.font_size + 8, 'bold'), fg='White',
              bg='#1c74f7').pack(side=BOTTOM, pady=30)
        self.player_two = ttk.Combobox(player_two_frame, width=12, font=self.font, state='readonly',
                                       values=['Human', 'Huntress', 'King', 'Samurai', 'Warrior', 'Wizard'])
        self.player_two.pack(side=BOTTOM, pady=(0, 10))
        self.player_two.bind("<<ComboboxSelected>>", self.show_character_image)
        self.player_two_img = Label(player_two_frame, image='', bg='#1c74f7')
        self.player_two_img.pack(side=BOTTOM, pady=10)

    def show_character_image(self, event):
        if self.player_two.get() != '':
            self.player_two_img.config(image=self.character_images[self.player_two.current()])
        if self.player_one.get() != '':
            self.player_one_img.config(image=self.character_images[self.player_one.current()])

    def load_character_images(self):
        path_list = os.listdir('assets/images/characters')
        print(path_list.sort())
        for cnt in path_list:
            if cnt.endswith(".png"):
                img = PhotoImage(file='assets/images/characters/' + cnt)
                self.character_images.append(img)
            print(cnt)

    def start_game(self):
        p1 = self.player_one.get()
        p2 = self.player_two.get()
        if p1 != '':
            if p2 != '':
                p1_index = self.player_one.current()
                p2_index = self.player_two.current()
                bg_image_index = random.choice(range(3))
                self.withdraw()
                run_fighter_game(p1_index, p2_index, bg_image_index,
                                 self.username_field_1st.get(), self.username_field_2nd.get(), db)
                self.deiconify()

            else:
                messagebox.showwarning('Warning', "Player 2 haven't select any character yet.... ")
        else:
            messagebox.showwarning('Warning', "Player 1 haven't select any character yet.... ")

    # Login window GUI code
    def Login(self):
        self.login_frame = Frame(self)
        # self.login_frame.pack(fill=BOTH, expand=1)
        self.login_img = PhotoImage(file='assets/images/login.png')
        Label(self.login_frame, image=self.login_img).place(x=-2, y=-2)
        Button(self.login_frame, text='Start', width=10, bg='#1c74f7', fg='White',
               font=self.font_bold, command=lambda: self.check_both_logged_in()).place(x=425, y=524)
        Button(self.login_frame, text='Back', width=10, bg='#1c74f7', fg='White',
               font=self.font_bold, command=lambda: [self.login_frame.pack_forget(),
                                                     self.menu_frame.pack(fill=BOTH, expand=1)]).place(x=425, y=564)

        player_one_frame = Frame(self.login_frame, bg='#1c74f7', width=300)
        player_one_frame.pack(side=LEFT, fill=Y)
        player_one_frame.propagate(False)
        player_two_frame = Frame(self.login_frame, width=300, bg='#1c74f7')
        player_two_frame.pack(side=RIGHT, fill=Y)
        player_two_frame.propagate(False)

        self._1st_login_frame = Frame(player_one_frame, bg='#1c74f7')
        self._1st_login_frame.pack(pady=150)
        self.login_frame_1 = Frame(self._1st_login_frame, bg='#1c74f7')
        self.login_frame_1.pack()
        Label(self.login_frame_1, text='Player 1 Login', bg='#1c74f7', fg='White',
              font=(self.font_name, self.font_size + 7, 'bold')).pack(pady=20)

        self.username_field_1st = Entry(self.login_frame_1, width=20, font=('Microsoft Yahei UI Light', 11, 'bold'),
                                        bd=0,
                                        fg='firebrick1')
        self.username_field_1st.pack()
        self.username_field_1st.insert(0, 'Username')
        self.username_field_1st.bind('<FocusIn>',
                                     lambda event, a=self.username_field_1st, b='Username': widget_enter(event, a, b))
        self.username_field_1st.bind('<FocusOut>',
                                     lambda event, a=self.username_field_1st, b='Username': widget_focus_out(event, a,
                                                                                                             b))

        Frame(self.login_frame_1, width=168, height=2, bg='firebrick1').pack(pady=(0, 10))

        self.password_field_1st = Entry(self.login_frame_1, width=20, font=('Microsoft Yahei UI Light', 11, 'bold'),
                                        bd=0,
                                        fg='firebrick1')
        self.password_field_1st.pack()
        self.password_field_1st.insert(0, 'Password')
        self.password_field_1st.bind('<FocusIn>',
                                     lambda event, a=self.password_field_1st, b='Password': widget_enter(event, a, b))

        self.password_field_1st.bind('<FocusOut>',
                                     lambda event, a=self.password_field_1st, b='Password': widget_focus_out(event, a,
                                                                                                             b))

        Frame(self.login_frame_1, width=168, height=2, bg='firebrick1').pack()

        Button(self.login_frame_1, text='Login', font=('Open Sans', 16, 'bold'), fg='white',
               bg='firebrick1',
               activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=12,
               command=lambda: self.sign_in(0)).pack(
            pady=10)
        Button(self.login_frame_1, text='Forgot Password?', bd=0, bg='#1c74f7', activebackground='white',
               cursor='hand2',
               font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', activeforeground='firebrick1',
               command=lambda: self.forget_pass(1)).pack()

        # player 2 login
        self._2nd_login_frame = Frame(player_two_frame, bg='#1c74f7')
        self._2nd_login_frame.pack(pady=150)
        self.login_frame_2 = Frame(self._2nd_login_frame, bg='#1c74f7')
        self.login_frame_2.pack()
        Label(self.login_frame_2, text='Player 2 Login', bg='#1c74f7', fg='White',
              font=(self.font_name, self.font_size + 7, 'bold')).pack(pady=20)

        self.username_field_2nd = Entry(self.login_frame_2, width=20, font=('Microsoft Yahei UI Light', 11, 'bold'),
                                        bd=0,
                                        fg='firebrick1')
        self.username_field_2nd.pack()
        self.username_field_2nd.insert(0, 'Username')
        self.username_field_2nd.bind('<FocusIn>',
                                     lambda event, a=self.username_field_2nd, b='Username': widget_enter(event, a, b))
        self.username_field_2nd.bind('<FocusOut>',
                                     lambda event, a=self.username_field_2nd, b='Username': widget_focus_out(event, a,
                                                                                                             b))

        Frame(self.login_frame_2, width=168, height=2, bg='firebrick1').pack(pady=(0, 10))

        self.password_field_2nd = Entry(self.login_frame_2, width=20, font=('Microsoft Yahei UI Light', 11, 'bold'),
                                        bd=0,
                                        fg='firebrick1')
        self.password_field_2nd.pack()
        self.password_field_2nd.insert(0, 'Password')
        self.password_field_2nd.bind('<FocusIn>',
                                     lambda event, a=self.password_field_2nd, b='Password': widget_enter(event, a, b))

        self.password_field_2nd.bind('<FocusOut>',
                                     lambda event, a=self.password_field_2nd, b='Password': widget_focus_out(event, a,
                                                                                                             b))

        Frame(self.login_frame_2, width=168, height=2, bg='firebrick1').pack()

        Button(self.login_frame_2, text='Login', font=('Open Sans', 16, 'bold'), fg='white',
               bg='firebrick1',
               activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=12,
               command=lambda: self.sign_in(1)).pack(pady=10)
        Button(self.login_frame_2, text='Forgot Password?', bd=0, bg='#1c74f7', activebackground='white',
               cursor='hand2',
               font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', activeforeground='firebrick1',
               command=lambda: self.forget_pass(2)).pack()

    def check_both_logged_in(self):
        if self._1st_player_logged and self._2nd_player_logged:
            self.login_frame.pack_forget()
            self.select_charater.pack(fill=BOTH, expand=1)
        else:
            messagebox.showwarning("Warning", "Both user need to login before continue...")

    def sign_in(self, which_player):
        player = [
            [self.username_field_1st.get(), self.password_field_1st.get(), self.login_frame_1, self._1st_login_frame,
             self._1st_player_logged],
            [self.username_field_2nd.get(), self.password_field_2nd.get(), self.login_frame_2, self._2nd_login_frame,
             self._2nd_player_logged]]
        u_name = player[which_player][0]
        pass_ = player[which_player][1]
        if u_name not in ('Username', '') and pass_ not in ('Password', ''):
            get_user = db.get_user(u_name.upper())
            if get_user:
                if get_user[2] == pass_:
                    player[which_player][2].pack_forget()
                    Label(player[which_player][3], text=str(get_user[1]) + '\nlogged in Successfully',
                          font=(self.font_name, self.font_size + 8), bg='#1c74f7', fg='white').pack(pady=(50, 20))
                    Button(player[which_player][3], text='Player Stat', font=self.font_bold,
                           command=lambda: messagebox.showinfo("Player Statics",
                                                               db.player_stat(player[which_player][0].upper()))).pack()
                    if which_player == 0:
                        self._1st_player_logged = True
                    elif which_player == 1:
                        self._2nd_player_logged = True
                    # check both user logged in successfully
                    # print(self._1st_player_logged, self._2nd_player_logged)
                    # if self._1st_player_logged and self._2nd_player_logged:
                    #     self.login_frame.pack_forget()
                    #     self.select_charater.pack(fill=BOTH, expand=1)
                else:
                    messagebox.showwarning("Warning", "InValid Password...")
            else:
                messagebox.showwarning("Warning", "InValid Username...")
        else:
            messagebox.showwarning("Warning", "Can't Leave Fields Null...")

    def forget_pass(self, which_user):
        if which_user == 1:
            u_name = self.username_field_1st.get()
        else:
            u_name = self.username_field_2nd.get()
        if u_name in ('Username', ''):
            messagebox.showwarning("Warning", "Username Required....")
        else:
            user_res = db.get_user(u_name.upper())
            if user_res:
                response = messagebox.askyesno("Reset Password",
                                               "Click OK will send a new password instruction to your Email id and will"
                                               " reset your current password.\nDo you want to continue? ")

                if response:

                    mail_id = user_res[-1]
                    pass_ = ''
                    for pas in range(6):
                        num = random.choice(range(0, 10))
                        pass_ += str(num)
                    msg = Send_email(mail_id, pass_)
                    if msg[-1]:
                        self.withdraw()
                        self.popup = Toplevel()
                        self.popup.title('KMK-Fighting (Password reset)')
                        self.popup.config(bg='#1c74f7')
                        x = (self.winfo_screenwidth() / 2) - (300 / 2)
                        y = (self.winfo_screenheight() / 2) - (300 / 2)
                        self.popup.geometry(f'300x300+{round(x)}+{round(y)}')
                        Label(self.popup, text='Reset Password', font=(self.font_name, self.font_size + 12, 'bold'),
                              fg='White', bg='#1c74f7').pack(pady=20)
                        Label(self.popup, text='New Password', font=self.font_bold, bg='#1c74f7', fg='White').pack()
                        self.new_pass = Entry(self.popup, font=self.font, width=20)
                        self.new_pass.pack(pady=(2, 10))
                        self.new_pass.delete(0, END)
                        Label(self.popup, text='Code', font=self.font_bold, bg='#1c74f7', fg='White').pack()
                        self.code = Entry(self.popup, font=self.font, width=20)
                        self.code.pack(pady=(2, 10))
                        self.code.delete(0, END)
                        Button(self.popup, text='Update', font=self.font_bold,
                               command=lambda: self.reset_pass(pass_, u_name, msg[0])).pack(pady=10)
                        self.popup.wait_window()
                        self.deiconify()
                    else:
                        messagebox.showerror("Error", msg[0])
            else:
                messagebox.showwarning("Warning", "No User Found with this name...")

    def reset_pass(self, pass_, u_name, msg):
        new_password = self.new_pass.get()
        code_ = self.code.get()
        if new_password != '' and code_ != '':
            if code_ == pass_:

                res = db.update_profile(data=[str(new_password), u_name.upper()])
                print(res)
                messagebox.showinfo("Success", msg)
                self.popup.destroy()
            else:
                messagebox.showwarning('Waring', "Failed: Invalid Code !!!")
        else:
            messagebox.showwarning("Warning", "Password and Code Field required")

    # Sign up GUI window code
    def Signup(self):
        self.signup_frame = Frame(self)
        # self.signup_frame.pack(fill=BOTH, expand=1)

        self.sigup_img = PhotoImage(file='assets/images/signup.png')
        Label(self.signup_frame, image=self.sigup_img).place(x=-2, y=-2)

        heading = Label(self.signup_frame, text='Sign Up', font=(self.font_name, self.font_size + 12, 'bold'),
                        bg='white',
                        fg='firebrick1')
        heading.place(x=660, y=111)

        self.r_username_field = Entry(self.signup_frame, width=30, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0,
                                      fg='firebrick1')
        self.r_username_field.place(x=590, y=170)
        self.r_username_field.insert(0, 'Username')
        self.r_username_field.bind('<FocusIn>',
                                   lambda event, a=self.r_username_field, b='Username': widget_enter(event, a, b))
        self.r_username_field.bind('<FocusOut>',
                                   lambda event, a=self.r_username_field, b='Username': widget_focus_out(event, a, b))

        Frame(self.signup_frame, width=250, height=2, bg='firebrick1').place(x=590, y=192)

        self.r_password_field = Entry(self.signup_frame, width=30, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0,
                                      fg='firebrick1')
        self.r_password_field.place(x=590, y=230)
        self.r_password_field.insert(0, 'Password')
        self.r_password_field.bind('<FocusIn>',
                                   lambda event, a=self.r_password_field, b='Password': widget_enter(event, a, b))

        self.r_password_field.bind('<FocusOut>',
                                   lambda event, a=self.r_password_field, b='Password': widget_focus_out(event, a, b))

        pass_frame = Frame(self.signup_frame, width=250, height=2, bg='firebrick1')  # frame for the entry fields
        pass_frame.place(x=590, y=252)

        self.r_c_password_field = Entry(self.signup_frame, width=30, font=('Microsoft Yahei UI Light', 11, 'bold'),
                                        bd=0,
                                        fg='firebrick1')
        self.r_c_password_field.place(x=590, y=290)
        self.r_c_password_field.insert(0, 'Confirm Password')
        self.r_c_password_field.bind('<FocusIn>',
                                     lambda event, a=self.r_c_password_field, b='Confirm Password': widget_enter(event,
                                                                                                                 a, b))
        self.r_c_password_field.bind('<FocusOut>',
                                     lambda event, a=self.r_c_password_field, b='Confirm Password': widget_focus_out(
                                         event,
                                         a, b))
        Frame(self.signup_frame, width=250, height=2, bg='firebrick1').place(x=590, y=312)

        self.r_email_field = Entry(self.signup_frame, width=30, font=('Microsoft Yahei UI Light', 11, 'bold'),
                                   bd=0, fg='firebrick1')
        self.r_email_field.place(x=590, y=350)
        self.r_email_field.insert(0, 'Email')
        self.r_email_field.bind('<FocusIn>', lambda event, a=self.r_email_field, b='Email': widget_enter(event, a, b))
        self.r_email_field.bind('<FocusOut>',
                                lambda event, a=self.r_email_field, b='Email': widget_focus_out(event, a, b))

        Frame(self.signup_frame, width=250, height=2, bg='firebrick1').place(x=590, y=372)

        Button(self.signup_frame, text='Sign Up', font=('Open Sans', 16, 'bold'), fg='white',
               bg='firebrick1',
               activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=20,
               command=lambda: self.store_user_in_db()).place(x=590, y=400)

        Button(self.signup_frame, text='Back', font=('Open Sans', 16, 'bold'), fg='white', bg='firebrick1', bd=0,
               width=20, activeforeground='white', activebackground='firebrick1', cursor='hand2',
               command=lambda: [self.signup_frame.pack_forget(), self.menu_frame.pack(fill=BOTH, expand=1),
                                self.clear_signup_fields()]).place(
            x=590, y=440)

    def store_user_in_db(self):
        username = self.r_username_field.get()
        pass_ = self.r_password_field.get()
        pass_c = self.r_c_password_field.get()
        mail = self.r_email_field.get()
        if (username != 'Username' or pass_ != 'Password' or pass_c != 'Confirm Password' or mail != 'Email') and (
                username != '' or pass_ != '' or pass_c != '' or mail != ''):
            if pass_ == pass_c:
                if email_validation(mail):
                    res = db.insert_profile([username.upper(), pass_, mail])
                    messagebox.showinfo("Success", res)
                    self.clear_signup_fields()
                else:
                    messagebox.showwarning("Warning", "InValid Email...")
            else:
                messagebox.showwarning("Warning", "Password and Confirm Password are not same...")
        else:
            messagebox.showwarning("Warning", "Fields can't be null or Default text...")

    def clear_signup_fields(self):
        # clear fields
        self.r_username_field.delete(0, END)
        self.r_email_field.delete(0, END)
        self.r_password_field.delete(0, END)
        self.r_c_password_field.delete(0, END)
        # insert default data
        self.r_username_field.insert(0, 'Username')
        self.r_email_field.insert(0, 'Email')
        self.r_password_field.insert(0, 'Password')
        self.r_c_password_field.insert(0, 'Confirm Password')
        # don't hide text
        self.r_password_field.config(show='')
        self.r_c_password_field.config(show='')


gui = GUI()








