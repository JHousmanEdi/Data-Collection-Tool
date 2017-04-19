
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

class to_AddressFinder(object):

    def __init__(self):
        display = Display(visible = 0, size =(800, 600))
        display.start()
        self.browser = webdriver.Firefox()
        #Determine if there is a reply button
    def gotoPage(self,url):
        self.browser.get(url)

    def check_exists_by_xpath(self):
        try:
            self.browser.find_element_by_xpath('/html/body/section/section/header/button')
        except NoSuchElementException:
            return False
        return True
        #Click reply button
    def get_email(self):
         self.browser.find_elements(By.CSS_SELECTOR, '.reply_button')[0].click()
         time.sleep(2)
         email = self.browser.find_elements(By.CSS_SELECTOR, '.anonemail')[0].text
         return email

    '''
    TODO
    Build function to deal with capchas
    '''
        #Obtain to_Address
