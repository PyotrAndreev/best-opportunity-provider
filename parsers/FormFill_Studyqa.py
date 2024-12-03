from config import *

from parser_Studyqa import allFormsJSON

for card in allFormsJSON:
  link = card['link']
  service = ChromeService(executable_path=ChromeDriverManager().install())
  options = webdriver.ChromeOptions()
  # options.add_argument("--headless")
  driver = webdriver.Chrome(service=service, options=options)
  driver.get(link)
  soupForm = BeautifulSoup(driver.page_source, "html.parser")

  values = []
  for atribute in card:
    if atribute != 'link' and atribute != 'Добавить резюме':
      values.append(card[atribute]['value'])
  pos = 0

# /html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/form/div[2]/div/div[1]/div/input
# /html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/form/div[2]/div/div[2]/div/input
# /html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/form/div[2]/div/div[4]/div/input
# /html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/form/div[2]/div/div[5]/div/span/span[1]/span/span[1]/span
# /html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div/div/div/div[1]/form/div[2]/div/div[6]/div/input

  for thing in driver.find_elements(By.CLASS_NAME, "form-control"):
    thing.send_keys(str(pos))
    pos += 1
    sleep(2)
  
  sleep(30)
