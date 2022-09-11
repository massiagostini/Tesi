import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
from selenium.webdriver.common.keys import Keys


def scraper1(browser):
    bando = {}
    bando['title'] = browser.find_element(By.XPATH, "//h1[@class='entry-title ']").text
    bando['url'] = browser.current_url
    specs_h = browser.find_elements(By.XPATH, "//h3[@class='cem-description-title']")
    specs_b = browser.find_elements(By.XPATH, "//div[@class='cem-text-description cem-overflow-anywhere']")

    for ii in range(len(specs_h)):
        bando[specs_h[ii].text] = specs_b[ii].text
        
    return bando

def scraper2(browser):
    bando = {}
    type = browser.find_element(By.XPATH, "//span[@class='txt_red_bold']").text
    if type != 'Bando di Gara':
        return
    tmp = browser.find_elements(By.TAG_NAME, 'p')
    date_tmp = browser.find_elements(By.XPATH, "//span[@class='txt_red']")
    bando['Scadenza'] = date_tmp[0].text
    bando['Pubblicazione'] = date_tmp[1].text
    bando['Descrizione']=tmp[2].text
    for ii in range(len(tmp)-3):
        splitted = tmp[ii+3].text.split(': ')
        bando[splitted[0]] = splitted[1]
    return bando
       

def crowler1(browser, type):
    actions = ActionChains(browser)
    bandi=[]
    catselector = browser.find_element(By.ID, type)
    actions.move_to_element(catselector).click(catselector).perform()
    try:
        lista = browser.find_elements(By.XPATH, "//div[@class='col-lg-4 col-lg-4 col-12 p-0 p-md-2 mb-4']")
    except:
        print('bandi non trovati/pagina irraggiungibile')
    for ii in lista:
        actions.move_to_element(ii).click(ii).perform()
        tmp_bando = scraper1(browser)
        bandi.append(tmp_bando)
        browser.back()
    return(bandi)

def crowler2(browser):
    actions = ActionChains(browser)
    bandi = []
    date = browser.find_element(By.NAME, "data_scad_dal")
    date.send_keys(datetime.today().strftime('%d/%m/%Y'))
    date.send_keys(Keys.ENTER)
    links = linkCollector2(browser, 'Visualizza ')
    while True:
        try:
            nextPage = browser.find_element(By.PARTIAL_LINK_TEXT, 'Precedenti')
            print(nextPage.text)
            actions.move_to_element(nextPage).perform()
            nextPage.click()
            for ii in linkCollector2(browser, 'Visualizza '):
                links.append(ii)
        except:
            break     
    for ii in links:
        browser.get(ii)
        bando_tmp = scraper2(browser)
        if bando_tmp != None:
         bandi.append(bando_tmp)
    return bandi
        
    
def linkCollector2(browser, partLinkText):
    list_tmp = browser.find_elements(By.PARTIAL_LINK_TEXT, 'Visualizza ')
    links = []
    for ii in list_tmp:
        links.append(ii.get_attribute('href'))
    return links
        

def calEuropa():
    bandi = []
    browser = webdriver.Chrome()
    browser.get('http://calabriaeuropa.regione.calabria.it/website//bandi/')
    try:
        browser.find_element(By.ID, 'wt-cli-accept-all-btn').click() #cookies
    except:
        pass
    prepublished = crowler1(browser, 'prepublished')
    browser.get('http://calabriaeuropa.regione.calabria.it/website//bandi/')
    try:
        browser.find_element(By.ID, 'wt-cli-accept-all-btn').click() #cookies
    except:
        pass
    published = crowler1(browser, 'published')
    for ii in prepublished:
        bandi.append(ii)
    for ii in published:
        bandi.append(ii)
    browser.quit()
    return bandi

def calReg():
    browser = webdriver.Chrome()
    browser.get('https://www.regione.calabria.it/website/bandiregione/')
    time.sleep(2)
    try:
        browser.find_element(By.PARTIAL_LINK_TEXT, 'Accetto!').click()
    except:
        pass
    bandi = crowler2(browser)
    return bandi

def excelOut(bandi, nomeFile):
    excel = pd.DataFrame(bandi) #generate dataframe from list
    excel.to_excel(nomeFile+".xlsx", index = False) #export dataframe in excel



if __name__=='__main__':
    bandiCalEu = calEuropa()
    bandiCalReg = calReg()
    excelOut(bandiCalReg, 'regione.calabria.it')
    excelOut(bandiCalEu, 'calabriaeuropa')
