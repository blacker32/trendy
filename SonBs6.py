from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time
import logging
import threading

def  Deger(MerchantIdx,ProductIDx):
    
    
    headers = {
    'authority': 'public-mdc.trendyol.com',
    'accept': 'application/json',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer',
    'if-none-match': 'W/"3e07-5egCik6IqeJnm5eIo/lrYHYyu48"',
    'origin': 'https://www.trendyol.com',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    
    response = requests.get('https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/'+str(ProductIDx)+'?merchantId='+str(MerchantIdx),headers=headers)
    if response.status_code==200:
        global ToplamYorumSayisi
        global UrunDegerlendirme
        global UrunPuan
        global BesYildizCount
        global DortYildizCount
        global UcYildizCount
        global ikiyildizCount
        global biryildizCount

        s=response.json()
        results=s.get("result")
        try:
            ToplamYorumSayisi=results.get("contentSummary").get("totalCommentCount")
        except:
            ToplamYorumSayisi=0
        try:   
            UrunDegerlendirme=results.get("contentSummary").get("totalRatingCount")
        except:
            UrunDegerlendirme=0
        try:
            UrunPuan=results.get("contentSummary").get("averageRating")
        except:
            UrunPuan=0  
        try:
            BesYildizCount=results.get("contentSummary").get("ratingCounts")[0].get("count")
        except:
            BesYildizCount=0
        try:
            DortYildizCount=results.get("contentSummary").get("ratingCounts")[1].get("count")
        except:
            DortYildizCount=0
        try:
            UcYildizCount=results.get("contentSummary").get("ratingCounts")[2].get("count")
        except:
            UcYildizCount=0        
        try:
            ikiyildizCount=results.get("contentSummary").get("ratingCounts")[3].get("count")
        except:
            ikiyildizCount=0
        try:
            biryildizCount=results.get("contentSummary").get("ratingCounts")[4].get("count")
        except:
            biryildizCount=0
    
    return ToplamYorumSayisi,UrunDegerlendirme,UrunPuan,BesYildizCount,DortYildizCount,UcYildizCount,ikiyildizCount,biryildizCount

def GetUrunDetail(xmarkaAd,xproductId,xurl,xsatici_id):
    #try:
        
        r=requests.get(xurl)
        soup=BeautifulSoup(r.content,"html.parser")
        slct=soup.find('script', type='application/javascript',)
    
        try:
            urun_barcode=slct.text.split("barcode")[1].split(",")[0].split(":")[1].replace('"',"")
        except:
            urun_barcode="None"
        urun_marka_ad=xmarkaAd
        urun_Id=xproductId
        urun_url=xurl
        if soup.find(class_="sl-pn") is not None:
            satici_puan=soup.find(class_="sl-pn").text
        else:
            satici_puan=0
        if soup.find(class_="pr-new-br") is not None:
            urun_ad=soup.find(class_="pr-new-br").text
        else:
            urun_ad="None"
        if soup.find(class_="merchant-text") is not None:
            urun_satici=soup.find(class_="merchant-text").text
        else:
            urun_satici="None"
        if soup.find(class_="prc-dsc") is not None:
            satis_fiyat=soup.find(class_="prc-dsc").text.split()[0].replace(" TL","").replace(".","").replace(",",".")
        else:
            satis_fiyat=0       
        if soup.find(class_="fv-dt") is not None:
            urun_favori=str(soup.find(class_="fv-dt").text).replace(" favori","")
        else:
            urun_favori=0

        if soup.find(class_="pr-omc-tl title") is not None:
            satici_sayisi=soup.find(class_="pr-omc-tl title").text.replace("Ürünün Diğer Satıcıları (","").replace(")","")
        else:
            satici_sayisi=0
        
        urun_satici_id=xsatici_id
        urun=Deger(urun_satici_id,urun_Id) 
        urun_Toplam_yorum_sayisi=urun[0]
        urun_degerlendirme_sayisi=urun[1]
        urun_puan=urun[2]
        urun_bes=urun[3]
        urun_dort=urun[4]
        urun_uc=urun[5]
        urun_iki=urun[6]
        urun_bir=urun[7]    
        data = {
            "urun_Id":str(urun_Id),
            "satici_Id":str(urun_satici_id),
            "urun_barcode":str(urun_barcode),
            "urun_marka_ad":str(urun_marka_ad),
            "urun_ad":str(urun_ad),
            "urun_satici":str(urun_satici),
            "satici_puan":float(satici_puan),
            "satis_fiyat":float(satis_fiyat),
            "urun_favori_sayisi":int(urun_favori),
            "urun_Toplam_yorum_sayisi":int(urun_Toplam_yorum_sayisi),
            "urun_degerlendirme_sayisi":int(urun_degerlendirme_sayisi),
            "urun_puan":float(urun_puan),
            "Bes_Yildiz_Sayisi":int(urun_bes),
            "Dort_Yildiz_Sayisi":int(urun_dort),
            "Uc_Yildiz_Sayisi":int(urun_uc),
            "iki_Yildiz_Sayisi":int(urun_iki),
            "bir_Yildiz_Sayisi":int(urun_bir),
            "urun_diger_satici_sayisi":int(satici_sayisi),
            "urun_url":str(urun_url)
            }
        
    #except:
        #print("Hata")
        return data


def mainx():
    header={"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"}
    URL="https://www.trendyol.com/sr?wc=1354&prc=2000-10000&pi="
    a=0
    alldata=[]
    klink=[]
    datam=[]
    #try:
    for x in range(1,208):
        page=requests.get(URL+str(x))
        time.sleep(2)
        if  page.status_code==200:
            print(x)
            soup=BeautifulSoup(page.content,"html.parser")
            results=soup.find_all("div", class_="p-card-chldrn-cntnr card-border")
            z=0
            for job_element in results:  
                for links in job_element.find_all('a'):
                    blink="https://www.trendyol.com"+links.get('href')
                    urun_marka=links.get("href").split("/")[1]
                    merchantId=blink.split("merchantId=",1)[1]
                    productId=blink.split("-p-",1)[1].split("?")[0]
                    print(merchantId)
                    datam.append(GetUrunDetail(urun_marka,productId,blink,merchantId))
        
        else:
            print("Sayfa Yüklenmedi")  
    #except Exception as ex:
        #print("hata :"+ str(ex))
    #finally:
    return datam

mainsub=mainx()
df2=pd.DataFrame(mainsub)
print(df2)
df2.to_excel("SoNoutput.xlsx")

