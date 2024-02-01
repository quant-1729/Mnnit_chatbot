# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# from typing import List, Dict, Text, Any
#
# from anaconda_navigator.api.external_apps.config_utils import Action
# from anaconda_navigator.external.UniversalAnalytics.Tracker import Tracker
# This is a simple example for a custom action which utters "Hello World!"

# from selenium import webdriver
# from spellchecker import SpellChecker
import webbrowser
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted, SlotSet
import pymongo
from datetime import datetime
import time
import sys
import random
from bson import ObjectId
import openai
from gtts import gTTS
from playsound import playsound



#Action for text to voice comversion

class ActionTextToSpeech(Action):
    def name(self) -> Text:
        return "action_text_to_speech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve the text from the latest user message
        # Retrieve the text from the last utterance
        last_user_message = tracker.latest_message.get('text', '')


        # Generate TTS audio from the response text
        tts = gTTS(text=last_user_message, lang='en')
        # Generate TTS audio from the user's text


        # Save the generated audio file
        audio_path = "Audio_response/output.mp3"
        tts.save(audio_path)

        # Play the generated audio
        playsound(audio_path)

        return []

client = pymongo.MongoClient("mongodb+srv://Derik714:Hrithiman1856@cluster0.c5z73yl.mongodb.net/")
DataBase = client['GACData']
coll1 = DataBase['GAC2023']
openai.api_key = "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"
# open Ai integration

def run(
    self,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
) -> List[Dict[Text, Any]]:

# Get user message from Rasa tracker
    user_message = tracker.latest_message.get('text')
    print(user_message)
# def get_chatgpt_response(self, message):
#     url = ' '
#     headers = {
#         'Authorization': 'fNzyk5rxfzkEn922GEGCT3BlbkFJbtbnaO9w9vGn1HAxbzVZ',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'model': "gpt-3.5-turbo",
#         'messages': [   {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user query'},
#                         {'role': 'user', 'content': 'You: ' + user_message}
#                         ],
#         'max_tokens': 100
#     }
#     response = requests.post(url, headers=headers, json=data)
#     # response = requests.post(api_url, headers=headers, json=data)
#
#     if response.status_code == 200:
#         chatgpt_response = response.json()
#         message = chatgpt_response['choices'][0]['message']['content']
#         dispatcher.utter_message(message)
#     else:
#         # Handle error
#         return "Sorry, I couldn't generate a response at the moment. Please try again later."
#
#         # Revert user message which led to fallback.
#     return [UserUtteranceReverted()]
# def open_google_maps_link(link):
#
#     driver = webdriver.Chrome()
#     driver.get(link)
#     input("Press any key to close the browser...")
#     driver.quit()
class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

class ActionProvideDirections(Action):
    def name(self) -> Text:
        return "action_provide_directions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location_name = "mnnit + "+tracker.get_slot("user_location")
        destination_name = "mnnit + "+tracker.get_slot("destination_given")


        link = f"https://www.google.com/maps/dir/?api=1&origin={location_name}&destination={destination_name}"
        dispatcher.utter_message(f"click on this link pls .. {link}")

        return []


class ActionOpenLink(Action):
    def name(self) -> Text:
        return "action_open_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Replace the URL with the link you want to open
        url_to_open = "http://www.mnnit.ac.in/"

        # You can customize the response sent back to the user
        dispatcher.utter_message(f"Opening the link: {url_to_open}")

        return []




def contains_mnnit_nit_mnit(sentence):
    target_words = ["mnnit", "nit", "mnit","nnit","nit mnnit"]
    words = sentence.split()
    for word in words:
        if word.lower() in target_words:
            return True
    return False
class ActionFallback(Action):
    def name(self) -> Text:
        return "say_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text")
        # response = openai.Completion.create(
        #     engine="text-davinci-003",  # GPT-3.5 engine
        #     prompt=user_input,
        #     max_tokens=50)
        inputLen=len(user_input.split());

        if(inputLen<4):
            dispatcher.utter_message("Please provide more data");
        elif contains_mnnit_nit_mnit(user_input):
            dispatcher.utter_message("Sorry this data is not currently in my data")
        else:
            dispatcher.utter_message("pls serach only for mnnnit college and bot rush i query i only meant for these. Sorry for inconvience")

class ActionProvideDirection(Action):
    def name(self) -> Text:
        return "action_give_direction"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text")
        destination= 'mnnit+'+ user_input.replace(" ","+");
        google_maps_link = f"https://www.google.com/maps/dir/?api=1&destination={destination}"
        dispatcher.utter_message(text=f"pls click on this {google_maps_link}")



class ConvoRestart(Action):
    def name(self) -> Text:
        return "restart_convo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [Restarted()]


class GAC2023(Action):
    def name(self) -> Text:
        return "gac2023_basic_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DetailType = ""
        entities = tracker.latest_message.get('entities', [])
        SpecDetails = next((entity for entity in entities if entity['entity'] == 'general_info'), None)
        if SpecDetails is not None:
            DetailType = str(SpecDetails['value'])
        else:
            dispatcher.utter_message("Sorry, but can you please elaborate the question?")
        if (DetailType == "L"):
            ChoiceNum = random.randint(1, 3)
            if (ChoiceNum == 1):
                dispatcher.utter_message(
                    "The Global Alumni Convention is going to be held in the Multi-Purpose Hall of MNNIT, also known as the MP hall")
            elif (ChoiceNum == 2):
                dispatcher.utter_message(
                    "GAC 2023 is going to be held in the institute's MP hall, also called the Multi Purpose hall")
            else:
                dispatcher.utter_message(
                    "The Alumni Convention 2023 is going to be conducted in the Multi Purpose hall of MNNIT")
        elif (DetailType == "DESC"):
            ChoiceNum = random.randint(1, 4)
            if (ChoiceNum == 1):
                doc = coll1.find_one({"id": "DESC"}, {"_id": 0})
                desc2023 = doc.get("desc1", {})
                dispatcher.utter_message(desc2023)
            elif (ChoiceNum == 2):
                doc = coll1.find_one({"id": "DESC"}, {"_id": 0})
                desc2023 = doc.get("desc2", {})
                dispatcher.utter_message(desc2023)
            else:
                doc = coll1.find_one({"id": "DESC"}, {"_id": 0})
                desc2023 = doc.get("desc3", {})
                dispatcher.utter_message(desc2023)
        elif (DetailType == "DL"):
            ChoiceNum = random.randint(1, 3)
            if (ChoiceNum == 1):
                dispatcher.utter_message(
                    "GAC 2023 is going to be held in the MP Hall of MNNIT, from 8 a.m November 4(Saturday) to 3 p.m November 5(Sunday)")
            elif (ChoiceNum == 2):
                dispatcher.utter_message(
                    "GAC 2023 is scheduled to take place at the MP Hall of MNNIT, and it will run from 8 a.m. on Saturday, November 4th, to 3 p.m. on Sunday, November 5th.")
            else:
                dispatcher.utter_message(
                    "Global Alumni Convention 2023 is scheduled to take place at the MP Hall of MNNIT, and it will run from 8 a.m. on Saturday, November 4th, to 3 p.m. on Sunday, November 5th.")
        elif (DetailType == "S"):
            ChoiceNum = random.randint(1, 3)

            if (ChoiceNum == 1):
                dispatcher.utter_message(
                    "Here is the detailed Schedule of GAC 2023: https://vaave.s3.amazonaws.com/attachments/1687341441_677f9c1773f98a424dde65c1c0563f2e.pdf")

            elif (ChoiceNum == 2):
                dispatcher.utter_message(
                    "You can find the event schedules of GAC 2023 following this link: https://vaave.s3.amazonaws.com/attachments/1687341441_677f9c1773f98a424dde65c1c0563f2e.pdf")
            else:
                dispatcher.utter_message(
                    "This is the link to the event schedule page: https://vaave.s3.amazonaws.com/attachments/1687341441_677f9c1773f98a424dde65c1c0563f2e.pdf")

        else:
            ChoiceNum = random.randint(1, 3)
            if (ChoiceNum == 1):
                dispatcher.utter_message(
                    "The Global Alumni Convention is going to be held in the Multi-Purpose Hall of MNNIT, also known as the MP hall")
            elif (ChoiceNum == 2):
                dispatcher.utter_message(
                    "GAC 2023 is going to be held in the institute's MP hall, also called the Multi Purpose hall")
            else:
                dispatcher.utter_message(
                    "The Alumni Convention 2023 is going to be conducted in the Multi Purpose hall of MNNIT")


class ConvoRestart(Action):
    def name(self) -> Text:
        return "gac2023_orgcom"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DetailType = ""
        entities = tracker.latest_message.get('entities', [])
        SpecDetails = next((entity for entity in entities if entity['entity'] == 'gacorg'), None)
        if SpecDetails is not None:
            DetailType = str(SpecDetails['value'])
        else:
            dispatcher.utter_message("Sorry, but can you please elaborate the question?")
        identifiers = ["CoChair", "oSec", "Tres", "Jsec", "chair", "Ad", "Pat"]
        if DetailType not in identifiers:
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"_id": 0})
            for i in doc:
                dispatcher.utter_message("Here is the list of members from the Organising Committee")
                dispatcher.utter_message(i + ":" + str(doc.get(i, {})))
        elif DetailType == "CoChair":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Co-Chairman", {})
            dispatcher.utter_message("The Co-Chairman of the event is, " + str(Name))
        elif DetailType == "oSec":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Org.Secretary", {})
            dispatcher.utter_message("The Organising Secretary of the event is, " + str(Name))
        elif DetailType == "Tres":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Treasurer", {})
            dispatcher.utter_message("The Treasurer of the event is, " + str(Name))
        elif DetailType == "Jsec":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Joint Org.Secretaries", {})
            dispatcher.utter_message("The Co-Chairman of the event is, " + str(Name))
        elif DetailType == "chair":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Chairman", {})
            dispatcher.utter_message("The Chairman of the event is, " + str(Name))
        elif DetailType == "Ad":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Advisor", {})
            dispatcher.utter_message("The Advisor of the event is, " + str(Name))
        elif DetailType == "Pat":
            query = {"id": "OrgComm"}
            doc = coll1.find_one(query, {"id": 0})
            Name = doc.get("Patron", {})
            dispatcher.utter_message("The Patron of the event is, " + str(Name))


class ConvoRestart(Action):
    def name(self) -> Text:
        return "gac_reg"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DetailType = ""
        entities = tracker.latest_message.get('entities', [])
        SpecDetails = next((entity for entity in entities if entity['entity'] == 'gacreg'), None)
        if SpecDetails is not None:
            DetailType = str(SpecDetails['value'])
        else:
            dispatcher.utter_message("Sorry, but can you please elaborate the question?")
        if DetailType == "FR" or DetailType == "RL":
            ChoiceNum = random.randint(1, 4)
            if ChoiceNum == 1:
                dispatcher.utter_message(
                    "You can register for GAC 2023, on this link:https://alumni.mnnit.ac.in/easysignup/register/event/278773.dz")
            elif ChoiceNum == 2:
                dispatcher.utter_message(
                    "You can register on this link, https://alumni.mnnit.ac.in/easysignup/register/event/278773.dz")
            else:
                dispatcher.utter_message(
                    "This is the link for registration, https://alumni.mnnit.ac.in/easysignup/register/event/278773.dz")
        elif DetailType == "FO":
            ChoiceNum = random.randint(1, 3)
            if ChoiceNum == 1:
                dispatcher.utter_message("The fee amount for non-felicitated batches is,₹5,000 ")
            elif ChoiceNum == 2:
                dispatcher.utter_message(
                    "As a token of our appreciation for those not in the felicitated batches, the fee is a humble ₹5,000")
            else:
                dispatcher.utter_message(
                    "For our cherished alumni in the non-felicitated batches, the fee is a mere ₹5,000, reflecting our gratitude for your continued support")
        elif DetailType == "FF":
            ChoiceNum = random.randint(1, 3)
            if ChoiceNum == 1:
                dispatcher.utter_message("The fee amount for felicitated batches is,₹7,500 ")
            elif ChoiceNum == 2:
                dispatcher.utter_message(
                    "As a heartfelt gesture to our celebrated alumni in the felicitated batches, the fee is set at ₹7,500, a sincere reflection of our admiration for your outstanding accomplishments")
            else:
                dispatcher.utter_message(
                    "For our cherished alumni in the felicitated batches, the fee is a mere ₹7,500, reflecting our gratitude for your continued support")
        elif DetailType == "F":
            ChoiceNum = random.randint(1, 3)
            if ChoiceNum == 1:
                dispatcher.utter_message(
                    "You can find the complete fee details for GAC 2023, a warm and welcoming event, by visiting this link:https://vaave.s3.amazonaws.com/attachments/1694691512_ddad0639613188f276576af5d6e44f35.png")
            elif ChoiceNum == 2:
                dispatcher.utter_message(
                    "Discover the full fee details for GAC 2023, a gathering filled with heartwarming moments, at this link: https://vaave.s3.amazonaws.com/attachments/1694691512_ddad0639613188f276576af5d6e44f35.png.")
            else:
                dispatcher.utter_message(
                    "The comprehensive fee information for GAC 2023, a celebration of our cherished alumni, can be found here: https://vaave.s3.amazonaws.com/attachments/1694691512_ddad0639613188f276576af5d6e44f35.png")
        elif DetailType == "RD":
            ChoiceNum = random.randint(1, 3)
            if ChoiceNum == 1:
                dispatcher.utter_message(
                    "Our heartwarming journey together has already begun, and we're excited to let you know that registration for this special event is now open. The last date to join us is November 3rd, so please don't miss out on being part of this memorable occasion")
            elif ChoiceNum == 2:
                dispatcher.utter_message(
                    "We're thrilled to announce that our registration process is in full swing, and we can't wait to welcome you. The deadline for registration is November 3rd, so we hope to see you there, creating beautiful memories together")
            else:
                dispatcher.utter_message(
                    "It's a joyous moment for us as registration for this event has officially started. We're looking forward to having you join us, and remember, the last day to register is November 3rd. Let's make this event an unforgettable experience together.")
###################################################################
###################################################################
################## BOT RUSH actions
class say_events_(Action):

    def name(self) -> Text:
        return "action_say_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        found = coll.find_one({"EventDate": {"$gt": current_time}}, {"_id": 0})
        event_name = found["EventName"]
        event_type = found["EventType"]
        event_start = found["StartTime"]
        event_end = found["EndTime"]
        event_date = found["EventDate"]
        desired_format = "%Y-%m-%d"
        parsed_datetime = event_date.strftime(desired_format)
        datetime_object = datetime.strptime(parsed_datetime, "%Y-%m-%d")
        day_of_week_number = datetime_object.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        message = "The next event in the college is " + event_name + ". It is a " + event_type + " event, from " + event_start + " to " + event_end + " on " + parsed_datetime + "(" + \
                  days[day_of_week_number] + ")"

        dispatcher.utter_message(text=message)
        return []


class giveUserEventLink(Action):
    def name(self) -> Text:
        return "action_givegformlink"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])
        Eventname = next((entity for entity in entities if entity['entity'] == 'eventname'), None)
        Eventnamevalue = str(Eventname['value'])
        found = coll.find_one({"EventName": Eventnamevalue}, {"_id": 0})
        if found is not None:
            link = found['GformLink']
            dispatcher.utter_message(
                text="You chose to register for " + Eventnamevalue + "\nHere is the google form link " + link)
            message = "You chose to register for " + Eventnamevalue + "\nHere is the google form link " + link
            if (v_coll.find_one({"_id": "voice_mode_on_off"})['Mode'] == "ON"):
                threading.Thread(target=text_to_speech, args=(message,)).start()
        else:
            message = "The Registration for " + Eventnamevalue + " has not begun yet"
            dispatcher.utter_message(text="The Registration for " + Eventnamevalue + " has not begun yet")


class giveUserEventLink(Action):
    def name(self) -> Text:
        return "say_bbsee_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = {"_id": "BumbeSee"}
        projection = {"Event_details": 1}
        desc = BBSEColl.find_one({"_id": "SmartBot"})
        descip = desc["Details"]
        storage = BBSEColl.find(query, projection)
        for i in storage:
            event_details = i.get("Event_details", {})
            date = event_details.get("date")
            stime = event_details.get("start_time")
            loc = event_details.get("location")
        dispatcher.utter_message(text=descip + "\nIt is on " + date + " starts at " + stime + ".\nLocation: " + loc)


class DecideArenaMember(Action):
    def name(self) -> Text:
        return "show_arena_map"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        descQuery = {"_id": "Arena_Desc"}
        descProjection = {"Line_following": 1, "Wall_following": 1}
        store_desc_data = BBSEColl.find(descQuery, descProjection)
        for i in store_desc_data:
            LineFollow = i.get("Line_following", {})
            WallFollow = i.get("Wall_following", {})
            LineDesc = LineFollow.get("description")
            WallDesc = WallFollow.get("description")
        message = "For Line following event, " + LineDesc + "\nFor the Wall following event, " + WallDesc
        dispatcher.utter_message(text=message)


class DetailsBBSE(Action):
    def name(self) -> Text:
        return "decide_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])
        SpecDetails = next((entity for entity in entities if entity['entity'] == 'SpecificDetail_BBSE'), None)
        DetailType = str(SpecDetails['value'])
        if (DetailType == "AllRules"):
            query = {"_id": "Rules"}
            ruledocument = BBSEColl.find_one(query)
            rdlen = len(ruledocument)
            for c in range(0, rdlen - 1):
                message = "Rule " + str(c + 1) + ":" + (BBSEColl.find_one(query))['R' + str(c + 1)] + "\n"
                dispatcher.utter_message(
                    ("Rule " + str(c + 1) + ":" + (BBSEColl.find_one(query))['R' + str(c + 1)] + "\n"))
                c = c + 1
            return []
        elif (DetailType == "Game_Play"):
            query = {"_id": "Game_Play"}
            projection = {"_id": 0, "instructions.start_to_D.action": 0, "instructions.D_to_end.action": 0}
            GPdoc = BBSEColl.find_one(query, projection)
            s_to_d_desc = GPdoc.get("instructions", {}).get("start_to_D", {}).get("description", {})
            d_to_end_desc = GPdoc.get("instructions", {}).get("D_to_end", {}).get("description", {})
            message = "Here are the Gamepy Guides provided by the coordinators:\n" + s_to_d_desc + "\n" + d_to_end_desc
            dispatcher.utter_message(
                text="Here are the Gamepy Guides provided by the coordinators:\n" + s_to_d_desc + "\n" + d_to_end_desc)
            return []
        elif DetailType == "REG":
            query = {"_id": "REG"}
            regdocument = BBSEColl.find_one(query)
            reglen = len(regdocument)
            for c in range(0, reglen - 1):
                message = str(c + 1) + ":" + (BBSEColl.find_one(query))[str(c + 1)] + "\n"
                dispatcher.utter_message((str(c + 1) + ":" + (BBSEColl.find_one(query))[str(c + 1)] + "\n"))
                c = c + 1
        elif DetailType == "BotSpec":
            query = {"_id": "Bot Specifications"}
            regdocument = BBSEColl.find_one(query)
            reglen = len(regdocument)
            for c in range(0, reglen - 1):
                message = str(c + 1) + ":" + (BBSEColl.find_one(query))[str(c + 1)] + "\n"
                dispatcher.utter_message((str(c + 1) + ":" + (BBSEColl.find_one(query))[str(c + 1)] + "\n"))
                c = c + 1
        elif DetailType == "BotComp":
            query = {"_id": "Bot Components"}
            regdocument = BBSEColl.find_one(query)
            reglen = len(regdocument)
            for c in range(0, reglen - 1):
                message = str(c + 1) + ":" + (BBSEColl.find_one(query))[str(c + 1)] + "\n"
                dispatcher.utter_message((str(c + 1) + ":" + (BBSEColl.find_one(query))[str(c + 1)] + "\n"))
                c = c + 1
        elif DetailType.isnumeric() == True:
            if (int(DetailType) in range(1, len(BBSEColl.find_one({"_id": "Rules"})))):
                query = {"_id": "Rules"}
                ruledoc = (BBSEColl.find_one(query))["R" + str(DetailType)]
                message = "According to Rule " + DetailType + "\n" + str(ruledoc)
                dispatcher.utter_message("According to Rule " + DetailType + "\n" + str(ruledoc))
                return []
            else:
                message = "Sorry that rule doesn't exist it seems"
                dispatcher.utter_message("Sorry that rule doesn't exist it seems")

        elif DetailType == "Penalty" or DetailType == "Marking_Scheme":
            GPdoc = BBSEColl.find_one({"_id": "Marking_Scheme"})
            if (DetailType == "Penalty"):
                message = "The number of seconds your bot takes to complete the arena, will be deducted from your final scoring"
                dispatcher.utter_message(
                    "The number of seconds your bot takes to complete the arena, will be deducted from your final scoring")

            else:
                A_to_B = str(GPdoc.get("checkpoints_points", {}).get("A_to_B", {}))
                B_to_C = str(GPdoc.get("checkpoints_points", {}).get("B_to_C", {}))
                C_to_D = str(GPdoc.get("checkpoints_points", {}).get("C_to_D", {}))
                D_to_END = str(GPdoc.get("checkpoints_points", {}).get("D_to_END", {}))
                message = "From A to B:" + A_to_B + "points. \nFrom B to C:" + B_to_C + "points. \nC to D:" + C_to_D + "points. \nD to Finish Line:" + D_to_END + "points."

                dispatcher.utter_message(
                    text="From A to B:" + A_to_B + "points. \nFrom B to C:" + B_to_C + "points. \nC to D:" + C_to_D + "points. \nD to Finish Line:" + D_to_END + "points.")