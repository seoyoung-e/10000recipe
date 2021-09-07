# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from time import sleep
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
import re
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path = '/Users/nang/Desktop/ML/chromedriver', options=options)

# 레시피 링크, 레시피 제목, 레시피 넘버, 인분, 소요시간, 난이도
titles, links, nums, servings, tot_times, levels = [], [], [], [], [], []
ingredients = [] # 레시피 재료

# +
start = time.time()
for i in range(600,601):
    for j in range(1,45): ## 한페이지당 레시피 40개, 광고 4개
        url = f'https://www.10000recipe.com/recipe/list.html?order=date&page={i}'
        driver.get(url)
        try:
            driver.find_element_by_css_selector(f'#contents_area_full > ul > ul >\
                    li:nth-child({j}) > div.common_sp_thumb > a > img').click()
            time.sleep(np.random.randint(2,5))
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            try:
                # 레시피명
                title = soup.find('div','view2_summary st3').find('h3').text
                titles.append(title)
            
            except NoSuchElementException:
                titles.append("null")
            
            try:
                # 레시피 링크
                link = soup.find('head').find('link',rel = 'canonical').attrs['href']
                links.append(link)
                num = link.split('/')[4]
                nums.append(num)
                
            except NoSuchElementException:
                links.append("null")
                nums.append('null')
                
            try:
                # 인분
                serving = soup.find('div','view2_summary_info').select('span')[0].text
                servings.append(serving)
                
            except (NoSuchElementException,IndexError):
                servings.append("null")
                
                
            try:    
                # 소요시간
                tot_time = soup.find('div','view2_summary_info').select('span')[1].text
                tot_times.append(tot_time)
            
            except (NoSuchElementException,IndexError):
                tot_times.append("null")
                
            try:
                # 난이도
                level = soup.find('div','view2_summary_info').select('span')[2].text
                levels.append(level)
            
            except (NoSuchElementException,IndexError):
                levels.append("null")
            
            try:
                # 재료
                ingredient = soup.find('div','cont_ingre').text.replace('\n','').replace(' ','')
                ingredients.append(ingredient)
                
            except AttributeError:
                # 다른 재료 포맷
                str_ing = soup.find('div','ready_ingre3').text.replace('\n',' ')
                rm_btwspace = ','.join(str_ing.split())  
                ingredients.append(rm_btwspace)
                 
            except NoSuchElementException:
                ingredients.append("null")
            
        except (NoSuchElementException, UnexpectedAlertPresentException):
            pass
        
        
        time.sleep(1)

print('time: ', time.time() - start)
# -

ny_recipe = pd.DataFrame({'레시피명': titles,
                          'Index': nums,
                          '레시피링크': links,
                          '소요시간': tot_times,
                          '인분': servings,
                          '난이도': levels,
                          '재료': ingredients})

# 마지막부분 확인하기
ny_recipe.iloc[-1,:]

ny_recipe.to_excel('501~600페이지.xlsx')

# +

del links[0:3987]
del tot_times[0:3987]
del nums[0:3987]
del servings[0:3987]
del ingredients[0:3987]
del levels[0:3987]
# -

len(titles)

len(titles)

len(links)

len(tot_times)

len(nums)

len(servings)

len(ingredients)

len(levels)

len(ny_recipe)

i

j

#
