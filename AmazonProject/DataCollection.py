from bs4 import BeautifulSoup
import os
import pandas as pd

data_table={'ProductTitle':[],'ProductPrice(₹)':[],'link':[]}
try:
    c=0
    for file in os.listdir("data"):
        with open(f"data/{file}","r",encoding='utf-8') as f:
            content=f.read()
        soup=BeautifulSoup(content,"lxml")
        c+=1
        # print(c)
        title_tag=soup.find("span",attrs={'class':"a-size-medium a-color-base a-text-normal"})
        Ptitle=title_tag.text
        # print(Ptitle)
        data_table['ProductTitle'].append(Ptitle)
        price_tag=soup.find('span',attrs={'class':"a-price-whole"})
        if price_tag==None:
            Pprice=("-")
        else:
            Pprice=price_tag.text
        # print(Pprice)
        data_table['ProductPrice(₹)'].append(Pprice)
        link_tag=soup.find("a",attrs={'class':"a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal"})
        if link_tag==None:
            Plink="-"
        else:
            Plink=link_tag['href']
        # print(Plink)
        data_table['link'].append(Plink)
    #making data table
    df=pd.DataFrame.from_dict(data_table)
    df.to_csv("amazon_keyboard_data.csv",index=False)
    print("file created successfully^_^")
except Exception as e:
    print(f"ERROR : {e}")