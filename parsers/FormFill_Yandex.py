from config import *

def fill_yandex_forms(card) -> None:
  link = card['link']
  driver.get(link)
  driver.find_element(by ="xpath", value="/html/body/div[1]/div/main/form/div/div[2]/div[2]/div/div[1]/label[2]").click()
  driver.find_element(by ="xpath", value="/html/body/div[1]/div/main/form/div/div[3]/div[2]/div[1]/span/span/input").send_keys(card['form']['resume']['label'])

  values = []
  for atribute in card['form']:
    if atribute != 'link' and atribute != 'resume':
      values.append(card['form'][atribute]['label'])
  pos = 0

  dom = etree.HTML(driver.page_source)
  tree = etree.ElementTree(dom)
  form_inputs = dom.xpath('//*/span/span/input')
  for thing in form_inputs:
    driver.find_element(by ="xpath", value=tree.getpath(thing)).send_keys(values[pos])
    pos += 1
  form_inputs = dom.xpath('//*/textarea')
  for thing in form_inputs:
    driver.find_element(by ="xpath", value=tree.getpath(thing)).send_keys(values[pos])
    pos += 1

  driver.find_element(by ="xpath", value="/html/body/div[1]/div/main/form/div/div[10]/div/div/div[1]/label/span[1]/input").click()
  driver.find_element(by ="xpath", value="/html/body/div[1]/div/main/form/div/div[11]/div/div/div[1]/label/span[1]/input").click()
  driver.find_element(by ="xpath", value="/html/body/div[1]/div/main/form/div/div[12]/div/div/div[1]/label/span[1]/input").click()
  driver.close()
