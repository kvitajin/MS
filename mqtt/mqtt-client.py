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
    if(username == "anon"):
        pass
    else:
        client.subscribe("/mschat/user/{0}/#".format(username))
        client.publish("/mschat/status/{0}".format(username), payload="online", qos=0, retain=True)

def on_message(client, userdata, msg):
    global contacts
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic.startswith("/mschat/all/")):
        publicchat.config(state=tk.NORMAL)
        publicchat.insert(tk.END, msg.topic[12:] + ": " + msg.payload.decode("utf-8").strip()+"\n")
        publicchat.see(tk.END)
        publicchat.config(state=tk.DISABLED)
    elif(msg.topic.startswith("/mschat/user/")):
        privatechat.config(state=tk.NORMAL)
        privatechat.insert(tk.END, "FROM: "+msg.topic[13:].split("/")[1]+"\n"+msg.payload.decode("utf-8").strip()+"\n\n")
        privatechat.see(tk.END)
        privatechat.config(state=tk.DISABLED)
    elif(msg.topic.startswith("/mschat/status/")):
        contacts[msg.topic[15:]] = msg.payload.decode("utf-8").strip()
        contactlist.delete(0, tk.END)
        for i,(k,v) in enumerate(contacts.items()):
            contactlist.insert(tk.END, k + ": " + v)
            color = 'black'
            if(v.lower()=='online'):
                color='dark green'
            elif(v.lower()=='offline'):
                color='red4'
            contactlist.itemconfig(i, {'fg':color})

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

client = mqtt.Client(client_id="sig0033")
#client.on_connect = on_connect
#client.on_message = on_message
#client.on_publish = on_publish
#client.on_subscribe = on_subscribe

#client.username_pw_set(username="mobilni", password="Systemy")
#client.connect("pcfeib425t.vsb.cz", 1883, 60)

#client.loop_forever()
#client.loop_start()

def on_closing():
    if messagebox.askokcancel("Quit", "Click OK to disconnect and quit."):
        if(username == "anon"):
            pass
        else:
            client.publish("/mschat/status/{0}".format(username), payload="offline", qos=0, retain=True)
        root.destroy()
        client.disconnect()

def contactselect(param):
    global recipient
    recipient = contactlist.get(contactlist.curselection()).split(":")[0]
    namelabeltext.set("recipient: "+recipient)

def sendmessage(topic, message):
    timestamp = str(int(time.time()))
    client.publish(topic, payload=timestamp+' '+message, qos=0, retain=False)

def sendpublic():
    print("def sendpublic():")
    sendmessage("/mschat/all/{0}".format(username), publicentry.get())

def sendprivate():
    if(recipient != ""):
        print("def sendprivate():")
        sendmessage("/mschat/user/{0}/{1}".format(recipient,username), privateentry.get())
        privatechat.config(state=tk.NORMAL)
        privatechat.insert(tk.END, "TO: "+recipient+"\n"+privateentry.get()+"\n\n")
        privatechat.see(tk.END)
        privatechat.config(state=tk.DISABLED)

root = tk.Tk()


root.protocol("WM_DELETE_WINDOW", on_closing)
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Verejny chat')
tabControl.add(tab2, text ='Privatni zpravy')
tabControl.pack(expand = 1, fill ="both")

publicchat = ScrolledText(tab1)
privatechat = ScrolledText(tab2)
publicchat.grid(column=1, row=1, columnspan=2)
privatechat.grid(column=1, row=1, columnspan=2)
publicchat.config(state=tk.DISABLED)
privatechat.config(state=tk.DISABLED)

publicentry = tk.Entry(tab1)
privateentry = tk.Entry(tab2)
publicentry.grid(column=1, row=2)
privateentry.grid(column=1, row=2)

contactlist = tk.Listbox(tab2)
contactlist.grid(column=0, row=1)
contactlist.event_generate("<<ListboxSelect>>")
contactlist.bind("<<ListboxSelect>>", contactselect)

namelabeltext = tk.StringVar()
namelabel=tk.Label(tab2, textvariable=namelabeltext)
namelabel.grid(column=0, row=2)

tk.Button(tab1, text="Send!", command=sendpublic).grid(column=2, row=2)
privatesend = tk.Button(tab2, text="Send!", command=sendprivate)
privatesend.grid(column=2, row=2)

root.withdraw()

login = tk.Toplevel(root)
tk.Label(login, text="Enter username:").pack()
loginentry = tk.Entry(login)
loginentry.pack()
def logininit():
    global username
    global client
    root.deiconify()
    username = loginentry.get()
    client = mqtt.Client(client_id=username)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    if(username == "anon"):
        privatesend.config(state=tk.DISABLED)
    elif(username == ""):
        messagebox.showerror("Error", "Empty login field\nClosing process")
        sys.exit()
    else:
        # Automatické nastavení informace o odpojení po výpadku klienta
        client.will_set("/mschat/status/{0}".format(username), payload="offline", qos=0, retain=True)
        client.username_pw_set(username="mobilni", password="Systemy")
    client.connect("pcfeib425t.vsb.cz", 1883, 60)
    client.loop_start()
    login.destroy()
    root.title("MQTT chat app by Filip Sigut | logged in as: {0}".format(username))
tk.Button(login, text="Log In", command=logininit).pack()


root.mainloop()