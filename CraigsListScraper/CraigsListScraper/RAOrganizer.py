from collections import  defaultdict
from csv import DictReader
import pandas as pd
import re
import collections
import os



class RAAssignment(object):
    def __init__(self, RA):
        self.RA = RA
        self.URL_Container = []
        indexed_urls_path = os.path.join(os.getcwd(),'Data','all_URLS_Indexed.csv' )
        RA_Table_path = os.path.join(os.getcwd(), 'Data', 'RA_Mapping.csv')
        self.URL_Table = pd.read_csv(indexed_urls_path)
        self.RA_Table = pd.read_csv(RA_Table_path)
        self.url_RA_map = defaultdict(list)

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

    def get_all_urls_map_RA(self):
        RA_Table = self.RA_Table
        RAs = RA_Table["RA"].tolist()
        RAlist = []
        for index, RA in enumerate(RAs):
            RAlist.append(RAAssignment(RA))
            RAlist[index].GetURLS()
        all_urls = []
        for i in RAlist:
            RA_Urls = []
            twojobs = False
            name = i.RA
            RE_D = re.compile('\d')
            if RE_D.search(name) is not None:
                name = name[:-1]
                twojobs = True
            elif RE_D.search(name) is None:
                name = name
            for j in i.URL_Container:
                if j not in all_urls:
                    all_urls.append(j)
                    RA_Urls.append(j)
                else:
                    RA_Urls.append(j)
            if twojobs == False:
                self.url_RA_map[name] = RA_Urls #Add list of RA's assocaited with RA to map
            if twojobs == True:
                self.url_RA_map[name].extend(RA_Urls) #If RA has more than one job, extend their total amount of urls


        return all_urls

    def get_RAS_with_shared(self):
        urls = []
        for key, values in self.url_RA_map.items():
            urls.extend(values)
        shared = [item for item, count in collections.Counter(urls).items() if count > 1]
        shared_regions = defaultdict(list)
        for key, values in self.url_RA_map.items():
            for i in values:
                if i in shared:
                    shared_regions[i].append(key)
        return shared_regions


    def get_RA_by_URL(self, url):
        shared = self.get_RAS_with_shared()
        if url in shared.keys():
            RA = random.choice(shared[url])
        else:
            for key, values in self.url_RA_map.items():
                for i in values:
                    if i == url:
                        RA = key
        return RA
