from config import *

def run() -> str:
  start_time = time.time()

  json_file = open(PARSER_JSON_DIR + 'allVacancyCard_JSON_Yandex.json', 'a', encoding='utf-8')

  url = 'https://yandex.ru/jobs/vacancies?text=стажёр'

  # Open the URL using Selenium WebDriver
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, "html.parser")

  # Collect links to all vacancy cards
  allVacancyCard_link = []
  for link in soup.findAll('a', class_='lc-jobs-vacancy-card__link'):
      allVacancyCard_link.append('https://yandex.ru' + link.get('href'))

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
          f"Using this html code of the vacancy {html_code}. "
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

  return 'allVacancyCard_JSON_Yandex.json'
