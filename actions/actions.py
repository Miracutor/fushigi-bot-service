# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import sqlite3
# This is a simple example for a custom action which utters "Hello World!"
# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import re
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

databasePath = Path('.', 'knowledge', 'fushigi.db')
conn = sqlite3.connect(databasePath)


class ActionAnswerDirection(Action):

    def name(self) -> Text:
        return "action_answer_direction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cursor = conn.cursor()
        try:
            cursor.execute('select * from Direction')
            direction = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        place: str = next(tracker.get_latest_entity_values("place"), None)
        # print("Place: ["+place+"]")

        result = None
        for d in direction:
            d: tuple
            keyword: str = d[1]
            if place.lower() in keyword:
                result = d
                break

        if result is None:
            dispatcher.utter_message(text="Requested direction not recorded in the system.")
        else:
            message = "Sure! To go to {}, you need to {}".format(result[1].capitalize(), result[2])
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', message)
            for s in sentences:
                dispatcher.utter_message(s)

        return []


class ActionAnswerExplain(Action):

    def name(self) -> Text:
        return "action_answer_explain"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cursor = conn.cursor()
        try:
            cursor.execute('select * from Explain')
            explain = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        explain_subject: str = next(tracker.get_latest_entity_values("explain_subject"), None)
        # print("Explain: ["+explain_subject+"]")

        result = None
        for e in explain:
            e: tuple
            keyword: str = e[1]
            if explain_subject.lower() in keyword:
                result = e
                break

        dispatcher.utter_message(text=result[2])

        return []


class ActionAnswerInquiry(Action):

    def name(self) -> Text:
        return "action_answer_inquiry"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cursor = conn.cursor()
        try:
            cursor.execute('select * from Inquiry')
            inquiry = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        inquiry_subject: str = next(tracker.get_latest_entity_values("inquiry_subject"), None)
        # print("Inquiry: ["+inquiry_subject+"]")

        result = None
        for i in inquiry:
            i: tuple
            keyword: str = i[1]
            if inquiry_subject.lower() in keyword:
                result = i
                break

        dispatcher.utter_message(text=result[2])

        return []
