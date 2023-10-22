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
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet
#
# # from rasa_sdk.events import Slotset
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

#
class ActionSetHostelSlot(Action):

    def name(self) -> Text:
        return "action_Set_Hostel_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hostel_entry = next(tracker.get_latest_entity_values("requested_hostel"), None)
        hostel_informations = next(tracker.get_latest_response)
        utc = arrow.utcnow()
        file_path_DJ= f"Responses/DJ.txt"
        response_DJ = file_path_DJ.read()

        if hostel_entry is not None:
            dispatcher.utter_message(f"SO you want to dive in the life of {hostel_entry}", response_DJ)
            return [SlotSet("hostel", hostel_entry)]
        else:
            dispatcher.utter_message("I'm sorry, I didn't understand which hostel you mentioned.")
            return []
        return [SlotSet("hostel", hostel_entry)]

class ActionProvideDirections(Action):
    def name(self) -> Text:
        return "action_provide_directions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location_name = tracker.get_slot("Current_location")
        destination_name = tracker.get_slot("Destination")

        location_coordinates = {
            "Central Library": "25.49260751334134,81.86402110821898",
            "Admin Building": "25.493425551166336,81.86273379235345",
            "SVBH": "25.490837274599187, 81.86274481076372",
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
            location_coords = location_coordinates[location_name]
            destination_coords = destination_coordinates[destination_name]

            #Google Maps URL
            map_url = f"https://www.google.com/maps/dir/?api=1&origin={location_coords}&destination={destination_coords}"

            dispatcher.utter_message(
                response="utter_provide_directions",
                location=location_name,
                destination=destination_name,
                map_url=map_url
            )
        else:
            dispatcher.utter_message(
                response="utter_no_directions",
                location=location_name,
                destination=destination_name
            )

        return []