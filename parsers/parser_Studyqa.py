from config import *

start_time = time.time()

url = 'https://ru.studyqa.com/internships/countries/cities/industries?page='

culc = 0
allVacancyCard_link = []
for page_num in range(1, 8):
  driver.get(url + f'{page_num}')
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")
  for link in soup.findAll('div', class_='cards__list'):
    culc+=1
    print(culc)
    allVacancyCard_link.append(link.find('a', class_='btn btn-secondary').get('href'))

# allVacancyCard_link = allVacancyCard_link[:1]

json_file = open('../JSON_webs/allVacancyCard_JSON_Studyqa.json', 'a', encoding='utf-8')

json_file.write("[")
for num_link in range(len(allVacancyCard_link)):
  link = allVacancyCard_link[num_link]
  driver.get(link)
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