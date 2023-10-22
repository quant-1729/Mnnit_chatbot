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
#
class ActionSetHostelSlot(Action):

    def name(self) -> Text:
        return "action_Set_Hostel_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hostel_entry = next(tracker.get_latest_entity_values("requested_hostel"), None)
        hostel_informations = next(tacker.get_latest_response)
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
