import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtWebKit import QWebView, QWebPage
import csv



class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Craigslist Collection Tool")
        self.Menu_Options() #Initialize Menu
        self.CSVFile = {}
        self.CSV_Loaded = 0
        self.start = 1

        self.current_len = self.__len__(self.CSVFile)
        self.entry = EntryForm(self) #Entry form for data


        _widget = QWidget()

        browser = QWebView()


        self.url_input = UrlInput(browser) #Initialize url input

        self.layout = QVBoxLayout(_widget) #Initialuze Vertical Layout

        self.layout.addWidget(self.url_input) #Add url Input widget

        self.layout.addWidget(browser) #Add Browser Widget

        self.layout.addWidget(self.entry) #Add Entry form Widget

        self.savepath = None
        self.setCentralWidget(_widget)
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
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close_application)
        importAction = QAction('&Import CSV', self)
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
        name = QFileDialog.getOpenFileName(self, 'Import CSV')
        csv_filled = self.load_csv(name)

        self.CSVFile = csv_filled

        self.current_len = len(self.CSVFile)

        self.setLoadedFile()



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

    def get_entries(self):
        values = self.entry.get_filled_in_values()

        if values['Approved'] == 0:
            pass
        if values['Approved'] == 1:
            print("Here")
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



    def save_good_entry(self, entry):
        if self.savepath is None:
            self.savepath = QFileDialog.getOpenFileName(
                    self, 'Save File', '', 'CSV(*.csv)')
        else:
            self.savepath = self.savepath

        with open(self.savepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(entry)






class EntryForm(QWidget):
    def __init__(self, parent = None):
        super(EntryForm, self).__init__()
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(10)
        self.parent = parent
        self.set_filled_vals()
        self.filled_fields()
        unfilled = self.unfilled_form()
        self.filled = self.filled_form()
        checkbox_layout = self.boolean_form()
        self.url_menu = self.url_dropdown()
        self.main_layout.addLayout(checkbox_layout, 1, 0)
        self.main_layout.addLayout(self.url_menu, 1, 1)
        self.main_layout.addLayout(self.filled, 2, 0)
        self.main_layout.addLayout(unfilled, 2, 1)
        self.setLayout(self.main_layout)
        self.nextAd.clicked.connect(self.load_next_url)


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

            self.CL_ID = QLabel("CL_ID")
            self.CL_fill = QLineEdit("")
            self.CL_fill.setReadOnly(True)
            self.Month = QLabel("Month")
            self.Month_Fill = QLineEdit("")
            self.Month_Fill.setReadOnly(True)
            self.Day = QLabel("Day")
            self.Day_Fill = QLineEdit("")
            self.Day_Fill.setReadOnly(True)
            self.State = QLabel("State")
            self.State_Fill = QLineEdit("")
            self.State_Fill.setReadOnly(True)
            self.RA = QLabel("RA")
            self.RA_fill = QLineEdit("")
            self.RA_fill.setReadOnly(True)
        if self.parent.CSV_Loaded == 1:
            self.CL_ID = QLabel("CL_ID")
            self.CL_fill = QLineEdit(self.CL_IDVal)
            self.CL_fill.setReadOnly(True)
            self.Month = QLabel("Month")
            self.Month_Fill = QLineEdit(self.MonthVal)
            self.Month_Fill.setReadOnly(True)
            self.Day = QLabel("Day")
            self.Day_Fill = QLineEdit(self.DayVal)
            self.Day_Fill.setReadOnly(True)
            self.State = QLabel("State")
            self.State_Fill = QLineEdit(self.StateVal)
            self.State_Fill.setReadOnly(True)
            self.RA = QLabel("RA")
            self.RA_fill = QLineEdit(self.RAVal)
            self.RA_fill.setReadOnly(True)
            self.update_filled_form()


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








    def filled_form(self):
        filled_layout = QGridLayout()
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
        unfilled_layout = QGridLayout()
        unfilled_layout.setSpacing(10)

        self.Occupation = QLabel("Occupation")
        self.Occupation_Entry = QLineEdit()
        self.ToAddress = QLabel("ToAddress")
        self.ToAddress_Entry = QLineEdit()
        self.Company = QLabel("Company")
        self.Company_Entry = QLineEdit()
        self.CompanyDesc = QLabel("Company Description")
        self.CompanyDesc_Entry = QLineEdit()
        self.EmailSubject = QLabel("EmailSubject")
        self.EmailSubject_Entry = QLineEdit()

        unfilled_layout.addWidget(self.Occupation, 2, 0)
        unfilled_layout.addWidget(self.Occupation_Entry, 2, 1)
        unfilled_layout.addWidget(self.ToAddress, 3, 0)
        unfilled_layout.addWidget(self.ToAddress_Entry, 3, 1)
        unfilled_layout.addWidget(self.Company, 4, 0)
        unfilled_layout.addWidget(self.Company_Entry, 4, 1)
        unfilled_layout.addWidget(self.CompanyDesc, 5, 0)
        unfilled_layout.addWidget(self.CompanyDesc_Entry, 5, 1)
        unfilled_layout.addWidget(self.EmailSubject, 6, 0)
        unfilled_layout.addWidget(self.EmailSubject_Entry, 6, 1)

        return unfilled_layout

    def boolean_form(self):
        checkbox_layout = QGridLayout()
        checkbox_layout.setSpacing(10)
        self.Approved = QLabel("Job Criteria Met")
        self.Approved_Answer = QCheckBox()
        self.WordResume = QLabel("WordResume")
        self.WordResume_Answer = QCheckBox()

        checkbox_layout.addWidget(self.Approved, 1, 0)
        checkbox_layout.addWidget(self.Approved_Answer, 1, 1)
        checkbox_layout.addWidget(self.WordResume, 1, 2)
        checkbox_layout.addWidget(self.WordResume_Answer, 1, 3)

        return checkbox_layout
    def url_dropdown(self):
        url_layout = QGridLayout()
        URL = QLabel("URLs")
        self.nextAd = QPushButton("Load Next Ad")
        self.nextAd.clicked.connect(self.load_next_url)
        self.choosebutton = QPushButton("Load Chosen Ad")
        self.choosebutton.clicked.connect(self.load_chosen_url)
        self.SaveEntry = QPushButton("Save Current Entry")
        self.SaveEntry.clicked.connect(self.parent.get_entries)

        if self.parent.CSV_Loaded == 0:
            self.comboBox = QComboBox(self)
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
            self.comboBox = QComboBox(self)
            for i in urls:
                self.comboBox.addItem(i)
            self.nextAd.setEnabled(True)
            self.choosebutton.setEnabled(True)
            self.url_menu.addWidget(URL, 1, 0)
            self.url_menu.addWidget(self.comboBox, 1, 1)
            self.url_menu.addWidget(self.choosebutton, 1, 2)
            self.url_menu.addWidget(self.nextAd, 2, 2)
            self.setLayout(self.main_layout)
            first_url = (self.comboBox.currentText())
            self.parent.load_url(first_url)


        return url_layout



    def load_chosen_url(self):
        self.parent.start = 0
        url = self.comboBox.currentText()
        url_index = self.comboBox.currentIndex()
        self.set_filled_vals(url_index)
        self.parent.load_url(url)


    def load_next_url(self):
        self.parent.start = 0
        url_index1 = self.comboBox.currentIndex()
        url1 = (self.comboBox.currentText())
        self.comboBox.setCurrentIndex(url_index1+1)
        url_index2 = self.comboBox.currentIndex()
        url2 = (self.comboBox.currentText())
        self.set_filled_vals(url_index2)
        self.parent.load_url(url2)












class UrlInput(QLineEdit):
    def __init__(self, browser):
        super(UrlInput, self).__init__()
        self.browser = browser
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        url = QUrl(self.text())
        self.browser.load(url)

    def url_chosen(self, url):
        url = QUrl(url)
        self.browser.load(url)




def main():
    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_())

main()
