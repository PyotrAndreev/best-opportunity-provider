from config import *

def run() -> str:
  start_time = time.time()

  json_file = open(PARSER_JSON_DIR + 'best-opportunity-provider/JSON_webs/allVacancyCard_JSON_FutureToday.json', 'a', encoding='utf-8')

  url = 'https://students.superjob.ru/stazhirovki/?page='

  # Collect links to all vacancy cards
  allVacancyCard_link = []
  for page_num in range(1, 135):  # Pages 1-134
      try:
          driver.get(url + f'{page_num}')
      except Exception as e:
          print(f"Error accessing page {page_num}: {e}")
          continue
      soup = BeautifulSoup(driver.page_source, "html.parser")
      for link in soup.find_all('div', class_='MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 VacancySnippet_root__Q5KZB mui-1sck884'):
          vacancy_link = link.find('a', class_='VacancySnippet_link__sF_cO')
          if vacancy_link:
              allVacancyCard_link.append('https://students.superjob.ru' + vacancy_link.get('href'))

  # Write the opening bracket for the JSON array
  json_file.write("[")

  # Iterate through all vacancy links and process them
  for num_link in range(len(allVacancyCard_link)):
      link = allVacancyCard_link[num_link]
      driver.get(link)

      # Parse the page source
      html_code = BeautifulSoup(driver.page_source, "html.parser")

      # Formulate the question for GPT
      question = (
          f"Fill in the maximum number of fields in the json form: {example}, "
          f"using this html code of the vacancy {html_code}. "
          "Also, be sure to find links to the vacancy and the mold and paste them into json. "
          "I want the data in the new JSON to be translated into Russian and rephrased "
          "so that they can be used as separate sentences. Send me only the code of this JSON."
      )

      # Add a comma for separation if it's not the first element
      if num_link != 0:
          json_file.write(',\n')

      # Write the response from GPT into the JSON file
      json_file.write(question_to_gpt(question))

  # Write the closing bracket for the JSON array
  json_file.write("\n]")

  # Close the browser and the file
  driver.close()
  json_file.close()

  print("--- Work time: %s seconds ---" % (time.time() - start_time))
  return 'allVacancyCard_JSON_Superjob.json'
