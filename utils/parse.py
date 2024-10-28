import os
import json
from .text_utils import normalize_text

def parse_ebsco(filename, entries):
    with open(filename, 'r') as file:
        entry = {}

        for line in file:
            if line.startswith("TY  -"):  # start of an entry
                entry = {
                    "title": "",
                    "abstract": "",
                    "doi": ""
                }
            elif line.startswith("ER  -"):  # end of an entry
                if entry["title"]:
                    entries.append(entry)
            elif line.startswith("T1  -"):  # title line
                entry["title"] = normalize_text(line[6:])
            elif line.startswith("AB  -"): # abstract
                if not entry["abstract"]:
                    entry["abstract"] = normalize_text(line[6:])
            elif line.startswith("DO  -") or line.startswith("L3  -"):  # doi
                entry["doi"] = normalize_text(line[6:])



def parse_pubmed(filename, entries):

    with open(filename, 'r') as file:
        entry = {
            "title": "",
            "abstract": "",
            "doi": ""
        }
        in_title = False
        in_abstract = False
        for line in file:
            if line.startswith("PMID-"):  # start of an entry
                entry = {
                    "title": "",
                    "abstract": "",
                    "doi": ""
                }
                in_title = False
                in_abstract = False
            elif line.startswith("TI  -"):  # title line
                entry["title"] = normalize_text(line[6:])
                in_title = True
            elif in_title and not line.startswith("  "): # end of title
                in_title = False
            elif in_title:   # title continued
                entry["title"] += " " + normalize_text(line[6:])
            elif (line.startswith("LID -") or line.startswith("AID -")) and "[doi]" in line: # doi
                entry["doi"] = normalize_text(line[6:].replace("[doi]", ""))
            elif line.startswith("AB  -"):  # abstract line
                entry["abstract"] = normalize_text(line[6:])
                in_abstract = True
            elif in_abstract and not line.startswith("  "): # end of abstract
                in_abstract = False
            elif in_abstract:   # abstract continued
                entry["abstract"] += " " + normalize_text(line[6:])
            elif line.startswith("SO  -"):  # end of an entry
                if entry["title"]:
                    entries.append(entry)



def parse_savedrecs(filename, entries):

    with open(filename, 'r') as file:
        entry = {
            "title": "",
            "abstract": "",
            "doi": ""
        }

        for line in file:
            if line.startswith("TY  -"):  # start of an entry
                entry = {
                    "title": "",
                    "abstract": "",
                    "doi": ""
                }
            elif line.startswith("ER  -"):  # end of an entry
                if entry["title"]:
                    entries.append(entry)
            elif line.startswith("TI  -"):  # title
                entry["title"] = normalize_text(line[6:])
            elif line.startswith("AB  -") and entry["abstract"] == "": # abstract
                    entry["abstract"] = normalize_text(line[6:])
            elif line.startswith("DO  -"):  # doi
                entry["doi"] = normalize_text(line[6:])



def parse(directory, output):
    data = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory,filename)
        if filename.startswith("EBSCO"):
            parse_ebsco(filepath, data)
        elif filename.startswith("pubmed"):
            parse_pubmed(filepath, data)
        elif filename.startswith("savedrecs"):
            parse_savedrecs(filepath, data)

    with open(f"{output}/parsed_papers.json", "w") as file:
        json.dump(data, file, indent=4)
        print(f"{len(data)} paper parsed")
