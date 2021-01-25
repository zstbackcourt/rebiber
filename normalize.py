from bib2json import normalize_title, load_bib_file
import argparse
import json
import sys


def construct_bib_db(bib_list="bib_list.txt"):
    with open(bib_list) as f:
        filenames = f.readlines()
    bib_db = {}
    for filename in filenames:
        with open(filename.strip()) as f:
            db = json.load(f)
            bib_db.update(db)
    return bib_db


def normalize_bib(bib_db, all_bib_entries):
    output_bib_entries = []
    log_text = ""
    for bib_entry in all_bib_entries:
        # read the title from this bib_entry
        original_title = ""
        original_bibkey = ""
        for entry_idx in range(len(bib_entry)):
            entry = bib_entry[entry_idx]
            if entry.strip().startswith("@"):
                original_bibkey = entry[entry.find('{')+1:-1]
                if not original_bibkey:
                    original_bibkey = bib_entry[entry_idx+1].strip()[:-1]
            if entry.strip().startswith("title"):
                start_idx = entry.find('=')+1
                while not entry[start_idx].isalpha():
                    start_idx += 1
                end_idx = len(entry)-1
                while not entry[end_idx].isalpha():
                    end_idx -= 1
                original_title = entry[start_idx:end_idx+1]
                break
        title = normalize_title(original_title)   
         
        # try to map the bib_entry to the keys in all_bib_entries
        if title in bib_db and title:
            # update the bib_key to be the original_bib_key
            for line_idx in range(len(bib_db[title])):
                if bib_db[title][line_idx].strip().startswith("@"):
                    bibkey = bib_db[title][line_idx][bib_db[title][line_idx].find('{')+1:-1]
                    if not bibkey:
                        bibkey = bib_db[title][line_idx+1].strip()[:-1]
                    bib_db[title][line_idx] = bib_db[title][line_idx].replace(bibkey, original_bibkey)
                    break
            log_str = "Converted to the official format. ID: %s ; Title: %s" % (original_bibkey, original_title)
            # print(log_str)
            log_text += log_str
            output_bib_entries.append(bib_db[title])
        else:
            output_bib_entries.append(bib_entry)
            
    # TODO: write the log_text to a file 
    with open(sys.argv[2], "w") as output_file:
        for entry in output_bib_entries:
            for line in entry:
                output_file.write(line)


if __name__ == "__main__":
    bib_db = construct_bib_db()
    all_bib_entries = load_bib_file(sys.argv[1])
    normalize_bib(bib_db, all_bib_entries)