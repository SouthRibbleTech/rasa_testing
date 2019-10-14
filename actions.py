# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

from elasticsearch import Elasticsearch
import json

class ActionGetForecast(Action):

    def name(self) -> Text:
        return "action_get_forecast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        partnumber = tracker.get_slot("partnumber")
        forecastRaw = requests.get(
            'http://localhost:3333/api/v1/forecast/earliest/' + partnumber)

        if forecastRaw.status_code == 200:
            forecast = forecastRaw.json()["forecast"]
            qty = str(forecastRaw.json()['qty'])
            dispatcher.utter_message("The next delivery for " + partnumber +
                                     " is for a qty of " + qty + ", the current forecast is " + forecast)
        else:
            dispatcher.utter_message(
                "Sorry, I could not find item " + partnumber)
        return []

class ActionExportControl(Action):
    def name(self) -> Text:
        return "action_export_control"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # userMessage = json.loads(tracker.latest_message)
        print(tracker.latest_message)
        print(tracker.latest_message['text'])
        es = Elasticsearch(['localhost'],
                           http_auth=('elastic', 'changeme')
                           )
        search_results = es.search(index='export_control',
                                   body={
                                       "query": {
                                           "query_string": {
                                               "query": tracker.latest_message['text']
                                           }
                                       },
                                       "highlight": {
                                           "fields": {
                                               "content": {"fragmenter": "span", "type": "fvh", "boundary_scanner": "sentence", "number_of_fragments": 3, "order": "score", "fragment_size": 500, "boundary_max_scan": 10}
                                           }
                                       }

                                   })
        print(search_results['hits']['total'])
        print(tracker.latest_message['text'])
        dispatcher.utter_message("The following document contains the text shown below.")
        # dispatcher.utter_message("<a href='http://localhost:3333/api/v1/exportcontrol/dowload/" + search_results['hits']['hits'][0]['_source']['name'] + "'>" + search_results['hits']['hits'][0]['_source']['name'] + "</a>")
        dispatcher.utter_message("[" + search_results['hits']['hits'][0]['_source']['name'] + "](http://localhost:3333/api/v1/exportcontrol/download/" + search_results['hits']['hits'][0]['_source']['name'] + ")")
        
        dispatcher.utter_message(search_results['hits']['hits'][0]['highlight']['content'][0])
        return []
