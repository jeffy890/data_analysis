'''
    written by Kensuke Kobayashi(jeffy890)
    2023/8/2

    read README.md to get details
    license info if in LICENSE
'''

import csv
import json
import requests
import sys
import datetime
import os

def check_json(id):
    if os.path.isfile("./jsondata/" + str(id)):
        return 1
    else:
        return 0

def check_jsondatadir():
    if not os.path.isdir("./jsondata"):
        os.makedirs("./jsondata")

def json_load(id):
    with open("./jsondata/" + str(id), "r", encoding="utf-8_sig") as f:
        jsondata = json.load(f)
    
    loadedlist = get_details(jsondata, id)
    return loadedlist

def find_the_one(id, name, links):
    return get_jsons(id, name, links)

def get_json(url, id):
    # get json
    response = requests.get(url)
    jsondata = response.json()

    # json save
    with open("./jsondata/" + str(id), "w", encoding="utf-8_sig") as f:
        json.dump(jsondata, f, indent=4, ensure_ascii=False)

    return get_details(jsondata, id)

def get_jsons(id, name, links):
    templist_multiple = []
    for i in range(len(links)):
        templist = []
        base_url = links[i].get_attribute("href").split("//")
        base_url_api = "http://api." + str(base_url[1])
        templist.append(base_url_api)
        if len(links) == 1:
            templist.extend(get_json(base_url_api, id))
        else:
            templist.extend(get_json(base_url_api, str(id)+str(i)))
        templist_multiple.append(templist)

    return templist_multiple

def get_details(jsondata, id):
    """
    discription: get details from url page
    """
    
    
    try:
        researchers_family_name_ja = jsondata["family_name"]["ja"]
        researchers_given_name_ja = jsondata["given_name"]["ja"]
    except:
        researchers_family_name_ja = "na"
        researchers_given_name_ja = "na"
    #researchers_family_name = jsondata["family_name"]["en"]
    #researchers_given_name = jsondata["given_name"]["en"]
    #print(researchers_family_name+researchers_given_name)


    # 所属と学位
    
    try:
        researchers_affiliation = json.loads(json.dumps(jsondata["affiliations"], indent=4, ensure_ascii=False))[0]
        # jaに対するtry, except
        try:
            researchers_affiliation_ja = researchers_affiliation["affiliation"]["ja"]
        except:
            researchers_affiliation_ja = "na"
        # enに対するtry, except
        try:
            researchers_affiliation_en = researchers_affiliation["affiliation"]["en"]
        except:
            researchers_affiliation_en = "na"
    except:
        researchers_affiliation_ja = "na"
        researchers_affiliation_en = "na"
    
    try:
        researchers_degree = json.loads(json.dumps(jsondata["degrees"], indent=4, ensure_ascii=False))[0]
        # jaに対するtry, except
        try:
            researchers_degree_ja = researchers_degree["degree"]["ja"]
        except:
            researchers_degree_ja = "na"
        # enに対するtry, except
        try:
            researchers_degree_en = researchers_degree["degree"]["en"]
        except:
            researchers_degree_en = "na"

        # 学位取得機関
        try:
            researchers_degreeinstitution_ja = researchers_degree["degree_institution"]["ja"]
        except:
            researchers_degreeinstitution_ja = "na"

        try:
            researchers_degreeinstitution_en = researchers_degree["degree_institution"]["en"]
        except:
            researchers_degreeinstitution_en = "na"

        try:
            researchers_degree_date = researchers_degree["degree_date"]
        except:
            researchers_degree_date = "na"
    except:
        researchers_degree_ja = "na"
        researchers_degree_en = "na"
        researchers_degreeinstitution_ja = "na"
        researchers_degreeinstitution_en = "na"
        researchers_degree_date = "na"

    researchers_rsmp_id = "na"
    # ID
    try:
        # rsmp id
        try:
            researchers_rsmp_id = jsondata["rm:user_id"]
        except:
            researchers_rsmp_id = "na"

        try:
            researchers_identifiers = jsondata["identifiers"]
            # erad_id
            try:
                researchers_identifiers_erad = researchers_identifiers["erad_id"][0]
            except:
                researchers_identifiers_erad = "na"
            # orc_id
            try:
                researchers_identifiers_orc = researchers_identifiers["orc_id"][0]
            except:
                researchers_identifiers_orc = "na"
            # jgrobal
            try:
                researchers_identifiers_jglobal = researchers_identifiers["j_global_id"][0]
            except:
                researchers_identifiers_jglobal = "na"
        except:
            researchers_identifiers_erad = "na"
            researchers_identifiers_orc = "na"
            researchers_identifiers_jglobal = "na"
    except:
        researchers_rsmp_id = "na"
        researchers_identifiers_erad = "na"
        researchers_identifiers_orc = "na"
        researchers_identifiers_jglobal = "na"
        print("in exception")


    # 要素が入っているgraphのリスト
    graph_list = jsondata["@graph"]

    # 要素を代入するリストの初期化
    paper_title = "no paper"
    awards_list_to_save = []
    exp_list_to_save = []
    education_list_to_save = []
    rspro_list_to_save = []

    for i in range(len(graph_list)):
        templist = graph_list[i]
        tempjsonstr = json.dumps(templist, indent=4, ensure_ascii=False)
        tempjson = json.loads(tempjsonstr)
        #print(tempjson["@type"])

        # リストの中からpublished_papersだけを取り出す
        if tempjson["@type"] == "published_papers":
            published_papers_list = tempjson["items"]

            # paper_titleの取得とエラー処理
            try:
                # ひとつめの論文情報を取得
                published_paper_one = published_papers_list[0]
                # enのタイトル情報があることを見越しての処理．無い場合はexceptへ
                paper_title = published_paper_one["paper_title"]["en"]
                #print(paper_title)
            except:
                # エラー処理
                # タイトル取得ができなかった場合に仮で入力する
                paper_title = "temp"
                #print("couldn't get paper_title   temp title has entered")

        # 受賞
        if tempjson["@type"] == "awards":
            awards_list = tempjson["items"]
            
            for i in range(len(awards_list)):
                try:
                    award_name = awards_list[i]["award_name"]["ja"]
                except:
                    award_name = awards_list[i]["award_name"]["en"]

                awards_list_to_save.append(award_name)

        # 経歴
        if tempjson["@type"] == "research_experience":
            exp_list = tempjson["items"]
            
            for i in range(len(exp_list)):
                try:
                    exp_affil = exp_list[i]["affiliation"]["ja"]
                except:
                    exp_affil = "?"
                try:
                    exp_job = exp_list[i]["job"]["ja"]
                except:
                    exp_job = "?"
                try:
                    exp_from_date = exp_list[i]["from_date"]
                except:
                    exp_from_date = "?"
                try:
                    exp_to_date = exp_list[i]["to_date"]
                    if exp_to_date == "9999":
                        exp_to_date = "現在"
                except:
                    exp_to_date = "?"
                exp_list_to_save.append(exp_from_date + " - " + exp_to_date + " "+ exp_affil + " " + exp_job)


        if tempjson["@type"] == "education":
            education_list = tempjson["items"]
            
            for i in range(len(education_list)):
                try:
                    edu_affil = education_list[i]["affiliation"]["ja"]
                except:
                    edu_affil = "?"
                try:
                    edu_depart = education_list[i]["department"]["ja"]
                except:
                    edu_depart = "?"
                try:
                    edu_course = education_list[i]["course"]["ja"]
                except:
                    edu_course = "?"
                try:
                    edu_from_date = education_list[i]["from_date"]
                except:
                    edu_from_date = "?"
                try:
                    edu_to_date = education_list[i]["to_date"]
                except:
                    edu_to_date = "?"

                education_list_to_save.append(edu_from_date + " - " + edu_to_date + " " + edu_affil + edu_depart + edu_course)


        if tempjson["@type"] == "research_projects":
            rspro_list = tempjson["items"]
            rspro_temp = []
            for i in range(len(rspro_list)):
                try:
                    rspro_title = rspro_list[i]["research_project_title"]["ja"]
                except:
                    rspro_title = "?"

                rspro_list_to_save.append(rspro_title)
            '''
            for i in range(len(rspro_list)):
                rspro_temp += 
            '''



    # csvに追加するリストを形作る
    lists_to_save = []

    # 名前
    lists_to_save.append(researchers_family_name_ja + researchers_given_name_ja)
    
    lists_to_save.append(researchers_family_name_ja)
    lists_to_save.append(researchers_given_name_ja)

    # 所属
    lists_to_save.append(researchers_affiliation_ja)
    lists_to_save.append(researchers_affiliation_en)

    # 学位
    lists_to_save.append(researchers_degree_ja)
    lists_to_save.append(researchers_degree_en)
    lists_to_save.append(researchers_degree_date)

    # 学位取得機関
    lists_to_save.append(researchers_degreeinstitution_ja)
    lists_to_save.append(researchers_degreeinstitution_en)

    # ID
    lists_to_save.append(researchers_rsmp_id)
    lists_to_save.append(researchers_identifiers_erad)
    lists_to_save.append(researchers_identifiers_orc)
    lists_to_save.append(researchers_identifiers_jglobal)

    # 経歴
    lists_to_save.append(exp_list_to_save)

    # 学歴
    lists_to_save.append(education_list_to_save)

    # 論文
    lists_to_save.append(paper_title)

    # 受賞
    lists_to_save.append(awards_list_to_save)

    # 共同研究
    lists_to_save.append(rspro_list_to_save)
    
    #print(lists_to_save)
    return lists_to_save

