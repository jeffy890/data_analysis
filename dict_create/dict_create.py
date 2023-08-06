'''
    written by Kensuke Kobayashi(jeffy890)
    2023.8.6

'''
import argparse
import MeCab
import numpy as np
import os
import pandas as pd
import pickle
import sys

def make_dict(baselist):
    mcb = MeCab.Tagger("-Owakati")
    made_dict = {}
    num_count = 0

    for i in range(len(baselist)):
        try:
            words_temp = baselist[i].split("/")
            for j in range(len(words_temp)):
                insert_word = words_temp[j].replace(" ", "")
                insert_word = mcb.parse(insert_word).split()
                for k in range(len(insert_word)):
                    if insert_word[k] not in made_dict:
                        made_dict[insert_word[k]] = num_count
                        num_count += 1
        except:
            pass
        
    print("made dict length: " + str(len(made_dict)))
    return made_dict

def make_array(basedict, baselist):
    mcb = MeCab.Tagger("-Owakati")
    madearray = np.zeros([len(baselist), len(basedict)])

    for i in range(len(baselist)):
        try:
            words_temp = baselist[i].split("/")
            for j in range(len(words_temp)):
                judge_word = words_temp[j].replace(" ", "")
                judge_word = mcb.parse(judge_word).split()
                for k in range(len(judge_word)):
                    if judge_word[k] in basedict:
                        madearray[i, basedict[judge_word[k]]] += 1
        except:
            pass

    print("made array shape: " + str(madearray.shape))
    return madearray

def dictsave(basedict, fn_to_s):
    with open(fn_to_s, "wb") as f:
        pickle.dump(basedict, f)
    print("dict saved: " + str(fn_to_s))

def load_dict(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)

def main():
    filename_to_load = "kaken.csv"

    desc = "make dict for analysis"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "-k",
        "--kaken",
        help="csv file name to load"
    )

    args = parser.parse_args()

    if args.kaken:
        filename_to_load = args.kaken
        error = os.path.isfile(filename_to_load)
        if error == 1:
            print("using file: " + filename_to_load)
        else:
            print("\nseems like no such file: " + filename_to_load)
            print("check the file name\n")
            sys.exit()

    # load base csv
    base_df = pd.read_csv(filename_to_load)
    # rename columns
    base_df = base_df.rename(columns={"審査区分/研究分野": "fields"})
    base_df = base_df.rename(columns={"キーワード": "keywords"})
    # drop NaN
    base_df = base_df.dropna(subset=["fields"])
    base_df = base_df.dropna(subset=["keywords"])

    print("\nlength of the list: " + str(len(base_df.index)))

    fields_lists = base_df["fields"].values.tolist()
    keywords_lists = base_df["keywords"].values.tolist()

    field_dict = make_dict(fields_lists)
    keyword_dict = make_dict(keywords_lists)

    # save made dict or not
    dictsave(field_dict, "field_dict.pkl")
    dictsave(keyword_dict, "keyword_dict.pkl")

    field_array = make_array(field_dict, fields_lists)
    keyword_array = make_array(keyword_dict, keywords_lists)

    print("\neverything is now done\n")

if __name__ == "__main__":
    main()
