import csv
from typing import Any, Text, Dict, List

import joblib
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from app.services.database import create_connection, execute_query
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

class ActionAddSymptom(Action):
    def name(self) -> Text:
        return "action_add_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy slot hiện tại
        current_symptoms = tracker.get_slot("symptoms") or []
        current_symptom = tracker.get_slot("symptom")

        # Thêm triệu chứng mới vào danh sách
        for symptom in current_symptom:
            if symptom not in current_symptoms:
                current_symptoms.extend(current_symptom)

        # dispatcher.utter_message(text=f"Triệu chứng hiện tại của bạn: {current_symptoms}")
        dispatcher.utter_message(text="Bạn có muốn thêm triệu chứng nào khác không?")

        return [SlotSet("symptoms", current_symptoms)]
    
class ActionPredictDisease(Action):
    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cnx = create_connection()
        # Lấy triệu chứng từ slot
        symptoms = tracker.get_slot("symptoms")

        # dispatcher.utter_message(text=f"Triệu chứng của bạn: {symptoms}")

        pipeline = joblib.load('./models/pipeline.pkl')

        # Dự đoán bệnh
        symptoms_str = ' '.join(symptoms)
        predicted_disease = pipeline.predict([symptoms_str])[0]

        dispatcher.utter_message(text=f"Bạn có thể bị mắc phải bệnh: {predicted_disease}")

        how_many_symptom = ','.join('symptom_{}'.format(i) for i in range(len(symptoms)))
        this_many_symptom = ','.join(f"'{symptom}'" for symptom in symptoms)
        
        try:
            execute_query(cnx,f"INSERT INTO dataset(disease,{how_many_symptom}) VALUES ('{predicted_disease}',{this_many_symptom})")
        except Exception as e:
            print(e)
        return [SlotSet("symptoms", None)]
    
class ActionProvideDiseaseInfo(Action):
    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dataframe = pandas.read_csv('./data/disease_description.csv', encoding='utf-8', quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',')
        # known_diseases = dataframe['Disease'].values
        known_diseases = execute_query(create_connection(),"SELECT * FROM chitietbenh")

        # Lấy tên bệnh từ entity `disease`
        disease = tracker.get_slot("disease")
        if disease:
        # Find the disease in the query results
            disease_info = next((row for row in known_diseases if row[1].lower() == disease.lower()), None)
        
            if disease_info:
            # Display disease information
                dispatcher.utter_message(text=f"{disease_info[3]}")  # Display description
            else:
                dispatcher.utter_message(response="utter_no_disease_info")
        else:
            dispatcher.utter_message(response="utter_no_disease_info")
        
        return []
    
class ActionProvideDiseasePrecaution(Action):
    def name(self) -> Text:
        return "action_provide_disease_precaution"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dataframe = pandas.read_csv('./data/disease_description.csv', encoding='utf-8', quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',')
        # known_diseases = dataframe['Disease'].values
        known_diseases = execute_query(create_connection(),"SELECT * FROM chitietbenh")

        # Lấy tên bệnh từ entity `disease`
        disease = tracker.get_slot("disease")
        if disease:
        # Find the disease in the query results
            disease_info = next((row for row in known_diseases if row[1].lower() == disease.lower()), None)
        
            if disease_info:
            # Display disease information
                dispatcher.utter_message(text=f"{disease_info[2]}")  # Display precaution
            else:
                dispatcher.utter_message(response="utter_no_disease_info")
        else:
            dispatcher.utter_message(response="utter_no_disease_info")
        
        return []
