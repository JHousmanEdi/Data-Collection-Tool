#
# from selenium import webdriver
# from pyvirtualdisplay import Display
# from selenium.common.exceptions import NoSuchElementException
#
# class to_AddressFinder(object):
#
#     def __init__(self):
#         display = Display(visible = 0, size =(800, 600))
#         display.start()
#         self.browser = webdriver.Chrome()
#         #Determine if there is a reply button
#     def gotoPage(self, url):
#         self.browser.get(url)
#
#     def check_exists_by_xpath(self):
#         if self.browser.find_elements_by_xpath('/html/body/section/section/header/button') > 0:
#             return True
#         return False
#         #Click reply button
#     def Click_Reply(self):
#         self.browser.find_element_by_xpath('/html/body/section/section/header/button').click()
#     '''
#     TODO
#     Build function to deal with capchas
#     '''
#         #Obtain to_Address
#     def Obtain_data(self):
#         try:
#             to_Address = self.browser.find_element_by_class_name('anonemail')
#             return self.to_Address
#         except Exception:
#             return "Captchad"
