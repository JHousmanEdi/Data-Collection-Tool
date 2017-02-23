
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException

class to_AddressFinder(object):

    def __init__(self):
        display = Display(visible = 0, size =(800, 600))
        display.start()
        self.browser = webdriver.Chrome()
        #Determine if there is a reply button
    def gotoPage(url):
        self.browser.get(url)

    def check_exists_by_xpath():
        try:
            webdriver.find_element_by_xpath('/html/body/section/section/header/button')
        except NoSuchElementException:
            return False
        return True
        #Click reply button
    def Click_Reply():
        browser.find_element_by_xpath('/html/body/section/section/header/button').click()

    '''
    TODO
    Build function to deal with capchas
    '''
        #Obtain to_Address
    def Obtain_data(self):
        to_Address = self.browser.find_element_by_xpath('/html/body/section/section/header/div[1]/aside/ul/li[3]/p').text
        return self.to_Address
