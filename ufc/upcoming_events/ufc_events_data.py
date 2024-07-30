from bs4 import BeautifulSoup
import requests
import csv
from mma_master_1_utils import extract_text_safely

ORG_WEBSITE = "https://www.ufc.com"
EVENT_HEADLINE = None
EVENT_ARENA = None
EVENT_LOCATION = None
EVENT_CARD = None
EVENT_DATETIME = None
EVENT_COVER_IMAGE = None
 
FIGHTERS_DIVISION=None

FIGHTER1 = None 
FIGHTER1_IMAGE = None
FIGHTER1_COUNTRY = None
FIGHTER1_ODD = None

FIGHTER2 = None
FIGHTER2_IMAGE = None 
FIGHTER2_COUNTRY = None
FIGHTER2_ODD = None

ALL_AVAILABLE_UFC_EVENTS = [
  ["EVENT_HEADLINE", "EVENT_ARENA", "EVENT_LOCATION", "FIGHTERS_DIVISION", "EVENT_CARD", "FIGHTER1", "FIGHTER1_IMAGE", "FIGHTER1_COUNTRY", "FIGHTER1_ODD", "FIGHTER2","FIGHTER2_IMAGE","FIGHTER2_COUNTRY","FIGHTER2_ODD", "EVENT_DATETIME", "EVENT_COVER_IMAGE"]
]




EVENT_CATEGOY = ['main-card','fight-card-prelims', 'fight-card-prelims-early']

ufc_UE_page = requests.get("https://www.ufc.com/events#events-list-upcoming")
pageContent = BeautifulSoup(ufc_UE_page.content, 'html.parser')

UE_EventsContainer = pageContent.find("div", class_="c-listing__wrapper--horizontal-tabs").find("details")

EventsContainer = UE_EventsContainer.find_all("div", class_="l-listing__item")

for events in EventsContainer:
  EventsInfo =  events.find_all("div", "c-card-event--result__info")

  for Information in EventsInfo:
    EVENT_LINK = Information.find("h3").find("a").get("href")
    EVENT_ARENA = extract_text_safely(Information, ("div", {"class":"c-card-event--result__location"}), ("div", {"class": "field--name-taxonomy-term-title"}))
    
    EVENT_LOCATION = extract_text_safely( Information, ("div", {"class": "c-card-event--result__location"}), ("div", {"class":"field--name-location"}))

    
    EventPage = requests.get(f"{ORG_WEBSITE}{EVENT_LINK}")
    EventPageContent = BeautifulSoup(EventPage.content, 'html.parser')
    try:
      EventInformation = EventPageContent.find("div", class_="dialog-off-canvas-main-canvas")
      EVENT_COVER_IMAGE = EventInformation.find("div", class_="c-hero__image").find("img").get("src")
      
      EVENT_HEADLINE = extract_text_safely(EventInformation, ("div", {"class": "c-hero__headline-prefix"})) 
      
      event_cards = EventInformation.find("div", class_="l-main__content").find("div", class_="fight-card")
      
      for categoy in EVENT_CATEGOY:
        fight_card=event_cards.find("div", class_=f"{categoy}")
        EVENT_CARD = extract_text_safely(fight_card, ("h3", {"class": "hidden"}))
        EVENT_DATETIME = extract_text_safely(fight_card, ("div", {"class":"c-event-fight-card-broadcaster__mobile-wrapper"}),("div", {"class":"c-event-fight-card-broadcaster__time tz-change-inner"}))
        fight_information = fight_card.find("section").find("ul").find_all("li")
        
        for fighter_information in fight_information:
          
          FIGHTER1_IMAGE = fighter_information.find("div", class_="c-listing-fight__content-row").find("div", class_="c-listing-fight__corner-image--red").find("a").find("img").get("src")
          FIGHTER2_IMAGE = fighter_information.find("div", class_="c-listing-fight__content-row").find("div",class_="c-listing-fight__corner-image--blue").find("a").find("img").get("src")
      
          Peronal_info = fighter_information.find("div", class_="c-listing-fight__details")
          FIGHTERS_DIVISION = extract_text_safely(Peronal_info,("div", {"class":"c-listing-fight__class-text"}))
          FIGHTER1 =  extract_text_safely(Peronal_info,("div", {"class":"c-listing-fight__names-row"}),("div", {"class":"c-listing-fight__corner-name--red"}))
          FIGHTER2 = extract_text_safely(Peronal_info,("div", {"class":"c-listing-fight__names-row"}),("div", {"class":"c-listing-fight__corner-name--blue"}))
      
          FIGHTER1_COUNTRY = extract_text_safely(fighter_information,("div", {"class":"c-listing-fight__odds-row"}),("div", {"class":"c-listing-fight__country--red"}))
          
          
          FIGHTER2_COUNTRY = extract_text_safely(fighter_information,("div", {"class":"c-listing-fight__odds-row"}),("div", {"class":"c-listing-fight__country--blue"}))
          
          FIGHTER1_ODD = fighter_information.find("div", class_="c-listing-fight__odds-row").find("div", class_="c-listing-fight__odds-wrapper").find_all("span", class_="c-listing-fight__odds")[0].text
          
          FIGHTER2_ODD = fighter_information.find("div", class_="c-listing-fight__odds-row").find("div", class_="c-listing-fight__odds-wrapper").find_all("span", class_="c-listing-fight__odds")[1].text
          
          print([[EVENT_HEADLINE, EVENT_ARENA, EVENT_LOCATION, FIGHTERS_DIVISION, EVENT_CARD, FIGHTER1, FIGHTER1_IMAGE, FIGHTER1_COUNTRY, FIGHTER1_ODD, FIGHTER2,FIGHTER2_IMAGE,FIGHTER2_COUNTRY,FIGHTER2_ODD, EVENT_DATETIME, EVENT_COVER_IMAGE]])
          EVENT_FIGHT_DATA = []
          EVENT_FIGHT_DATA.extend([EVENT_HEADLINE, EVENT_ARENA, EVENT_LOCATION, FIGHTERS_DIVISION, EVENT_CARD, FIGHTER1, FIGHTER1_IMAGE, FIGHTER1_COUNTRY, FIGHTER1_ODD, FIGHTER2,FIGHTER2_IMAGE,FIGHTER2_COUNTRY,FIGHTER2_ODD, EVENT_DATETIME, EVENT_COVER_IMAGE])
          ALL_AVAILABLE_UFC_EVENTS.append(EVENT_FIGHT_DATA)
    except:
      pass
    
              
print('\n---------------------------------------------------------------------')                
print("Extracted Datas are been converted to csv format\nPlease Wait MMA master 1...")            
  
  
with open("ufc_events.csv", mode='w', newline='', encoding='utf-8') as file:
  writer = csv.writer(file)
  writer.writerows(ALL_AVAILABLE_UFC_EVENTS)
  
  print("Data Extraction Completed(100%) MMA master 1..")           

print('\n---------------------------------------------------------------------')   
