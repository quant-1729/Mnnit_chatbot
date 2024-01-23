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

from selenium import webdriver
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
def open_google_maps_link(link):
    driver = webdriver.Chrome()
    driver.get(link)
    input("Press any key to close the browser...")
    driver.quit()
class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

class ActionSetHostelSlot(Action):
    def name(self) -> Text:
        return "action_set_hostel_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hostel_entry = next(tracker.get_latest_entity_values("requested_hostel"), None)

        if hostel_entry:
            dispatcher.utter_message(f"So, you want to dive into the life of {hostel_entry}")
            return [SlotSet("hostel", hostel_entry)]
        else:
            dispatcher.utter_message("I'm sorry, I didn't understand which hostel you mentioned.")
        return []

class ActionProvideDirections(Action):
    def name(self) -> Text:
        return "action_provide_directions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location_name = tracker.get_slot("user_location")
        destination_name = tracker.get_slot("destination_given")
        # location_name = tracker.get_latest_entity_values(user_location)
        # destination_name = tracker.get_latest_entity_values(destination_given)
        location_coordinates = {
            "Central Library": "25.49260751334134,81.86402110821898",
            "Admin Building": "25.493425551166336,81.86273379235345",
            "SVBH": "25.490837274599187,81.86274481076372",
            "Athletic Ground": "25.494390812450987,81.86448942334405",
            "Dean Academics": "25.492371007273704,81.86276909854777"
        }

        destination_coordinates = {
            "Central Library": "25.49260751334134,81.86402110821898",
            "Admin Building": "25.493425551166336,81.86273379235345",
            "SVBH": "25.490837274599187,81.86274481076372",
            "Athletic Ground": "25.494390812450987,81.86448942334405",
            "Dean Academics": "25.492371007273704,81.86276909854777"
        }

        if location_name in location_coordinates and destination_name in destination_coordinates:
            location_cords = location_coordinates[location_name]
            destination_cords = destination_coordinates[destination_name]

            map_url = f"https://www.google.com/maps/dir/?api=1&origin={location_cords}&destination={destination_cords}"

            dispatcher.utter_message(
                text=map_url
            )
            open_google_maps_link(map_url)
        else:
            dispatcher.utter_message("I couldn't find directions for the specified locations.")

        return []


class ActionOpenLink(Action):
    def name(self) -> Text:
        return "action_open_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Replace the URL with the link you want to open
        url_to_open = "http://www.mnnit.ac.in/"

        webbrowser.open(url_to_open)

        # You can customize the response sent back to the user
        dispatcher.utter_message(f"Opening the link: {url_to_open}")

        return []





class ActionFallback(Action):
    def name(self) -> Text:
        return "say_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message.get("text")
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5 engine
            prompt=user_input,
            max_tokens=50)

        fallback_response = response.choices[0].text.strip()
        dispatcher.utter_message(text=fallback_response)


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
