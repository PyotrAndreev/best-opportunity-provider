from config import *

def run() -> str:
  start_time = time.time()

  json_file = open(PARSER_JSON_DIR + 'best-opportunity-provider/JSON_webs/allVacancyCard_JSON_Studyqa.json', 'a', encoding='utf-8')

  url = 'https://ru.studyqa.com/internships/countries/cities/industries?page='

  allVacancyCard_link = []
  for page_num in range(1, 8):  # Pages 1-7
      try:
          driver.get(url + f'{page_num}')
          page = driver.page_source
          soup = BeautifulSoup(page, "html.parser")
          for link in soup.findAll('div', class_='cards__list'):
              card_link = link.find('a', class_='btn btn-secondary')
              if card_link:
                  allVacancyCard_link.append(card_link.get('href'))
      except Exception as e:
          print(f"Error accessing page {page_num}: {e}")
          continue

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
          f"Fill in the maximum number of fields in the json form: {example}. "
          f"Using this html job code {html_code}. "
          "I want the data in the new JSON to be translated into Russian and rephrased "
          "so that they can be used as separate sentences. Just send me the code of this JSON."
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
  return 'allVacancyCard_JSON_Studyqa.json'
