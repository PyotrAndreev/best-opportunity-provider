from config import *
start_time = time.time()

url = 'https://www.internationalstudent.com/school-search/school/search/?page='
json_file = open('../JSON_webs/allVacancyCard_JSON_InternationalStudent.json', 'a', encoding='utf-8')

allVacancyCard_link = []
for num in range(1, 146):
  try:
    driver.get(url + f'{num}') 
  except:
    continue

  soup = BeautifulSoup(driver.page_source, "html.parser")
  for link in soup.find_all('a', class_='font-bitter text-left text-danger mb-2 mb-lg-0'):
    allVacancyCard_link.append('https://www.internationalstudent.com' + link.get('href'))

  break
allVacancyCard_link = allVacancyCard_link[:10]

json_file.write("[")
for num_link in range(len(allVacancyCard_link)):
  link = allVacancyCard_link[num_link]
  try:
    driver.get(link)
  except:
    continue
  html_code = BeautifulSoup(driver.page_source, "html.parser")
  question = f"Fill in the json form: {example}, using this html code of the vacancy: {html_code}. Also, be sure to find links to the vacancy and the mold and paste them into json. Be sure to find all the fields of the application form and paste them into json. I want the data in the new JSON to be translated into Russian and rephrased so that they can be used as separate sentences. Send me only the code of this JSON."

  completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[{"role":"user","content":question}],
    temperature=0.1,
    top_p=1,
    max_tokens=16384,
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

# culc = 0
# allVacancyForms = []
# allVacancyCard_JSON = []
# json_file.write("[")
# for link in allVacancyCard_link:
#   card_data = {}

#   try:
#     driver.get(link)
#   except:
#     continue
#   pageVacancy = driver.page_source
#   soupVacancy = BeautifulSoup(pageVacancy, "html.parser")

#   card_data['id'] = culc
#   card_data['link'] = link
#   card_data['title'] = str(soupVacancy.find('h1').text.replace("\n", ""))
#   card_data['short_description'] = str((soupVacancy.find('div', {"id": 'school-info-mission'}).text if soupVacancy.find('div', {"id": 'school-info-mission'}) is not None else '')).replace("\n", "")
#   card_data['description'] = str((soupVacancy.find('div', class_='markdown-content').text if soupVacancy.find('div', class_='markdown-content') is not None else '')).replace("\n", "")

#   card_data['tags']  = (''.join([tag.text for tag in soupVacancy.find('div', class_='col-sm d-flex flex-column justify-content-between').find_all('div')] if soupVacancy.find('div', class_='col-sm d-flex flex-column justify-content-between') is not None else [])).replace('\n\n', '\n').replace('\t', '').split('\n')
  
#   form_link = link

#   form_data = {}
#   form_data['link'] = form_link

#   soupForm = soupVacancy.find('div', class_='card card-body bg-light shadow rounded-0')
#   formFilds = soupForm.find('div', class_='row')
#   for thing in formFilds.find_all('label', class_='mb-1 col-sm-4 col-md-3 col-lg-4 col-form-label text-md-right'):
#     form_data[str(thing.text)] = {'value': '', 'type':'string'}
      
#   for thing in soupForm.findAll('div', class_='select-wrap'):
#     name = thing.get('data-placeholder')
#     values = []
#     for thing2 in thing.findAll('option'):
#       if(thing2.get('value') is not None):
#         values.append((thing2.get('value'), thing2.text))
#     form_data[name] = {'value': values, 'type':'select-wrap'}

#   if soupForm.find('img') is not None:
#     response = requests.get('	https://www.internationalstudent.com' + soupForm.find('img').get('src'))
#     image = Image.open(BytesIO(response.content))
#     txt = pytesseract.image_to_string(image, lang='eng').replace("\n", "")
#     print(txt)
#     form_data['Type the text from the image ']['value'] = txt

#   card_data['form'] = form_data
#   allVacancyCard_JSON.append(card_data)

#   json.dump(card_data, json_file, ensure_ascii=False, indent=4)
#   json_file.write(",\n")

#   culc+=1
#   print(culc)
#   card_data['id'] = culc
# json_file.write("{ }\n]")


driver.close()  
print("--- Work time: %s seconds ---" % (time.time() - start_time))