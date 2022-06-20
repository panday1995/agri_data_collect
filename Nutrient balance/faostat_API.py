

"""
Created on Jun 19 2022

@author: Fan Yang

This script 
- scraps FAOstat data from FAOstat websit (https://www.fao.org/faostat/en/#home) using bulk download
- unzip the FAOstat.zip file into a faostat folder
- unzip all the .zip files in the folder and delete .zip items

ToDo
- Organize folders into subfolders according to https://www.fao.org/faostat/en/#data

"""

from collections import Iterable
from selenium import webdriver
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

import pandas as pd
import pathlib
import os
import selenium.webdriver.support.expected_conditions as EC
import shutil
import zipfile

parent_path = pathlib.Path(__file__).parent.parent.resolve()
data_path = os.path.join(parent_path,"Nutrient balance")



# install Chrome browser webdriver
browser_driver_path = ChromeDriverManager().install() # path to browser driver for selenium

# set file path for FAOstat data download
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : data_path} # set path for download
chrome_options.add_experimental_option('prefs', prefs)

# initiate browser for use
def init_browser(website, 
                browser_driver_path = browser_driver_path, 
                chrome_options = chrome_options):
    """
    This function initiate a browser object to open a website

    Parameters
    ----------
    webiste: str, the website to be open
    browser_driver_path: str, the path to browser driver
    chrome_options: object, webdriver object to define default downloading path
    """
    browser = webdriver.Chrome(service=Service(browser_driver_path),options=chrome_options)
    browser.get(website)
    return browser

browser = init_browser("https://www.fao.org/faostat/en/#home")

try:
    # wait maximum 15 seconds until the download button is available
    element = WebDriverWait(browser, 15).until(
        # find element "FAOSTAT" by xpath and click
        EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[1]/div/div[1]/i"))
    )
    element.click()
except:
    browser.quit()

# go to the data
FAO_zip = "FAOSTAT.zip"
time = 0
# unzip the FAOSTAT.zip file
while FAO_zip not in os.listdir(data_path): # check if FAO_zip is downloaded
    sleep(10) # if not, wait for 5 seconds
    time = time+10
    print("FAOSTAT downloading, {:.1f}s".format(time))
else: # if yes, unzip the file
    handle = zipfile.ZipFile(FAO_zip)
    faostat_unzip = os.path.join(data_path,"faostat")
    handle.extractall(os.path.join(faostat_unzip)) # extract the files into a "faostat" folder
    handle.close()
    os.remove(FAO_zip) # remove the zip file

# go to the unzipped folder and unzip all the files inside
zip_ls = os.chdir(faostat_unzip)
extension = ".zip"

for item in os.listdir(zip_ls): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(item[:-4]) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file

# organize folders into subfolders
        # browser = init_browser("https://www.fao.org/faostat/en/#data")
# create dict match subfolder with the first world of FAO original subfolder names
category_dict = {"Production":["Production","Value"],
                "Food Security and Nutrition":["Food"],
                "Food Balances":["SUA", "FoodBalanceSheetsHistoric","FoodBalanceSheets", "CommodityBalances"],
                "Trade":["Trade",],
                "Prices":["Prices","PricesArchive",'Deflators','Exchange'],
                "Land, Inputs and Sustainability":["Inputs","Environment"],
                "Population and Employment":["Population",'Employment'],
                "Investment":["Investment"],
                "Macro-Economic Indicators":["Macro-Statistics"],
                "Climate Change":["Emissions"],
                "Forestry":["Forestry","Forestal"],
                "SDG Indicators":["SDG"],
                "World Census of Agriculture":["World"],
                "Discontinued archives and data series":["ASTI","Indicators"],}
pair = {value: key
            for key, values in category_dict.items() 
            for value in values}

# create subfolders corresponding to FAO categories
for key in category_dict:
    if not os.path.exists(key):
        os.makedirs(key)

#Traverses every folder
folder_ls = [folder for folder in os.listdir(faostat_unzip) if folder not in pair.values()]
for folder in folder_ls:
    first_word = folder.split("_")[0] # find the first word of a FAOstat folder
    if first_word in pair.keys():
        shutil.move(faostat_unzip+'/'+folder,faostat_unzip+'/'+pair[first_word]+'/'+folder)


os.chdir("../../")



