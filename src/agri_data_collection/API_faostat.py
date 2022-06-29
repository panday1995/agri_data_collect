
"""API to scrap FAOstat data

Created on Jun 19 2022
@author: Fan Yang

This script 
- scraps FAOstat data from FAOstat websit (https://www.fao.org/faostat/en/#home) using bulk download
- unzip the FAOstat.zip file into a faostat folder
- unzip all the .zip files in the folder and delete .zip items
- Organize folders into subfolders according to https://www.fao.org/faostat/en/#data

"""

from selenium import webdriver
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

import pytest
import pandas as pd
import pathlib
import os
import selenium.webdriver.support.expected_conditions as EC
import shutil
import zipfile


parent_path = pathlib.Path(__file__).parent.parent.parent.resolve()

data_path = os.path.join(parent_path,"data")

faostat_dir_name = "faostat"

faostat_unzip = os.path.join(data_path,faostat_dir_name)
FAO_zip = "FAOSTAT.zip"
FAO_zip_path = os.path.join(data_path, FAO_zip)
data_dir = os.path.join(parent_path,"data")
# faostat_final_path = os.path.join(data_dir,faostat_dir_name)

# install Chrome browser webdriver
browser_driver_path = ChromeDriverManager().install() # path to browser driver for selenium

# set file path for FAOstat data download
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : data_path} # set path for download
chrome_options.add_experimental_option('prefs', prefs)
website = "https://www.fao.org/faostat/en/#home"

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

def down_FAOstat(website = website):
    """
    This function is used to bulk download FAOstat data

    Parameters
    ----------
    webiste: str, the website to be open

    return
    ---------
    broswer: object, a browser object
    """
    browser = init_browser(website)

    # wait maximum 15 seconds until the download button is available
    element = WebDriverWait(browser, 15).until(
        # find element "FAOSTAT" by xpath and click
        EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[1]/div/div[1]/i"))
    )
    element.click()
    return browser      

def unzip_FAO():
    """
    This function extract FAOstat data from 'FAOSTAT.zip' file into 'faostat' folder
    """


    if not os.path.exists(FAO_zip_path):
        browser = down_FAOstat()
        
    # go to the data    
    time = 0
    # unzip the FAOSTAT.zip file
    while FAO_zip not in os.listdir(data_path): # check if FAO_zip is downloaded
        sleep(10) # if not, wait for 5 seconds
        time = time+10
        print("FAOSTAT downloading, {:.1f}s".format(time))
    else: # if yes, unzip the file              
        handle = zipfile.ZipFile(FAO_zip_path)      
        handle.extractall(faostat_unzip) # extract the files into a "faostat" folder
        handle.close()
        os.remove(FAO_zip_path) # remove the zip file
 
    assert os.path.exists(faostat_unzip)

def unzip_subfolders():
    """
    This function unzips .zip files in FAOstat data folder
    """

    unzip_FAO()
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
    
    assert extension not in os.listdir(zip_ls)

def sort_subfolders():
    """
    This function moves subfolders in "faostat" directory into categories according to https://www.fao.org/faostat/en/#data
    """
    unzip_subfolders()
    # create dict match subfolder with the first world of FAO original subfolder names
    category_dict = {"Production":["Production","Value"],
                    "Food Security and Nutrition":["Food"],
                    "Food Balances":["SUA", "FoodBalanceSheetsHistoric","FoodBalanceSheets", "CommodityBalances"],
                    "Trade":["Trade",],
                    "Prices":["Prices","PricesArchive",'Deflators','Exchange', "ConsumerPriceIndices"],
                    "Land, Inputs and Sustainability":["Inputs","Environment"],
                    "Population and Employment":["Population",'Employment'],
                    "Investment":["Investment", "Development"],
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
            # move folders from /faostat to /faostat/category           
            shutil.move(faostat_unzip+'/'+folder,faostat_unzip+'/'+pair[first_word]+'/'+folder)
    
    #shutil.move(faostat_unzip, data_dir)
    os.chdir("../../")

sort_subfolders()



