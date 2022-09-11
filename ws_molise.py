from cmd import PROMPT
from lib2to3.pgen2 import driver
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def scraper(browser):
    bando = {}
    titolo = browser.find_element(By.XPATH, "//section[@id='post-content']//h1").text
    if titolo == 'TEST':
        return
    bando['Titolo'] = titolo
    bando['url'] = browser.current_url
    bando['Descrizione'] = browser.find_element(By.XPATH, "//div[@class='field field-name-body field-type-text-with-summary field-label-hidden']")
    bando['Misura'] = browser.find_element(By.XPATH, "//div[@class='field field-name-field-relazione-misura field-type-taxonomy-term-reference field-label-above']//div[@class=field-item even']")
    print(bando)
    return bando

def crowler(browser):
    actions = ActionChains(browser)
    bandi = []
    lista = browser.find_elements(By.XPATH, "//div[@class='field-item even']//h3//a")
    links = []
    for ii in lista:
        #time.sleep(3)
        tmp = ii.get_attribute("href")
        if tmp != None:
            links.append(tmp)
    for ii in links:
        print(ii)
        browser.get('https://psr.regione.molise.it/aperti')
        time.sleep(3)
        browser.get(ii+'/')
        time.sleep(2)
        tmp_list = browser.find_elements(By.PARTIAL_LINK_TEXT, 'Leggi tutto')
        for jj in tmp_list:
            browser.get(jj.get_attribute('href'))
            b_tmp = scraper(browser)
            time.sleep(2)
            if b_tmp != None:
                bandi.append(b_tmp)
    return bandi
            


def psrMolise():
    browser = webdriver.Chrome()
    browser.get('https://psr.regione.molise.it/aperti')
    bandi = crowler(browser)



if __name__=='__main__':
    psrMolise()