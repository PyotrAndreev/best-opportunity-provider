from config import *
start_time = time.time()

url = 'https://www.google.com/about/careers/applications/jobs/results/?src=Online/Google%20Website/ByF&utm_source=Online%20&utm_medium=careers_site%20&utm_campaign=ByF&company=Fitbit&company=Google&company=YouTube&distance=50&employment_type=INTERN'
json_file = open('../JSON_webs/allVacancyCard_JSON_CIEE.json', 'a', encoding='utf-8')

driver.get(url) 
soup = BeautifulSoup(driver.page_source, "html.parser")
allVacancyCard_link = []
for link in soup.find_all('a', class_='WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb'):
  allVacancyCard_link.append('https://www.google.com/about/careers/applications/' + link.get('href'))

json_file.write("[")
for num_link in range(len(allVacancyCard_link)):
  link = allVacancyCard_link[num_link]
  driver.get(link)
  html_code = BeautifulSoup(driver.page_source, "html.parser").find('div', class_='ObfsIf-haAclf ObfsIf-haAclf-fW01td-oXtfBe tFpK0')
  question = f"Fill in the maximum number of fields in the json form: {example}. using this html code of the vacancy {html_code}. Also, be sure to find links to the vacancy and the mold and paste them into json. I want the data in the new JSON to be translated into Russian and rephrased so that they can be used as separate sentences. Send me only the code of this JSON."

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