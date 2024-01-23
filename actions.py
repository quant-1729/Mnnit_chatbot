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
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# from selenium import webdriver  //
import pymongo
from datetime import datetime
import time
import sys
from bson import ObjectId
# import pyttsx3  //
import threading
# import openai  //
from rasa_sdk.events import Restarted
import logging
# def open_google_maps_link(link):  //
#     driver = webdriver.Chrome()   //
#     driver.get(link)             //
#     input("Press any key to close the browser...")    //
#     driver.quit()                       //
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

##### download the calender
## this action is currently not working
class ActionProvideDownloadLink(Action):
    def name(self) -> Text:
        return "action_academic_calendar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        file_path = 'calendar.ics'  
        download_link = f"file://{file_path}"

        response_message = f"You can download the academic calendar [here]({download_link})."

        
        dispatcher.utter_message(response_message)

        return []
        # def run(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any], ) -> List[Dict[Text, Any]]:

        
        # download_link = "your_download_link"
        # academic_calendar_path = "path_to_academic_calendar.pdf"

        
        # message = f"Sure! Here is the link to download the academic calendar: [{download_link}]({download_link})"
        
       
        # dispatcher.utter_message(text=message)

        # return []
    
current_time = datetime.now()
client = pymongo.MongoClient("mongodb://localhost:27017")
db= client["Trial_event_database"]
coll=db["Year_1"]
coll2 = db["user_data"]
DataBase = client['BotRush2k23']
BBSEColl = DataBase['Bumblesee(Line_followers)']
MNGEColl = DataBase['Match_ngage']
v_coll = DataBase["VoiceMode"]
logging.basicConfig(level=logging.INFO)
# openai.api_key = "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" //
# def text_to_speech(text):     //
#     engine = pyttsx3.init()   //
#     engine.say(text)          //
#     engine.runAndWait()       //

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
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        return[Restarted()]
    
# class RestartConvo(Action):
#     def name(self) -> Text:
#         return "restart_convo"

#     async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         try:
#             # Your action code here
#             logging.info("Action 'restart_convo' executed successfully.")
#             return []
#         except Exception as e:
#             logging.exception("Error in action 'restart_convo': %s", str(e))
#             return []
class say_events_(Action):

    def name(self) -> Text:
         return "action_say_events"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        found = coll.find_one({"EventDate":{"$gt":current_time}}, {"_id":0})
        event_name = found["EventName"]
        event_type = found["EventType"]
        event_start= found["StartTime"] 
        event_end = found["EndTime"]
        event_date = found["EventDate"]
        desired_format = "%Y-%m-%d"
        parsed_datetime = event_date.strftime(desired_format)
        datetime_object = datetime.strptime(parsed_datetime, "%Y-%m-%d")
        day_of_week_number = datetime_object.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        message = "The next event in the college is "+event_name+". It is a "+event_type+" event, from "+event_start+" to "+event_end+" on "+parsed_datetime+"("+days[day_of_week_number]+")"

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
        found = coll.find_one({"EventName": Eventnamevalue},{"_id":0})       
        if found is not None:
            link = found['GformLink']
            dispatcher.utter_message(text="You chose to register for "+Eventnamevalue+"\nHere is the google form link "+link)
            message = "You chose to register for "+Eventnamevalue+"\nHere is the google form link "+link
            if(v_coll.find_one({"_id":"voice_mode_on_off"})['Mode']=="ON"):
                    threading.Thread(target=text_to_speech, args=(message,)).start()
        else:
            message = "The Registration for "+Eventnamevalue+" has not begun yet"
            dispatcher.utter_message(text="The Registration for "+Eventnamevalue+" has not begun yet")

class giveUserEventLink(Action):
    def name(self) -> Text:
        return "say_bbsee_details"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query={"_id":"BumbeSee"}
        projection = {"Event_details":1}
        desc = BBSEColl.find_one({"_id":"SmartBot"})
        descip = desc["Details"]
        storage = BBSEColl.find(query,projection)
        for i in storage:
            event_details = i.get("Event_details", {})
            date=event_details.get("date")
            stime=event_details.get("start_time")
            loc=event_details.get("location")
        dispatcher.utter_message(text=descip+"\nIt is on "+date+" starts at "+stime+".\nLocation: "+loc)
class DecideArenaMember(Action):
    def name(self) -> Text:
        return "show_arena_map"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])
        boolMapEntity= next((entity for entity in entities if entity['entity'] == 'boolMap'), None)
        descQuery ={"_id":"Arena_Desc"}
        descProjection = {"Line_following":1,"Wall_following":1}
        store_desc_data = BBSEColl.find(descQuery,descProjection)
        for i in store_desc_data:
            LineFollow = i.get("Line_following",{})
            WallFollow = i.get("Wall_following",{})
            LineDesc = LineFollow.get("description")
            WallDesc = WallFollow.get("description")
        if boolMapEntity is not None:
            boolMapValue = str(boolMapEntity['value'])
            mapObject=BBSEColl.find_one({"_id":"Arena_Map"})
            mapURL = mapObject['URL']
            dispatcher.utter_message(text="Sure! Here is a map of the arena\n"+mapURL)
        else:
            message = "For Line following event, "+LineDesc+"\nFor the Wall following event, "+WallDesc
            dispatcher.utter_message(text="For Line following event, "+LineDesc+"\nFor the Wall following event, "+WallDesc)

class DetailsBBSE(Action):
    def name(self) -> Text:
        return "decide_details"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])
        SpecDetails = next((entity for entity in entities if entity['entity'] == 'SpecificDetail_BBSE'), None)
        DetailType = str(SpecDetails['value'])
        if(DetailType == "AllRules"):
            query={"_id":"Rules"}
            ruledocument = BBSEColl.find_one(query)
            rdlen = len(ruledocument)
            for c in range(0,rdlen-1):
                message = "Rule "+str(c+1)+":"+(BBSEColl.find_one(query))['R'+str(c+1)]+"\n"
                dispatcher.utter_message(("Rule "+str(c+1)+":"+(BBSEColl.find_one(query))['R'+str(c+1)]+"\n"))
                c=c+1
            return[]
        elif (DetailType =="Game_Play"):
            query = {"_id":"Game_Play"}
            projection ={"_id":0,"instructions.start_to_D.action":0,"instructions.D_to_end.action":0}
            GPdoc= BBSEColl.find_one(query,projection)
            s_to_d_desc=GPdoc.get("instructions",{}).get("start_to_D",{}).get("description",{})
            d_to_end_desc = GPdoc.get("instructions",{}).get("D_to_end",{}).get("description",{})
            message = "Here are the Gamepy Guides provided by the coordinators:\n"+s_to_d_desc+"\n"+d_to_end_desc
            dispatcher.utter_message(text="Here are the Gamepy Guides provided by the coordinators:\n"+s_to_d_desc+"\n"+d_to_end_desc)
            return[]
        elif DetailType=="REG":
            query = {"_id":"REG"}
            regdocument = BBSEColl.find_one(query)
            reglen = len(regdocument)
            for c in range(0,reglen-1):
                message = str(c+1)+":"+(BBSEColl.find_one(query))[str(c+1)]+"\n"
                dispatcher.utter_message((str(c+1)+":"+(BBSEColl.find_one(query))[str(c+1)]+"\n"))
                c=c+1
        elif DetailType=="BotSpec":
            query = {"_id":"Bot Specifications"}
            regdocument = BBSEColl.find_one(query)
            reglen = len(regdocument)
            for c in range(0,reglen-1):
                message = str(c+1)+":"+(BBSEColl.find_one(query))[str(c+1)]+"\n"
                dispatcher.utter_message((str(c+1)+":"+(BBSEColl.find_one(query))[str(c+1)]+"\n"))
                c=c+1
        elif DetailType=="BotComp":
            query = {"_id":"Bot Components"}
            regdocument = BBSEColl.find_one(query)
            reglen = len(regdocument)
            for c in range(0,reglen-1):
                message = str(c+1)+":"+(BBSEColl.find_one(query))[str(c+1)]+"\n"
                dispatcher.utter_message((str(c+1)+":"+(BBSEColl.find_one(query))[str(c+1)]+"\n"))
                c=c+1
        elif DetailType.isnumeric() == True:
            if(int(DetailType) in range(1,len(BBSEColl.find_one({"_id":"Rules"})))):
                query={"_id":"Rules"}
                ruledoc=(BBSEColl.find_one(query))["R"+str(DetailType)]
                message = "According to Rule "+DetailType+"\n"+str(ruledoc)
                dispatcher.utter_message("According to Rule "+DetailType+"\n"+str(ruledoc))
                return[]
            else:
                message = "Sorry that rule doesn't exist it seems"
                dispatcher.utter_message("Sorry that rule doesn't exist it seems")

        elif DetailType == "Penalty" or DetailType == "Marking_Scheme":
            GPdoc = BBSEColl.find_one({"_id":"Marking_Scheme"})
            if(DetailType == "Penalty"):
                message = "The number of seconds your bot takes to complete the arena, will be deducted from your final scoring"
                dispatcher.utter_message("The number of seconds your bot takes to complete the arena, will be deducted from your final scoring")

            else:
                A_to_B = str(GPdoc.get("checkpoints_points",{}).get("A_to_B",{}))
                B_to_C = str(GPdoc.get("checkpoints_points",{}).get("B_to_C",{}))
                C_to_D = str(GPdoc.get("checkpoints_points",{}).get("C_to_D",{}))
                D_to_END = str(GPdoc.get("checkpoints_points",{}).get("D_to_END",{}))
                message = "From A to B:"+A_to_B+"points. \nFrom B to C:"+B_to_C+"points. \nC to D:"+C_to_D+"points. \nD to Finish Line:"+D_to_END+"points."
                
                dispatcher.utter_message(text="From A to B:"+A_to_B+"points. \nFrom B to C:"+B_to_C+"points. \nC to D:"+C_to_D+"points. \nD to Finish Line:"+D_to_END+"points.")