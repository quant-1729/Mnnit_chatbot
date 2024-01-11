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
from selenium import webdriver
import webbrowser
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