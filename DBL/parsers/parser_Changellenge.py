from config import *

def run() -> str:
  start_time = time.time()

  json_file = open(PARSER_JSON_DIR + 'best-opportunity-provider/JSON_webs/allVacancyCard_JSON_Changellenge.json', 'a', encoding='utf-8')

  url = 'https://changellenge.com/vacancy/'

  # Navigate to the URL and parse the page
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, "html.parser")

  allVacancyCard_link = []
  # Collect all vacancy links
  for link in soup.find_all('a', class_='new-vacancies-card__link new-vacancies-card__logo-wrapper'):
    allVacancyCard_link.append('https://changellenge.com' + link.get('href'))

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

    # Extract the relevant HTML section
    html_code = BeautifulSoup(driver.page_source, "html.parser").find('div', class_='vacancy-without-form-wrapper-shadow')

    # Formulate the question for GPT
    question = (
      f"Fill in the maximum number of fields in the json form: {example}. using this html code of the vacancy {html_code}. "
      "Also, be sure to find links to the vacancy and the mold and paste them into json. I want the data in the new JSON "
      "to be translated into Russian and rephrased so that they can be used as separate sentences. Send me only the code of this JSON."
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
  return 'allVacancyCard_JSON_Changellenge'