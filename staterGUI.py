import customtkinter
import tkinter as tk
import tkinter
import requests
from termcolor import colored
import sys
import time , pymongo

client = pymongo.MongoClient("mongodb+srv://Derik714:Hrithiman1856@cluster0.c5z73yl.mongodb.net/")
database = client['Chat_history']
coll2023 = database['Chat_History_2023']
app = customtkinter.CTk()
app.geometry("1920x1080")
app.title("Mnnit_ChatBOT")
rasa_server_url = "http://localhost:5055/webhook"
conversationid = "default"
chat_count = 0
save_chat = True
chat_header = ""


def LoadChatHistory(header):
    Output_box.configure(state='normal')
    Output_box.delete(0.0, "end")
    doc = coll2023.find_one({'id': header}, {"id": 0})
    Output_box.configure(state='disabled')
    if doc is not None:
        l = int(len(doc.get("convo", {})) / 2)
        for i in range(0, l):
            user_message = str(doc.get("convo", {}).get(str(i), {}))
            response_message = str(doc.get("convo", {}).get(str(i) + "r", {}))
            Output_box.tag_config("1", foreground="Yellow")
            Output_box.tag_config("2", foreground="green")
            Output_box.configure(state='normal')
            Output_box.insert(tkinter.END, "You->")
            Output_box.insert(tkinter.END, user_message + "\n", "1")
            Output_box.insert(tkinter.END, "RASA-> ")
            Output_box.insert(tkinter.END, response_message + "\n", "2")
            Output_box.configure(state='disabled')


def clearChat():
    global save_chat, chat_count
    Output_box.configure(state='normal')
    Output_box.delete(0.0, "end")
    Output_box.configure(state='disabled')
    save_chat = True
    chat_count = 0


def GetandDisplayResponse():
    text = input_box.get()
    input_box.delete(0, "end")
    user_message = text
    global save_chat, chat_count, chat_header
    Output_box.configure(state='normal')
    Output_box.tag_config("1", foreground="Yellow")
    Output_box.tag_config("2", foreground="green")
    user_input_url = f"{rasa_server_url}/webhooks/rest/webhook"
    payload = {
        "sender": conversationid,
        "message": user_message
    }
    Output_box.insert(tkinter.END, "You->")
    Output_box.insert(tkinter.END, user_message + "\n", "1")
    Output_box.insert(tkinter.END, "RASA-> ")
    response = requests.post(user_input_url, json=payload)
    bot_responses = response.json()
    response_message = ""
    for bot_response in bot_responses:
        bot_response['text'] = bot_response['text'] + "\n"
        for i in bot_response['text']:
            Output_box.insert(tkinter.END, i, "2")
            response_message += i
    user_question = user_message
    if save_chat == True:

        chat_header = user_message[:15] + "..."
        hist = customtkinter.CTkButton(master=side_panel, text=user_message[:20] + "...", font=("Comic Sans MS", 16),
                                       fg_color="#333333", command=lambda header=chat_header: LoadChatHistory(header))
        hist.pack(fill="x", pady=10)
        doc = {"id": chat_header, "convo": {str(chat_count): user_question, str(chat_count) + "r": response_message}}
        coll2023.insert_one(doc)
        save_chat = False
        chat_count = chat_count + 1
    else:

        update = {
            "$set": {
                "convo." + str(chat_count): user_message,
                "convo." + str(chat_count) + "r": response_message
            }
        }

        filter_doc = {"id": chat_header}
        chat_count = chat_count + 1
        coll2023.update_one(filter_doc, update)

    Output_box.configure(state='disabled')


welcome_box = customtkinter.CTkLabel(master=app, text="""Welcome to Mnnit_ChatBOT, your  MNNIT Information Companion!

Mnnit_ChatBOT is your go-to chatbot for all things including  essential general information about Motilal Nehru National Institute of Technology (MNNIT). Whether you're a curious alumnus looking for the latest GAC updates or someone interested in learning about MNNIT, I'm here to provide you with the knowledge you seek.

Feel free to inquire about the event schedule, speakers, activities, or any details regarding our College. Additionally, if you have questions about MNNIT's campus, academic programs, or student life, I've got you covered.

Just type your queries or topics of interest, and I'll ensure you receive accurate and up-to-date information. Mnnit_ChatBOT is your virtual guide, ready to assist and inform, bridging the gap between alumni and the institution that holds a special place in your heart. Let's embark on this journey of knowledge and nostalgia together!
""", font=("Comic Sans MS", 14), width=120, height=25, corner_radius=8, wraplength=1200, text_color=("#BF9553"))
welcome_box.place(relx=0.57, rely=0.15, anchor=tkinter.CENTER)
input_box = customtkinter.CTkEntry(master=app, justify="center", width=1000, placeholder_text="Your input message here",
                                   font=("Comic Sans MS", 14))
input_box.place(relx=0.57, rely=0.3, anchor=tkinter.CENTER)
side_panel = customtkinter.CTkScrollableFrame(app, width=250, bg_color="#333333", fg_color="#333333")
side_panel.pack(fill="y", side="left")

banner = tkinter.Label(side_panel, text="MNNIT ROBOTICS CLUB", font=("Comic Sans MS", 16), bg="#333333", fg="white",
                       padx=10, pady=30)
banner.pack(fill="x")
submit_button = customtkinter.CTkButton(master=app, width=80, text="Submit", font=("Comic Sans MS", 15),
                                        command=GetandDisplayResponse)
submit_button.place(relx=0.57, rely=0.35, anchor=tkinter.CENTER)
Output_box = customtkinter.CTkTextbox(master=app, width=1000, corner_radius=30, border_spacing=1, height=450,
                                      font=("Comic Sans MS", 16), fg_color="#333333")
Output_box.place(relx=0.57, rely=0.66, anchor=tkinter.CENTER)
Output_box.configure(state='disabled')
clear_button = customtkinter.CTkButton(master=app, width=45, text="Clear Chat", font=("Comic Sans MS", 10),
                                       command=clearChat)
clear_button.place(relx=0.27, rely=0.95, anchor=tkinter.CENTER)
app.mainloop()