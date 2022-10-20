import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import time
import sys

username = ""
recipient = ""
contacts = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/mschat/all/#")
    client.subscribe("/mschat/status/#")
    client.subscribe("/mschat/user/{0}/#".format(username))
    client.publish("/mschat/status/{0}".format(username), payload="online", qos=0, retain=True)


def on_message(client, userdata, msg):
    global contacts
    print(msg.topic+" "+str(msg.payload))
    if msg.topic.startswith("/mschat/all/"):
        public_chat.config(state=tk.NORMAL)
        public_chat.insert(tk.END, msg.topic[12:] + ": " + msg.payload.decode("utf-8").strip() + "\n")
        public_chat.see(tk.END)
        public_chat.config(state=tk.DISABLED)
    elif msg.topic.startswith("/mschat/user/"):
        private_chat.config(state=tk.NORMAL)
        private_chat.insert(tk.END, "FROM: " + msg.topic[13:].split("/")[1] + "\n" + msg.payload.decode("utf-8").strip() + "\n\n")
        private_chat.see(tk.END)
        private_chat.config(state=tk.DISABLED)
    elif msg.topic.startswith("/mschat/status/"):
        contacts[msg.topic[15:]] = msg.payload.decode("utf-8").strip()
        contact_list.delete(0, tk.END)
        for i,(k,v) in enumerate(contacts.items()):
            contact_list.insert(tk.END, k + ": " + v)
            color = 'black'
            if v.lower() == 'online':
                color = 'dark green'
            elif v.lower() == 'offline':
                color = 'red4'
            contact_list.itemconfig(i, {'fg': color})


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def send_private():
    if recipient != "":
        print("def sendprivate():")
        sendmessage("/mschat/user/{0}/{1}".format(recipient, username), private_entry.get())
        private_chat.config(state=tk.NORMAL)
        private_chat.insert(tk.END, "TO: " + recipient + "\n" + private_entry.get() + "\n\n")
        private_chat.see(tk.END)
        private_chat.config(state=tk.DISABLED)


def send_public():
    print("def sendpublic():")
    sendmessage("/mschat/all/{0}".format(username), public_entry.get())


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


client = mqtt.Client(client_id="kvi0029")


def on_closing():
    if messagebox.askokcancel("Quit", "Click OK to disconnect and quit."):
        client.publish("/mschat/status/{0}".format(username), payload="offline", qos=0, retain=True)
        root.destroy()
        client.disconnect()


def select_contact():
    global recipient
    recipient = contact_list.get(contact_list.curselection()).split(":")[0]
    text_label.set("recipient: " + recipient)


def sendmessage(topic, message):
    timestamp = str(int(time.time()))
    client.publish(topic, payload=timestamp + ' ' + message, qos=0, retain=False)


root = tk.Tk()


root.protocol("WM_DELETE_WINDOW", on_closing)
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Public chat')
tab_control.add(tab2, text='Private messages')
tab_control.pack(expand=1, fill="both")

public_chat = ScrolledText(tab1)
private_chat = ScrolledText(tab2)
public_chat.grid(column=1, row=1, columnspan=2)
private_chat.grid(column=1, row=1, columnspan=2)
public_chat.config(state=tk.DISABLED)
private_chat.config(state=tk.DISABLED)

public_entry = tk.Entry(tab1)
private_entry = tk.Entry(tab2)
public_entry.grid(column=1, row=2)
private_entry.grid(column=1, row=2)

contact_list = tk.Listbox(tab2)
contact_list.grid(column=0, row=1)
contact_list.event_generate("<<ListboxSelect>>")
contact_list.bind("<<ListboxSelect>>", select_contact)

text_label = tk.StringVar()
name_label = tk.Label(tab2, textvariable=text_label)
name_label.grid(column=0, row=2)

tk.Button(tab1, text="Send!", command=send_public).grid(column=2, row=2)
private_send = tk.Button(tab2, text="Send!", command=send_private)
private_send.grid(column=2, row=2)

root.withdraw()

login = tk.Toplevel(root)
tk.Label(login, text="Enter username:").pack()
login_entry = tk.Entry(login)
login_entry.pack()


def login_init():
    global username
    global client
    root.deiconify()
    username = login_entry.get()
    client = mqtt.Client(client_id=username)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    if username == "":
        messagebox.showerror("Error", "Empty login field\nClosing process")
        sys.exit()
    else:
        client.will_set("/mschat/status/{0}".format(username), payload="offline", qos=0, retain=True)
        client.username_pw_set(username="mobilni", password="Systemy")
    client.connect("pcfeib425t.vsb.cz", 1883, 60)
    client.loop_start()
    login.destroy()
    root.title("MQTT pain | logged in as: {0}".format(username))


tk.Button(login, text="Log In", command=login_init).pack()

root.mainloop()
