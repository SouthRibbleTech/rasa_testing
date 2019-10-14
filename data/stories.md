## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## give me a forecast
* get_supplier_forecast{"partnumber":"J12345-001"}
  - slot {"partnumber":"J12345-001"}
  - action_get_forecast
* get_part_number
  - utter_get_part_number
  - form{"partnumber": "partnumber_form"}
  - form{"partnumber":null}
  - slot{"partnumber":"677665-001"}


## export_control
* export_control
  - action_export_control

