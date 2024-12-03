from config import *
start_time = time.time()

url = 'https://career.habr.com/vacancies?qid=1&type=all&page='
json_file = open('../JSON_webs/allVacancyCard_JSON_Habr.json', 'a', encoding='utf-8')

allVacancyCard_link = []
for page_num in range(1, 7):
  try:
    driver.get(url + f'{page_num}') 
  except:
    continue
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")
  for link in soup.find_all('a', class_='vacancy-card__title-link'):
    allVacancyCard_link.append('https://career.habr.com' + link.get('href'))

# allVacancyCard_link = allVacancyCard_link[:1]

culc = 0
allVacancyForms = []
allVacancyCard_JSON = []
json_file.write("[")
for num_link in range(len(allVacancyCard_link)):
  link = allVacancyCard_link[num_link]
  try:
    driver.get(link)
  except:
    continue
  html_code = BeautifulSoup(driver.page_source, "html.parser")
  question = f"Fill in the maximum number of fields in the json form: {example}. using this html job code {html_code}. I want the data in the new JSON to be translated into Russian and rephrased so that they can be used as separate sentences. Just send me the code of this JSON."
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

driver.close()  
print("--- Work time: %s seconds ---" % (time.time() - start_time))