'''
    written by Kensuke Kobayashi(jeffy890)
    2023/8/2

    read README.md to get details
    license info if in LICENSE.txt
'''

import argparse
import csv
import datetime
import json
import os
import sys
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np

from details import check_json
from details import check_jsondatadir
from details import get_details
from details import get_json
from details import get_jsons
from details import json_load
from details import find_the_one

# settings and function call
def main():
    # variables(global)
    filename_to_load = "kaken.csv"
    filename_to_save = "result.csv"
    
    scripts_option = 0

    desc = "get data from researchmap by researchers name and id"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "-o", 
        "--option", 
        action="store_true",
        help="hundle multiple targets or not"
        )

    parser.add_argument(
        "-k",
        "--kaken",
        help="csv file name to load"
    )

    args = parser.parse_args()

    print("using option: ", end="")
    if args.option:
        scripts_option = 1
        print(scripts_option)
    else:
        print(scripts_option)

    if args.kaken:
        filename_to_load = args.kaken
        error = os.path.isfile(filename_to_load)
        if error == 1:
            print("using file: " + filename_to_load)
        else:
            print("\nseems like no such file: " + filename_to_load)
            print("check the file name\n")
            sys.exit()

    # main sentences in this main function
    check_jsondatadir()
    base_df = data_prepare(filename_to_load)
    error = get_data(base_df, filename_to_save, scripts_option)

    if error == 0:
        print("\neverything is now done")
        print("check the file: " + filename_to_save + "\n")

# data preparation
def data_prepare(fn_to_l):
    """
    load csv and prepare researchers' name and id at least
    """
    # csv load
    readlist = pd.read_csv(fn_to_l)

    # rename columns
    readlist = readlist.rename(columns={"姓名": "name"})
    readlist = readlist.rename(columns={"研究者番号": "id"})
    
    # data cleaning if necessary
    readlist = readlist.dropna(subset=["name"])
    readlist = readlist.reset_index()

    print("\nlength of the list: " + str(len(readlist.index)))
    #print("\nread csv contains following columns")
    #print(readlist.columns)

    # the returned list must have name and id columns at least
    return readlist

# selenium part
def get_data(base_df, fn_to_s, scripts_option):
    # url settings
    base_url_name = "https://researchmap.jp/researchers?q="
    base_url_id = "https://researchmap.jp/researchers?erad_id="

    # selenium settings
    try:
        option = Options()
        option.add_argument('--headless')
        service = Service(executable_path=r'./chromedriver/chromedriver')
        driver = webdriver.Chrome(service=service, options=option)
        print("chrome driver succeccfuly loaded\n")
    except:
        print("chrome driver load error(or some error on selenium)")

    # save list setting
    list_titles = ["name from csv", "hit number", "url(api)", "hit name", "hit family name", "hit given name", "affiliation ja", "affiliation en", "degree ja", "degree en", "degree date", "degree institution ja", "degree institution en", "rsmp id", "erad", "orcid", "jglobal", "experience", "education", "paper", "award", "research project", "probability"]
    with open(fn_to_s, "a", encoding="utf_8_sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(list_titles)

    # main loop
    for index, row in base_df.iterrows():
        search_id = row.loc["id"]
        serach_name = row.loc["name"].replace(" ", "")
        templist = []
        templist_multiple = []
        templist.append(serach_name)
        print(" - " + str(search_id) + str(serach_name).rjust(10) + ":\t", end="")

        # file check. if the file exists, load the file.
        if check_json(search_id) == 1:
            templist.extend([1, search_id])
            templist.extend(json_load(search_id))
            save_data(templist, fn_to_s)
            print("file found, saved json loaded")

        else:
            # first is id search
            try:
                driver.get(base_url_id + urllib.parse.quote(str(search_id)))
                # if the id hit, badge_number exist. else, this try ends and goes to except
                badge_number = driver.find_element(By.CSS_SELECTOR, "span.badge.rm-cv-header-badge")
                print("id hit    -> ", end="")
                templist.append(int(badge_number.text))
                all_links = driver.find_elements(By.XPATH, "//div[@class='rm-cv-card-name']/a")
                base_url = all_links[0].get_attribute("href").split("//")
                base_url_api = "http://api." + str(base_url[1])
                templist.append(base_url_api)

                templist.extend(get_json(base_url_api, search_id))
                print("got data")

            # if there's no id result, then name search starts
            except:
                print("no id hit -> name src starts -> ", end="")

                # name search
                try:
                    driver.get(base_url_name + urllib.parse.quote(str(serach_name)))
                    badge_number = driver.find_element(By.CSS_SELECTOR, "span.badge.rm-cv-header-badge")
                    templist.append(int(badge_number.text))
                    all_links = driver.find_elements(By.XPATH, "//div[@class='rm-cv-card-name']/a")

                    # if the option==1, save one researcher, else save all
                    if scripts_option == 1:
                        templist.extend(find_the_one(search_id, serach_name, all_links))
                    else:
                        templist_multiple = (get_jsons(search_id, serach_name, all_links))
                    print("name hit!")

                # if there's no data or couldn't get data
                except:
                    print("no name hit")
                    templist.append(0)

            # add data to file
            if len(templist_multiple) > 0:
                for i in range(len(templist_multiple)):
                    savelist = [serach_name, int(badge_number.text)]
                    savelist.extend(templist_multiple[i])
                    save_data(savelist, fn_to_s)
            else:
                save_data(templist, fn_to_s)
            
        # debug option
        if index > 6:
            break

    return 0

def save_data(datalist, fn_to_s):
    with open(fn_to_s, "a", encoding="utf_8_sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(datalist)

if __name__ == "__main__":
    main()