import sys
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import csv
import codecs
import os
import re

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Craigslist Collection Tool")
        self.Menu_Options() #Initialize Menu
        self.CSVFile = {}
        self.CSV_Loaded = 0
        self.start = 1

        self.current_len = self.__len__(self.CSVFile)
        self.entry = EntryForm(self) #Entry form for data


        _widget = QtGui.QWidget()

        self.browser = QtWebKit.QWebView()


        self.url_input = UrlInput(self.browser, self) #Initialize url input

        self.layout = QtGui.QVBoxLayout(_widget) #Initialuze Vertical Layout

        self.layout.addWidget(self.url_input) #Add url Input widget

        self.layout.addWidget(self.browser) #Add Browser Widget

        self.layout.addWidget(self.entry) #Add Entry form Widget
        self.onMain = 1
        self.savepath = None
        self.setCentralWidget(_widget)
        self.html_location_chosen = 0
        self.show()

    def __len__(self, storage):
        return len(storage)

    def load_items(self, itemnum):
        if self.current_len == 0:
            raise Exception("No Items to load")

        else:
            CL_ID = self.CSVFile['CL_ID'][itemnum]
            Month = self.CSVFile['Month'][itemnum]
            Day = self.CSVFile['Day'][itemnum]
            State = self.CSVFile['State'][itemnum]
            RA = self.CSVFile['RA'][itemnum]
            urls = self.CSVFile['url']

        cur_values = {'CL_ID': CL_ID, 'Month': Month, 'Day':Day, 'State':State, 'RA':RA}
        self.urls = urls
        return cur_values




    def Menu_Options(self):
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close_application)
        importAction = QtGui.QAction('&Import CSV', self)
        importAction.setStatusTip('Import Jobs CSV')
        importAction.triggered.connect(self.selectFile)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(importAction)



    def setLoadedFile(self):
        self.CSV_Loaded = 1
        self.entry.set_filled_vals()

    def close_application(self):
        sys.exit()

    def selectFile(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Import CSV')
        csv_filled = self.load_csv(name)

        self.CSVFile = csv_filled

        self.current_len = len(self.CSVFile)

        self.setLoadedFile()


    def selectHtmlDirectory(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.html_location_chosen = 1
        return file


    def load_csv(self, csv_path):
        cities = []
        ids = []
        month = []
        day = []
        state = []
        url = []
        RA = []
        with open(csv_path, 'rb') as csvfile:
            scraper_reader = csv.DictReader(csvfile)
            for row in scraper_reader:
                    cities.append(row['City'])
                    ids.append(row['CL_ID'])
                    month.append(row['Month'])
                    day.append(row['Day'])
                    state.append(row['State'])
                    url.append(row['url'])
                    RA.append(row['RA'])
        vals = {'Day': day, 'CL_ID':ids, 'Month':month, 'State':state, 'url':url, 'RA':RA}

        return vals
    def load_url(self, url):
        self.url_input.url_chosen(url)
        self.url_input.goingToReply = 0
        self.browser.loadFinished.connect(self.get_HTML)

    def get_entries(self):
        values = self.entry.get_filled_in_values()

        if values['Approved'] == 0:
            pass
        if values['Approved'] == 1:
            entry = []
            entry.append(values['CL_ID'])
            entry.append(values['Month'])
            entry.append(values['Day'])
            entry.append(values['State'])
            entry.append(values['Occupation'])
            entry.append(values['ToAddress'])
            entry.append(values['WordResume'])
            entry.append(values['Company'])
            entry.append(values['CompanyDescription'])
            entry.append(values['EmailSubject'])
            entry.append(values['RA'])
            self.save_good_entry(entry)

    # def wait_for_captcha(self):
    #     self.browser.urlChanged.connect(self.pull_ToAddress)
    def load_toAddress(self):
        self.onMain = 0
        self.url_input.get_save_name()
        find_reply = self.browser.page().currentFrame().documentElement()
        reply_button_search = find_reply.findFirst('#replylink')
        reply_button_search.evaluateJavaScript('this.click()')
        self.browser.page().mainFrame().evaluateJavaScript('https://www.google.com/recaptcha/api.js?onload=gRecaptchaCallback&render=explicit')
        #self.browser.urlChanged.connect(self.wait_for_captcha)
    # def pull_ToAddress(self):
    #     element = self.browser.page().currentFrame().documentElement()
    #     Element_Search = element.findFirst("p[class=anonemail]")
    #     titlewcss = "%s" %Element_Search.toPlainText()
    #     #address = re.search('>(.*)<',titlewcss)
    #     self.fill_ToAddress(address)

    # def fill_ToAddress(self, value):
    #     self.entry.ToAddress_Fill(value)

    def get_HTML(self):
        self.page = self.browser.page().currentFrame().toHtml()


    def save_good_entry(self, entry):
        if self.savepath is None:
            self.savepath = QtGui.QFileDialog.getOpenFileName(
                    self, 'Save File', '', 'CSV(*.csv)')
        else:
            self.savepath = self.savepath

        filepath = "%s" %self.savepath
        directory_path = os.path.dirname(filepath)
        with open(self.savepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(entry)
        if self.html_location_chosen == 0:
            self.html_dir= self.selectHtmlDirectory()
        if self.html_location_chosen == 1:
            pass

        if self.onMain == 1:
            element = self.browser.page().currentFrame().documentElement()
            Element_Search = element.findFirst('#titletextonly')
            titlewcss = "%s" %Element_Search.toOuterXml()
            title_only = re.search('>(.*)<',titlewcss)
            save_name = title_only.group(1)
            with codecs.open(os.path.join(html_dir, save_name+'.html'),mode='w') as f:
                f.write(self.page)
        if self.onMain == 0:
            with codecs.open(os.path.join(self.html_dir, self.url_input.save_name+'.html'),mode='w') as f:
                f.write(self.page)








class EntryForm(QtGui.QWidget):
    def __init__(self, parent = None):
        super(EntryForm, self).__init__()
        self.main_layout = QtGui.QGridLayout()
        self.main_layout.setSpacing(10)
        self.parent = parent
        self.set_filled_vals()
        self.filled_fields()
        unfilled = self.unfilled_form()
        self.filled = self.filled_form()
        self.checkbox_layout = self.boolean_form()
        self.url_menu = self.url_dropdown()
        self.main_layout.addLayout(self.checkbox_layout, 1, 0)
        self.main_layout.addLayout(self.url_menu, 1, 1)
        self.main_layout.addLayout(self.filled, 2, 0)
        self.main_layout.addLayout(unfilled, 2, 1)
        self.setLayout(self.main_layout)
        self.nextAd.clicked.connect(self.load_next_url)
        self.curr_url_index = 0


        """
        After Loading CSV and loading items, the filled values will be swapped to new ones.
        """
    def set_filled_vals(self, url_index = 0):
        if self.parent.CSV_Loaded == 1:
            if self.parent.start == 1:
                filled_fields = self.parent.load_items(0)
            if self.parent.start == 0:
                filled_fields = self.parent.load_items(url_index)
            self.CL_IDVal = filled_fields['CL_ID']
            self.MonthVal =filled_fields['Month']
            self.DayVal = filled_fields['Day']
            self.StateVal = filled_fields['State']
            self.RAVal  = filled_fields['RA']
            self.filled_fields()

        if self.parent.CSV_Loaded == 0:
            self.CL_IDVal = ""
            self.MonthVal = ""
            self.DayVal = ""
            self.StateVal = ""
            self.RAVal = ""


    def filled_fields(self):
        if self.parent.CSV_Loaded == 0:

            self.CL_ID = QtGui.QLabel("CL_ID")
            self.CL_fill = QtGui.QLineEdit("")
            self.CL_fill.setReadOnly(True)
            self.Month = QtGui.QLabel("Month")
            self.Month_Fill = QtGui.QLineEdit("")
            self.Month_Fill.setReadOnly(True)
            self.Day = QtGui.QLabel("Day")
            self.Day_Fill = QtGui.QLineEdit("")
            self.Day_Fill.setReadOnly(True)
            self.State = QtGui.QLabel("State")
            self.State_Fill = QtGui.QLineEdit("")
            self.State_Fill.setReadOnly(True)
            self.RA = QtGui.QLabel("RA")
            self.RA_fill = QtGui.QLineEdit("")
            self.RA_fill.setReadOnly(True)
        if self.parent.CSV_Loaded == 1:
            self.CL_ID = QtGui.QLabel("CL_ID")
            self.CL_fill = QtGui.QLineEdit(self.CL_IDVal)
            self.CL_fill.setReadOnly(True)
            self.Month = QtGui.QLabel("Month")
            self.Month_Fill = QtGui.QLineEdit(self.MonthVal)
            self.Month_Fill.setReadOnly(True)
            self.Day = QtGui.QLabel("Day")
            self.Day_Fill = QtGui.QLineEdit(self.DayVal)
            self.Day_Fill.setReadOnly(True)
            self.State = QtGui.QLabel("State")
            self.State_Fill = QtGui.QLineEdit(self.StateVal)
            self.State_Fill.setReadOnly(True)
            self.RA = QtGui.QLabel("RA")
            self.RA_fill = QtGui.QLineEdit(self.RAVal)
            self.RA_fill.setReadOnly(True)
            self.update_filled_form()

    def ToAddress_Fill(self, value):
        self.ToAddressFill = QtGui.QLineEdit(value)
        self.unfilled_layout.addWidget(self.ToAddressFill, 3, 1)
        self.setLayout(self.main_layout)

    def update_filled_form(self):
        self.filled.addWidget(self.CL_fill, 1, 1)
        self.filled.addWidget(self.Month_Fill, 2, 1)
        self.filled.addWidget(self.Day_Fill, 3, 1)
        self.filled.addWidget(self.State_Fill, 4, 1)
        self.filled.addWidget(self.RA_fill, 5, 1)
        self.setLayout(self.main_layout)

        if self.parent.start == 1:
            self.url_dropdown()
        else:
            pass

    def get_filled_in_values(self):
        filled_in = {}
        if self.Approved_Answer.isChecked():
            filled_in['Approved'] = 1
        else:
            filled_in['Approved'] = 0

        filled_in['CL_ID'] = "%s" %self.CL_fill.text()
        filled_in['Month'] = "%s" % self.Month_Fill.text()
        filled_in['Day'] = "%s" %self.Day_Fill.text()
        filled_in['State'] = "%s" %self.State_Fill.text()
        filled_in['Occupation'] = "%s" %self.Occupation_Entry.text()
        filled_in['ToAddress'] = "%s" %self.ToAddress_Entry.text()
        if self.WordResume_Answer.isChecked():
            filled_in['WordResume'] = 1
        else:
            filled_in['WordResume'] = ""
        filled_in['Company'] = "%s" %self.Company_Entry.text()
        filled_in['CompanyDescription'] = "%s" %self.CompanyDesc_Entry.text()
        filled_in['EmailSubject'] = "%s" %self.EmailSubject_Entry.text()
        filled_in['RA'] = "%s" %self.RA_fill.text()


        return filled_in

    def clear_unfilled_form(self):
        self.Occupation_Entry = QtGui.QLineEdit()
        self.ToAddress_Entry = QtGui.QLineEdit()
        self.Company_Entry = QtGui.QLineEdit()
        self.CompanyDesc_Entry = QtGui.QLineEdit()
        self.EmailSubject_Entry = QtGui.QLineEdit()
        self.unfilled_layout.addWidget(self.Occupation_Entry, 2, 1)
        self.unfilled_layout.addWidget(self.ToAddress_Entry, 3, 1)
        self.unfilled_layout.addWidget(self.Company_Entry, 4, 1)
        self.unfilled_layout.addWidget(self.CompanyDesc_Entry, 5, 1)
        self.unfilled_layout.addWidget(self.EmailSubject_Entry, 6, 1)
        self.Approved_Answer.setChecked(False)
        self.WordResume_Answer.setChecked(False)
        self.checkbox_layout.addWidget(self.Approved_Answer, 1, 1)
        self.checkbox_layout.addWidget(self.WordResume_Answer, 1, 3)
        self.setLayout(self.main_layout)


    def filled_form(self):
        filled_layout = QtGui.QGridLayout()
        filled_layout.setSpacing(10)

        filled_layout.addWidget(self.CL_ID, 1, 0)
        filled_layout.addWidget(self.CL_fill, 1, 1)
        filled_layout.addWidget(self.Month, 2, 0)
        filled_layout.addWidget(self.Month_Fill, 2, 1)
        filled_layout.addWidget(self.Day, 3, 0)
        filled_layout.addWidget(self.Day_Fill, 3, 1)
        filled_layout.addWidget(self.State, 4, 0)
        filled_layout.addWidget(self.State_Fill, 4, 1)
        filled_layout.addWidget(self.RA, 5, 0)
        filled_layout.addWidget(self.RA_fill, 5, 1)

        return filled_layout


    def unfilled_form(self):
        self.unfilled_layout = QtGui.QGridLayout()
        self.unfilled_layout.setSpacing(10)

        self.Occupation = QtGui.QLabel("Occupation")
        self.Occupation_Entry = QtGui.QLineEdit()
        self.ToAddress = QtGui.QLabel("ToAddress")
        self.ToAddress_Entry = QtGui.QLineEdit()
        self.Company = QtGui.QLabel("Company")
        self.Company_Entry = QtGui.QLineEdit()
        self.CompanyDesc = QtGui.QLabel("Company Description")
        self.CompanyDesc_Entry = QtGui.QLineEdit()
        self.EmailSubject = QtGui.QLabel("EmailSubject")
        self.EmailSubject_Entry = QtGui.QLineEdit()
        self.get_ToAddress = QtGui.QPushButton("Get ToAddress")
        self.get_ToAddress.clicked.connect(self.parent.load_toAddress)
        self.unfilled_layout.addWidget(self.Occupation, 2, 0)
        self.unfilled_layout.addWidget(self.Occupation_Entry, 2, 1)
        self.unfilled_layout.addWidget(self.ToAddress, 3, 0)
        self.unfilled_layout.addWidget(self.ToAddress_Entry, 3, 1)
        self.unfilled_layout.addWidget(self.get_ToAddress, 3, 2)
        self.unfilled_layout.addWidget(self.Company, 4, 0)
        self.unfilled_layout.addWidget(self.Company_Entry, 4, 1)
        self.unfilled_layout.addWidget(self.CompanyDesc, 5, 0)
        self.unfilled_layout.addWidget(self.CompanyDesc_Entry, 5, 1)
        self.unfilled_layout.addWidget(self.EmailSubject, 6, 0)
        self.unfilled_layout.addWidget(self.EmailSubject_Entry, 6, 1)

        return self.unfilled_layout

    def boolean_form(self):
        self.checkbox_layout = QtGui.QGridLayout()
        self.checkbox_layout.setSpacing(10)
        self.Approved = QtGui.QLabel("Job Criteria Met")
        self.Approved_Answer = QtGui.QCheckBox()
        self.WordResume = QtGui.QLabel("WordResume")
        self.WordResume_Answer = QtGui.QCheckBox()

        self.checkbox_layout.addWidget(self.Approved, 1, 0)
        self.checkbox_layout.addWidget(self.Approved_Answer, 1, 1)
        self.checkbox_layout.addWidget(self.WordResume, 1, 2)
        self.checkbox_layout.addWidget(self.WordResume_Answer, 1, 3)

        return self.checkbox_layout
    def url_dropdown(self):
        url_layout = QtGui.QGridLayout()
        URL = QtGui.QLabel("URLs")
        self.nextAd = QtGui.QPushButton("Load Next Ad")
        self.nextAd.clicked.connect(self.load_next_url)
        self.choosebutton = QtGui.QPushButton("Load Chosen Ad")
        self.choosebutton.clicked.connect(self.load_chosen_url)
        self.SaveEntry = QtGui.QPushButton("Save Current Entry")
        self.SaveEntry.clicked.connect(self.parent.get_entries)

        if self.parent.CSV_Loaded == 0:
            self.comboBox = QtGui.QComboBox(self)
            self.comboBox.addItem("")
            self.nextAd.setEnabled(False)
            self.choosebutton.setEnabled(False)
            url_layout.addWidget(URL, 1, 0)
            url_layout.addWidget(self.comboBox, 1, 1)
            url_layout.addWidget(self.choosebutton, 1, 2)
            url_layout.addWidget(self.nextAd, 2, 2)
            url_layout.addWidget(self.SaveEntry, 2, 1)




        if self.parent.CSV_Loaded == 1:
            urls = self.parent.urls
            self.comboBox = QtGui.QComboBox(self)
            self.URL_num = QtGui.QLineEdit(str(self.curr_url_index))
            self.URL_num.setFixedWidth(50)
            for i in urls:
                self.comboBox.addItem(i)
            self.nextAd.setEnabled(True)
            self.choosebutton.setEnabled(True)
            self.url_menu.addWidget(URL, 1, 0)
            self.url_menu.addWidget(self.URL_num, 2,0)
            self.url_menu.addWidget(self.comboBox, 1, 1)
            self.url_menu.addWidget(self.choosebutton, 1, 2)
            self.url_menu.addWidget(self.nextAd, 2, 2)
            self.setLayout(self.main_layout)
            first_url = (self.comboBox.currentText())
            self.parent.load_url(first_url)


        return url_layout

    def update_url_num(self):
        self.URL_num = QtGui.QLineEdit(str(self.curr_url_index))
        self.URL_num.setFixedWidth(50)
        self.url_menu.addWidget(self.URL_num, 2, 0)
        self.setLayout(self.main_layout)


    def load_chosen_url(self):
        self.parent.start = 0
        url = self.comboBox.currentText()
        url_index = self.comboBox.currentIndex()
        self.set_filled_vals(url_index)
        self.parent.load_url(url)
        self.curr_url_index = url_index
        self.clear_unfilled_form()
        self.update_url_num()
        self.parent.onMain = 1


    def load_next_url(self):
        self.parent.start = 0
        url_index1 = self.comboBox.currentIndex()
        url1 = (self.comboBox.currentText())
        self.comboBox.setCurrentIndex(url_index1+1)
        url_index2 = self.comboBox.currentIndex()
        self.curr_url_index = url_index2
        self.update_url_num()
        url2 = (self.comboBox.currentText())
        self.clear_unfilled_form()
        self.set_filled_vals(url_index2)
        self.parent.load_url(url2)
        self.parent.onMain = 1












class UrlInput(QtGui.QLineEdit):
    def __init__(self, browser, parent = None):
        super(UrlInput, self).__init__()
        self.browser = browser
        self.returnPressed.connect(self._return_pressed)
        self.goingToReply = 0


    def _return_pressed(self):
        url = QtCore.QUrl(self.text())
        self.browser.load(url)
    def customuseragent(self, url):
        print 'called for %s' % url
        return 'custom ua'

    def url_chosen(self, url):
        self.goingToReply = 0
        USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1"
        self.request = QtNetwork.QNetworkRequest()
        self.request.setUrl(QtCore.QUrl(url))
        self.request.setRawHeader("User-Agent",USER_AGENT)
        self.browser.page().userAgentForURL = self.customuseragent
        self.browser.load(self.request)

    def get_save_name(self):
        element = self.browser.page().currentFrame().documentElement()
        Element_Search = element.findFirst('#titletextonly')
        titlewcss = "%s" %Element_Search.toOuterXml()
        title_only = re.search('>(.*)<',titlewcss)
        self.save_name = title_only.group(1)







def main():
    app = QtGui.QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_())

main()
