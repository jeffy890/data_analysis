'''
    written by Kensuke Kobayashi(jeffy890)
    2023/8/23

    education data extractor
'''

import csv

def main():
    pass

def extract(got_list):
    search_word_daigakuin = "大学院"
    serach_word_kennkyuuka = "研究科"
    search_word_gakubu = "学部"

    append_list = ["NaN", "NaN", "NaN", "NaN", "NaN", "NaN"]

    firstone = got_list[0].split(" ")
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
