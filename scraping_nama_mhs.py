import requests, re, argparse, logging
import pandas as pd
from bs4 import BeautifulSoup

class Scraping_Data_Mahasiswa():
    def __init__ (self, urltxt, fileout):
        self.filename=urltxt
        self.fileout=fileout

    def scraping_link_univ(self, url):
        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features="lxml")
        all_link=[]
        regrex=r'detail'
        for link in soup.find_all('a'):
            if(link.get('href')!=None):
                if(re.search(regrex, link.get('href'))!=None):
                    all_link.append(link.get('href'))
        return all_link

    def scraping_detail_semester(self, url):
        regrex1=r'detailsemester'
        all_link_mhs=[]
        r1  = requests.get(url)
        data1 = r1.text
        soup1 = BeautifulSoup(data1, features="lxml")
        for link in soup1.find_all('a'):
            if(link.get('href')!=None):
                if(re.search(regrex1, link.get('href'))!=None):
                    all_link_mhs.append(link.get('href'))
        return all_link_mhs

    def scraping_detail_mhs(self, url):
        all_link_mhs_detail=[]
        r2  = requests.get(url)
        data2 = r2.text
        soup2 = BeautifulSoup(data2, features="lxml")
        regrex=r'detail\b'
        for link in soup2.find_all('a'):
            if(link.get('href')!=None):
                if(re.search(regrex, link.get('href'))!=None):
                    all_link_mhs_detail.append(link.get('href'))
        return all_link_mhs_detail

    def get_data(self, url):
        r3  = requests.get(url)
        data3 = r3.text
        soup3 = BeautifulSoup(data3, 'html.parser')
        content_name = soup3.findChildren('table', attrs={'class': 'table1'})
        my_table = content_name[0]
        name=str(my_table.findChildren(['td'])[2])
        name=name.split('>')[1].split('<')[0]
        gender=str(my_table.findChildren(['td'])[5])
        gender=gender.split('>')[1].split('<')[0]
        return name, gender

    def scrap(self):
        print('mulai')
        df=pd.DataFrame(columns=['nama','gender'])
        f = open(self.filename, 'r')
        url_list=[x.replace('\n','') for x in f]
        # print(url_list)
        count=0
        for url in url_list:
            count+=1
            print('LIST UNIVERSITAS KE-',count)
            list1=self.scraping_link_univ(url)
            for i in list1:
                try :
                    list_j=self.scraping_detail_semester(i)
                    j=list_j[round(len(list_j)/2)]
                    for k in self.scraping_detail_mhs(j):
                        try:
                            name, gender=self.get_data(k)
                            df.loc[len(df),:]=name, gender
                            print(str(len(df))+'.', name, gender)
                        except:
                            print('FAILED', k)
                            pass
                except:
                    pass
                    print('pass')
        df.to_csv(self.fileout+'.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='example: python scraping_nama_mhs.py -fn url.txt -fo hasil_scrap')
    parser.add_argument('-fn', '--filename', help='filename of university url', default='url.txt', type=str)
    parser.add_argument('-fo', '--fileoutput', help="output filrname (don't need to give exstention", default="hasil_scraping", type=str)
    args = parser.parse_args()
    scraping=Scraping_Data_Mahasiswa(urltxt=args.filename, fileout=args.fileoutput)
    scraping.scrap()