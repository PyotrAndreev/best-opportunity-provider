from includes import *

start_time = time.time()

url = 'https://yandex.ru/jobs/vacancies?text=стажёр'

service = ChromeService(executable_path=ChromeDriverManager().install())

options = webdriver.ChromeOptions()
# options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
page = driver.page_source

soup = BeautifulSoup(page, "html.parser")

#------------------Writing the html code of the page to the file----------------------
# with open('out.html', 'w', encoding='utf-8') as f:
#   f.write(page)

allVacancyCard_link = []
for link in soup.findAll('a', class_='lc-jobs-vacancy-card__link'):
  allVacancyCard_link.append('https://yandex.ru' + link.get('href'))

# allVacancyCard_link = allVacancyCard_link[:1]

#------------------Writing the html code of the job cards to the file----------------
# with open('allVacancy.html', 'w', encoding='utf-8') as f:
#   f.write(str(allVacancyCard))

#------------------Writing links to vacancies in the file--------------------------------
# with open('allVacancy_link.html', 'w', encoding='utf-8') as f:
#   for s in allVacancyCard_link:
#     f.write(str(s) + '\n')


json_file = open('../JSON_webs/allVacancyCard_JSON_Yandex.json', 'a', encoding='utf-8')

json_file.write("[")
for num_link in range(len(allVacancyCard_link)):
  link = allVacancyCard_link[num_link]
  driver.get(link)
  html_code = BeautifulSoup(driver.page_source, "html.parser")
  question = f"Carefully and correctly fill in the maximum number of fields in the json form: {example}. using this html job code {html_code}. I want the data in the new JSON to be translated into Russian and rephrased so that they can be used as separate sentences. Just send me the code of this JSON."
  
  completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[{"role":"user","content":question}],
    temperature=0.1,
    top_p=1,
    max_tokens=8192,
    stream=True
  )
  result = ''
  for chunk in completion:
    if chunk.choices[0].delta.content is not None:
      result += str(chunk.choices[0].delta.content)

  start = -1
  end = -1
  for i in range(len(result)):
    if(result[i] == '{' and start == -1):
      start = i
    if(result[i] == '}'):
      end = i
  
  if(num_link != 0):
    json_file.write(',\n')
  json_file.write(result[start: end + 1])
json_file.write("\n]")

#-------------------Writing the html code of the forms for vacancies to the file--------------
# with open('allVacancy_form.html', 'w', encoding='utf-8') as f:
#   for s in allVacancyForms:
#     f.write(str(s) + '\n')

# with open('allVacancy_formData.json', 'w', encoding='utf-8') as json_file:
#   json_file.write("{")
#   for for_json in allFormsJSON:
#     json.dump(for_json, json_file, ensure_ascii=False, indent=4)
#     json_file.write(",\n")
#   json_file.write("{ }\n}")

driver.close()  

print("--- Work time: %s seconds ---" % (time.time() - start_time))