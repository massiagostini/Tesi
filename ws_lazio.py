from cmd import PROMPT
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def toTxtList(lista):
    output = ''
    for ii in lista:
        if ii != lista[-1]:
            output = output + ii.text + ', '
        else:
            output = output + ii.text
    return output

def linkCollector1(browser):
    listaEl = browser.find_elements(By.XPATH, "//div[@class='box-bandi-immagine']//a")
    links = []
    for ii in listaEl:
        links.append(ii.get_attribute('href'))
    return links

def excelOut(bandi, nomeFile):
    excel = pd.DataFrame(bandi) #generate dataframe from list
    excel.to_excel(nomeFile+".xlsx", index = False) #export dataframe in excel

def scraper1(browser):
    bando = {}
    bando['title'] = browser.find_element(By.XPATH, "//div[@class='single-bandi-titolo']").text
    bando['categoria'] = browser.find_element(By.XPATH, "//div[@class='single-bandi-categoria']").text
    tipoAg = browser.find_elements(By.XPATH, "/html/body/div[1]/main/article/footer/span[1]/div")
    tipoAg = toTxtList(tipoAg)    
    bando['Tipo Agevolazioni'] = tipoAg
    dest = browser.find_elements(By.XPATH, "/html/body/div[1]/main/article/footer/span[2]/div/a")
    dest = toTxtList(dest)
    bando['Destinatari'] = dest
    enti = browser.find_elements(By.XPATH, "html/body/div[1]/main/article/footer/span[3]/div/a")
    enti = toTxtList(enti)
    bando['Enti'] = enti
    bando['url'] = browser.current_url

    return bando
      
def crowler1(browser, stato):
    actions = ActionChains(browser)
    bandi=[]
    selector = Select(browser.find_element(By.ID, "filtro-stati"))
    selector.select_by_visible_text(stato)
    browser.find_element(By.NAME, 'action').click()
    links = linkCollector1(browser)
    while True:
        try:
            browser.find_element(By.PARTIAL_LINK_TEXT, 'SUCCESSIVI').click()
            links_tmp = linkCollector1(browser)
            for ii in links_tmp:
                links.append(ii)
        except:
            break
    for ii in links:
        browser.get(ii)
        bandi.append(scraper1(browser))
    return bandi

def lazEuropa():
    bandi = []
    browser = webdriver.Chrome()
    browser.get('http://www.lazioeuropa.it/bandi/')
    try:
        browser.find_element(By.PARTIAL_LINK_TEXT, 'Accetta tutto').click()
    except:
        pass
    aperti = crowler1(browser, 'Aperto')
    browser.get('http://www.lazioeuropa.it/bandi/')
    try:
        browser.find_element(By.PARTIAL_LINK_TEXT, 'Accetta tutto').click()
    except:
        pass
    proxApertura = crowler1(browser, 'Prossima Apertura')
    bandi = []
    for ii in aperti:
        ii['Stato']='Aperto'
        bandi.append(ii)
    for jj in proxApertura:
        jj['Stato']='Prossima Apertura'
        bandi.append(jj)
    browser.quit()
    return bandi

def linkCollector2(browser):
    lista_tmp =  browser.find_elements(By.XPATH, "//header//h2//a")
    output = []
    for ii in lista_tmp:
        output.append(ii.get_attribute('href'))
    return output

def scraper2(browser):
    bando = {}
    bando['Titolo'] = browser.find_element(By.XPATH, "//header[@class='entry-header']").text
    bando['url'] = browser.current_url
    tematiche = browser.find_elements(By.XPATH, "html/body/div[1]/main/article/footer/span[1]/div/a")
    tematiche = toTxtList(tematiche)
    bando['Tematiche'] = tematiche
    tipoFondi = browser.find_elements(By.XPATH, "html/body/div[1]/main/article/footer/span[2]/div/a")
    tipoFondi = toTxtList(tipoFondi)
    bando['Tipologie Fondi'] = tipoFondi
    tipoAg = browser.find_elements(By.XPATH, "html/body/div[1]/main/article/footer/span[3]/div/a")
    tipoAg = toTxtList(tipoAg)
    bando['Tipo Agevolazioni'] = tipoAg
    dest = browser.find_elements(By.XPATH, "html/body/div[1]/main/article/footer/span[4]/div/a")
    dest = toTxtList(dest)
    bando['Destinatari'] = dest
    return bando
    
def crowler2(browser, stato):
    actions = ActionChains(browser)
    bandi=[]
    selector = Select(browser.find_element(By.ID, "filtro-stati"))
    selector.select_by_visible_text(stato)
    browser.find_element(By.NAME, 'action').click()
    links = linkCollector2(browser)
    while True:
        try:
            browser.find_element(By.PARTIAL_LINK_TEXT, 'BANDI MENO RECENTI').click()
            links.append(linkCollector2(browser))
        except:
            break
    for ii in links:
        browser.get(ii)
        bandi.append(scraper2(browser))
    return bandi

def lazioInnova():
    browser = webdriver.Chrome()
    browser.get('http://www.lazioinnova.it/bandi/')
    aperti = crowler2(browser, 'Aperto')
    browser.get('http://www.lazioinnova.it/bandi/')
    proxApertura = crowler2(browser, 'Prossima Apertura')
    bandi = []
    for ii in aperti:
        ii['Stato']='Aperto'
        bandi.append(ii)
    for jj in proxApertura:
        jj['Stato']='Prossima Apertura'
        bandi.append(jj)
    browser.quit()
    return bandi

if __name__=='__main__':
    #lazEu = lazEuropa()
    #excelOut(lazEu, 'lazioeuropa')
    lazInn = lazioInnova()
    excelOut(lazInn, 'lazioinnova')
    
