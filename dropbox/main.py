import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import *

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

import os
from dotenv import load_dotenv


def get_env():
    load_dotenv()
    APP_KEY = os.getenv('APP_KEY')
    APP_SECRET = os.getenv('APP_SECRET')
    TOKEN = os.getenv('TOKEN')

    return APP_KEY, APP_SECRET, TOKEN


def getting_token():
    global dbx

    app_key, app_secret, _ = get_env()

    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")

    auth_code = input("Enter the authorization code here: ").strip()
    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)

    dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)

    with open(".env", "a") as f:
        f.write("TOKEN="+oauth_result.access_token + "\n")


def login():
    global dbx
    _, _, token = get_env()
    print(token)
    if token is None:
        print("TOKEN not found. Getting a new one:")
        token_window()
    else:
        dbx = dropbox.Dropbox(token)
        user_data = dbx.users_get_current_account()
        print(user_data.name, " ", user_data.email)


def del_listbox():
    listbox.delete(0, tk.END)


next_l = ''


def isFile(dropboxMeta):
    return isinstance(dropboxMeta, dropbox.files.FileMetadata)


def get_data():
    global next_l
    print("zacatek: "+next_l)
    next = listbox.get(ANCHOR)

    del_listbox()

    if next == "...":
        next_l = next_l[:next_l.rfind("/")]
    else:
        if next != "":
            next_l = "/" + next

    listbox.insert(1, "...")
    for x, entry in enumerate(dbx.files_list_folder(next_l).entries, 2):
        listbox.insert(x, entry.name)


def GUI():
    global root
    root = Tk()
    root.geometry("200x300")
    frame = Frame(root)
    frame.pack()

    label = Label(root, text="Cesty")
    label.pack()

    global listbox
    listbox = Listbox(root)

    listbox.pack()

    button1 = tk.Button(
        text="move",
        width=5,
        height=1,
        bg="blue",
        fg="yellow",
        command=get_data
    )
    button2 = tk.Button(
        text="download",
        width=5,
        height=1,
        bg="blue",
        fg="yellow",
        command=filen
    )
    button3 = tk.Button(
        text="login",
        width=5,
        height=1,
        bg="blue",
        fg="yellow",
        command=login
    )

    button1.pack()
    button2.pack()
    button3.pack()
    root.title("Main window")
    root.mainloop()
    return root


def write_token(auth_code, auth_flow):
    print(auth_flow, '\n', auth_code.strip())

    try:
        oauth_result = auth_flow.finish(auth_code.strip())
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)

    with open(".env", "a") as f:
        f.write("\n"+"TOKEN="+oauth_result.access_token + "\n")


def token_window():

    app_key, app_secret, _ = get_env()

    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = auth_flow.start()

    log_window = tk.Toplevel(root)
    tk.Label(log_window, text="Enter a key generated from webside:", bg='blue').pack()
    w = Text(log_window, height=1, borderwidth=0, width=100)
    w.insert(1.0, authorize_url)
    w.configure(state="disabled")
    w.configure(inactiveselectbackground=w.cget("selectbackground"))

    authbutton = Button(
        log_window,
        text="login",
        width=5,
        height=1,
        bg="blue",
        fg="yellow",
        command=lambda: write_token(loginentry.get(), auth_flow)
    )

    loginentry = tk.Entry(log_window)
    loginentry.pack()
    w.pack()

    authbutton.pack()

    log_window.title("Login window")


def download():
    dbx.files_download_to_file('/Users/michalpecina', 'video0-5.mov')


def filen():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    print(filename)


if __name__ == "__main__":
    GUI()

