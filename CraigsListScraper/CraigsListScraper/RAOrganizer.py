from collections import  defaultdict
from csv import DictReader
import pandas as pd


class RAAssignment(object):
    def __init__(self, RA):
        self.RA = RA
        self.URL_Container = []
        self.URL_Table = pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/all_URLS_Indexed.csv')
        self.RA_Table = pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/RA_Mapping.csv')

    def GetRAIndices(self):
        #Get indice of RA
        RA_Indice = 0
        for i in range(len(self.RA_Table.RA)):
            if self.RA_Table.RA[i] == self.RA:
                RA_Indice = i
        #Get indice of Job and indices of URLs
        Indice_list = []
        for i in self.RA_Table.iloc[RA_Indice]:
            if type(i) != str and i > 0:
                Indice_list.append(i)

        return Indice_list

    #Get Urls for the desired states
    def GetURLS(self):
        indices = self.GetRAIndices()
        job = indices.pop(0)
        for i in indices:
            url = self.URL_Table.iloc[i-2][str(job)]
            self.URL_Container.append(url)
    #Get state for a certain URL associated with an RA
    def getState(self, city):
        #TODO Convert it to state code
        city_indice = self.URL_Table.Region[self.URL_Table.Region == city].index.tolist() #Get the indice of the city
        state = self.URL_Table.StateCode[city_indice[0]] #Get the value of the state
        return state
    def geturlfolder(self):
        for i in range(len(self.RA)):
            RA_Name = self.RA
            if RA_Name[i] == " ":
                RA_Name[i] == "_"
                break
        RA_Name+"/"
        return RA_Name
