from config import *

def run() -> str:
  start_time = time.time()

  json_file = open(PARSER_JSON_DIR + 'best-opportunity-provider/JSON_webs/allVacancyCard_JSON_Habr.json', 'a', encoding='utf-8')

  url = 'https://career.habr.com/vacancies?qid=1&type=all&page='

  allVacancyCard_link = []
  for page_num in range(1, 7):  # Pages 1-6
      try:
          driver.get(url + f'{page_num}')
      except Exception as e:
          print(f"Error accessing page {page_num}: {e}")
          continue

      page = driver.page_source
      soup = BeautifulSoup(page, "html.parser")
      for link in soup.find_all('a', class_='vacancy-card__title-link'):
          allVacancyCard_link.append('https://career.habr.com' + link.get('href'))

  # Write the opening bracket for the JSON array
  json_file.write("[")

  # Iterate through all vacancy links and process them
  for num_link in range(len(allVacancyCard_link)):
      link = allVacancyCard_link[num_link]
      try:
          driver.get(link)
      except Exception as e:
          print(f"Error accessing link {link}: {e}")
          continue

      # Parse the page source
      html_code = BeautifulSoup(driver.page_source, "html.parser")

      # Formulate the question for GPT
      question = (
          f"Fill in the maximum number of fields in the json form: {example}. using this html job code {html_code}. "
          "I want the data in the new JSON to be translated into Russian and rephrased so that "
          "they can be used as separate sentences. Just send me the code of this JSON."
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
  return 'allVacancyCard_JSON_Habr'