from config import *

def fill_superjob_form(card) -> None:
  link = card['link']
  driver.get(link)

  driver.find_element(by="xpath", value="/html/body/div/div[3]/div/div[1]/div/div/div/div/div/div/div[1]/button").click()

  driver.find_element(by="xpath", value="/html/body/div[2]/div[3]/div/div[1]/div[2]/form/div[2]/div[1]/div[1]/div/div/div/input").send_keys(card['form']['name']['label'])
  driver.find_element(by="xpath", value="/html/body/div[2]/div[3]/div/div[1]/div[2]/form/div[2]/div[1]/div[2]/div/div/div/input").send_keys(card['form']['surename']['label'])
  driver.find_element(by="xpath", value="/html/body/div[2]/div[3]/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/div/div/div/input").send_keys(card['form']['phone']['label'])
  driver.find_element(by="xpath", value="/html/body/div[2]/div[3]/div/div[1]/div[2]/form/div[2]/div[2]/div[2]/div/div/div/input").send_keys(card['form']['birthday']['label'])
  
  sleep(10)
  
  driver.find_element(by="xpath", value="/html/body/div[2]/div[3]/div/div[2]/div/button").click()

  sleep(10)
  
  driver.close()

tr = {
    "link": "https://students.superjob.ru/stazhirovki/44386520/",
    "form":{
      "name": {
        "type": "string",
        "label": "Art"
      },
      "surename": {
        "type": "string",
        "label": "Zap"
      },
      "birthday": {
        "type": "string",
        "label": "12.12.2000"
      },
      "email": {
        "type": "email",
        "label": "12345678@mail.ru"
      },
      "phone": {
        "type": "string",
        "label": "8005553535"
      },
      "resume": {
        "type": "string",
        "label": "тшорарикудшгрмпиорлыукрошдпружолмриошжвалыярпшомрцукнгшрщапр икушорритыпш доыуекшщгнр пагнолуыкр шгдщапукрфшгд"
      }
    }
  }

fill_superjob_form(tr)