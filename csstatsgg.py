# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 22:00:14 2024

@author: Klavs
"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import asyncio
import pandas as pd
import datetime as dt
import re
import time

async def get_result(bet_time):

    driver = webdriver.Chrome()
    
    driver.get("https://csstats.gg/player/76561198880591506#/matches")
    
    await asyncio.sleep(3)
    
    actions = ActionChains(driver)
    actions.move_by_offset(500, 900).click().perform()
    
    await asyncio.sleep(3)
    
    driver.find_element(By.XPATH, '//*[@id="match-list-outer"]/table/tbody/tr[1]').click()
    await asyncio.sleep(2)
    match_date = driver.find_element(By.XPATH, '//*[@id="last-info"]/div[1]/span[2]').text
    match_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', match_date)
    match_date = dt.datetime.strptime(match_date, '%d %b %Y %H:%M:%S') + dt.timedelta(hours = 3)
    
    
    
    if (bet_time - match_date).days == 0 or bet_time < match_date:
        time_diff = (bet_time - match_date).seconds / 60
        if time_diff < 24 or bet_time < match_date:
    
    
            driver.back()
            await asyncio.sleep(2)
            
            table_xpath = '//*[@id="match-list-outer"]/table'
            table = driver.find_element(By.XPATH, table_xpath)
            
            rows = table.find_elements(By.TAG_NAME, 'tr')
            rows = rows[0:2]
            
            header = table.find_elements(By.TAG_NAME, 'th')
            header_data = [h.text for h in header] 
            
            data = []
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                # If there are cells, extract their text
                if cells:
                    row_data = [cell.text for cell in cells]
                    data.append(row_data)
            
            driver.close()
            
            df = pd.DataFrame(data)
            df.columns = header_data
            score = df['Score'].values[0]
            score = score.split(':')
            if int(score[0]) > int(score[1]):
                score = 'W'
                return score
            elif int(score[0]) == int(score[1]):
                score = 'D'
                return score
            elif int(score[0]) < int(score[1]):
                score = 'L'
                return score
        elif time_diff > 24 and time_diff < 60:
            score = 'DQ'
            driver.close()
            return score
        
        elif time_diff > 60:
            score = 'Pending'
            driver.close()
    
    else:
        score = 'Pending'
        driver.close()

    return score
        
def get_result_debug(bet_time):
    
    driver = webdriver.Chrome()
    
    driver.get("https://csstats.gg/player/76561198880591506#/matches")
    
    time.sleep(3)
    
    actions = ActionChains(driver)
    actions.move_by_offset(500, 900).click().perform()
    
    time.sleep(3)
    
    driver.find_element(By.XPATH, '//*[@id="match-list-outer"]/table/tbody/tr[1]').click()
    time.sleep(2)
    match_date = driver.find_element(By.XPATH, '//*[@id="last-info"]/div[1]/span[2]').text
    match_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', match_date)
    match_date = dt.datetime.strptime(match_date, '%d %b %Y %H:%M:%S') + dt.timedelta(hours = 3)
    print(match_date)
    print(bet_time)
    print((bet_time - match_date))
    
    
    if (bet_time - match_date).days == 0 or bet_time < match_date :
        time_diff = (bet_time - match_date).seconds / 60
        if time_diff < 24 or bet_time < match_date:
    
    
            driver.back()
            time.sleep(2)
            
            table_xpath = '//*[@id="match-list-outer"]/table'
            table = driver.find_element(By.XPATH, table_xpath)
            
            rows = table.find_elements(By.TAG_NAME, 'tr')
            rows = rows[0:2]
            
            header = table.find_elements(By.TAG_NAME, 'th')
            header_data = [h.text for h in header] 
            
            data = []
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells:
                    row_data = [cell.text for cell in cells]
                    data.append(row_data)
            
            driver.close()
            
            df = pd.DataFrame(data)
            df.columns = header_data
            score = df['Score'].values[0]
            score = score.split(':')
            print(score[0])
            print(score[1])
            print(int(score[0])>int(score[1]))
            if int(score[0]) > int(score[1]):
                score = 'W'
                return score
            elif int(score[0]) == int(score[1]):
                score = 'D'
                return score
            elif int(score[0]) < int(score[1]):
                score = 'L'
                return score
        elif time_diff > 24 and time_diff < 60:
            score = 'DQ'
            driver.close()
            return score
        
        elif time_diff > 60:
            score = 'Pending'
            driver.close()
    
    else:
        score = 'Pending'
        driver.close()

    return score

async def get_result_over(bet_time, betmetric):

    os.chdir(r"C:\Programs and Games\betting bot")
    
    driver = webdriver.Chrome()
    
    driver.get("https://csstats.gg/player/76561198880591506#/matches")
    
    await asyncio.sleep(3)
    
    actions = ActionChains(driver)

    actions.move_by_offset(500, 900).click().perform()
    
    await asyncio.sleep(3)
    
    driver.find_element(By.XPATH, '//*[@id="match-list-outer"]/table/tbody/tr[1]').click()
    await asyncio.sleep(2)
    match_date = driver.find_element(By.XPATH, '//*[@id="last-info"]/div[1]/span[2]').text
    match_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', match_date)
    match_date = dt.datetime.strptime(match_date, '%d %b %Y %H:%M:%S') + dt.timedelta(hours = 3)
    
    
    
    if (bet_time - match_date).days == 0 or bet_time < match_date:
        time_diff = (bet_time - match_date).seconds / 60
        if time_diff < 24 or bet_time < match_date:
    
    
            driver.back()
            await asyncio.sleep(2)
            
            table_xpath = '//*[@id="match-list-outer"]/table'
            table = driver.find_element(By.XPATH, table_xpath)
            
            rows = table.find_elements(By.TAG_NAME, 'tr')
            rows = rows[0:2]
            
            header = table.find_elements(By.TAG_NAME, 'th')
            header_data = [h.text for h in header] 
            
            data = []
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells:
                    row_data = [cell.text for cell in cells]
                    data.append(row_data)
            
            driver.close()
            
            df = pd.DataFrame(data)
            df.columns = header_data
            score = df[betmetric].values[0]
            score = float(score)
            return score
        
        elif time_diff > 24 and time_diff < 60:
            score = 'DQ'
            driver.close()
            return score
        
        elif time_diff > 60:
            score = 'Pending'
            driver.close()
    
    else:
        score = 'Pending'
        driver.close()

    return score

def get_result_over_debug(bet_time, betmetric):

    os.chdir(r"C:\Programs and Games\betting bot")
    
    driver = webdriver.Chrome()
    
    driver.get("https://csstats.gg/player/76561198880591506#/matches")
    
    time.sleep(3)
    
    actions = ActionChains(driver)
    actions.move_by_offset(500, 900).click().perform()
    
    time.sleep(3)
    
    driver.find_element(By.XPATH, '//*[@id="match-list-outer"]/table/tbody/tr[1]').click()
    time.sleep(2)
    match_date = driver.find_element(By.XPATH, '//*[@id="last-info"]/div[1]/span[2]').text
    match_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', match_date)
    match_date = dt.datetime.strptime(match_date, '%d %b %Y %H:%M:%S') + dt.timedelta(hours = 3)
    
    
    
    if (bet_time - match_date).days == 0 or bet_time < match_date:
        time_diff = (bet_time - match_date).seconds / 60
        if time_diff < 24 or bet_time < match_date:
    
    
            driver.back()
            time.sleep(2)
            
            table_xpath = '//*[@id="match-list-outer"]/table'
            table = driver.find_element(By.XPATH, table_xpath)
            
            rows = table.find_elements(By.TAG_NAME, 'tr')
            rows = rows[0:2]
            
            header = table.find_elements(By.TAG_NAME, 'th')
            header_data = [h.text for h in header] 
            
            data = []
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells:
                    row_data = [cell.text for cell in cells]
                    data.append(row_data)
            
            driver.close()
            
            df = pd.DataFrame(data)
            df.columns = header_data
            score = df[betmetric].values[0]
            score = float(score)
            return score
        
        elif time_diff > 24 and time_diff < 60:
            score = 'DQ'
            driver.close()
            return score
        
        elif time_diff > 60:
            score = 'Pending'
            driver.close()
    
    else:
        score = 'Pending'
        driver.close()

    return score