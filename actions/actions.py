# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import List, Dict, Text, Any

from anaconda_navigator.api.external_apps.config_utils import Action
from anaconda_navigator.external.UniversalAnalytics.Tracker import Tracker




# This is a simple example for a custom action which utters "Hello World!"

 from typing import Any, Text, Dict, List

 from rasa_sdk import Action, Tracker
 from rasa_sdk.executor import CollectingDispatcher



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
# class FormDataCollect(FormAction):


