'''
    written by Kensuke Kobayashi(jeffy890)
    2023/8/24

    education data extractor
'''

import numpy as np
import pandas as pd

filename_to_load = "kaken.csv"
filename_to_save = "result.csv"

def main():
    education_extract(filename_to_load, filename_to_save)

def education_extract(fn_to_l, fn_to_s):
    # file load
    base_df = pd.read_csv(fn_to_l)

    #print(str(len(base_df.index)) + " loop will be executed")

    # adding educational columns
    base_df["year1"] = np.nan
    base_df["edu1"] = np.nan
    base_df["year2"] = np.nan
    base_df["edu2"] = np.nan
    base_df["year3"] = np.nan
    base_df["edu3"] = np.nan

    edu_df = base_df["education"]

    
    for i in range(len(base_df.index)):
        temp_list = ["NaN", "NaN", "NaN", "NaN", "NaN", "NaN"]

        if pd.isnull(edu_df[i]):
            base_df["year1"][i] = "NaN"
            base_df["edu1"][i] = "NaN"
            base_df["year2"][i] = "NaN"
            base_df["edu2"][i] = "NaN"
            base_df["year3"][i] = "NaN"
            base_df["edu3"][i] = "NaN"
            continue

        edu_temp = edu_df[i]
        edu_temp = edu_temp.replace("[", "").replace("]", "").replace("'", "")
        edu_temp = edu_temp.split(",")
        
        if len(edu_temp) != 1:
            temp_list = extract(edu_temp)

        base_df["year1"][i] = temp_list[0]
        base_df["edu1"][i] = temp_list[1]
        base_df["year2"][i] = temp_list[2]
        base_df["edu2"][i] = temp_list[3]
        base_df["year3"][i] = temp_list[4]
        base_df["edu3"][i] = temp_list[5]

    base_df.to_csv(fn_to_s, index=False, encoding="utf_8_sig")

def extract(got_list):
    search_word_daigakuin = "大学院"
    serach_word_kennkyuuka = "研究科"
    search_word_gakubu = "学部"

    append_list = ["NaN", "NaN", "NaN", "NaN", "NaN", "NaN"]

    firstone = got_list[0].split(" ")
    print(firstone)
    append_list[0] = firstone[2]
    append_list[1] = firstone[3].replace("'", "")

    for i in range(len(got_list)):
        univ_name = got_list[i].split(" ")
        if search_word_daigakuin in univ_name[len(univ_name)-1]:
            append_list[2] = univ_name[len(univ_name)-2]
            append_list[3] = univ_name[len(univ_name)-1].replace("'", "").replace("?", "")

        elif serach_word_kennkyuuka in univ_name[len(univ_name)-1]:
            append_list[2] = univ_name[len(univ_name)-2]
            append_list[3] = univ_name[len(univ_name)-1].replace("'", "").replace("?", "")

        if search_word_gakubu in univ_name[len(univ_name)-1]:
            append_list[4] = univ_name[len(univ_name)-2]
            append_list[5] = univ_name[len(univ_name)-1].replace("'", "").replace("]", "").replace("?", "")

    return append_list

if __name__ == "__main__":
    main()
