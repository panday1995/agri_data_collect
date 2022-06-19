

"""
Created on Jun 19 2022

@author: Fan Yang

ToDo
- Documentation

"""

from collections import Iterable
from selenium import webdriver
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

import pandas as pd
import os
import selenium.webdriver.support.expected_conditions as EC
import zipfile

parent_path = "D:\\Users\\sheep\\Codes\\KRproject"
data_path = os.path.join(parent_path,"Nutrient balance")



# install Chrome browser webdriver
browser_driver_path = ChromeDriverManager().install() # path to browser driver for selenium

# set file path for FAOstat data download
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : data_path} # set path for download
chrome_options.add_experimental_option('prefs', prefs)

# initiate browser for use
browser = webdriver.Chrome(browser_driver_path,options=chrome_options)
browser.get(r"https://www.fao.org/faostat/en/#home")

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
    print("FAOSTAT downloading, {int}s".format(time))
else: # if yes, unzip the file
    handle = zipfile.ZipFile(FAO_zip)
    faostat_unzip = os.path.join(data_path,"faostat")
    handle.extractall(os.path.join(faostat_unzip)) # extract the files into a "faostat" folder
    handle.close()
# os.remove(FAO_zip) # remove the zip file

# go to the zip file
zip_ls = os.chdir(faostat_unzip)
extension = ".zip"

for item in os.listdir(zip_ls): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(item[:-4]) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file



