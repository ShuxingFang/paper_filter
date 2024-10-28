import os
import json

def remove_no_abstract_papers(unique_papers, no_abstract_papers):
    for paper in unique_papers:
        if paper["abstract"] == "":
            no_abstract_papers.append(paper)
            unique_papers.remove(paper)

def remove_duplicate(file):
    with open(file, "r") as f:
        paper_list = json.load(f)

    CAP = 250
    unique_papers = []
    seen_dois = set()
    seen_titles = set()
    seen_abstract = set()
    duplicate_count = 0

    for paper in paper_list:

        doi = paper["doi"]
        title = paper["title"].lower()
        abstract = paper["abstract"].lower()[:CAP]

        # if we found a duplicate doi
        if doi in seen_dois and doi != "":
            for existing_paper in unique_papers:
                if existing_paper["doi"] == doi:
                    # delete stored duplicate if it does not have abstract
                    if existing_paper["abstract"] == "":
                        unique_papers.remove(existing_paper)
                        unique_papers.append(paper)
                    # else we skip the current paper
                    else:
                        break
            duplicate_count += 1
            continue
        # if we found duplicate title
        elif title in seen_titles:
            for existing_paper in unique_papers:
                if existing_paper["title"].lower() == title:
                    # delete stored duplicate if it does not have abstract
                    if existing_paper["abstract"] == "":
                        unique_papers.remove(existing_paper)
                        unique_papers.append(paper)
                    # else we skip the current paper
                    else:
                        break
            duplicate_count += 1
            continue
        # if we found duplicate abstract
        elif abstract in seen_abstract and abstract != "":
            duplicate_count += 1
            continue


        seen_dois.add(doi)
        seen_titles.add(title)
        seen_abstract.add(abstract)
        unique_papers.append(paper)


    no_abstract_papers = []
    remove_no_abstract_papers(unique_papers, no_abstract_papers)



    with open("data/parsed/cleaned_papers.json", "w") as file:
        json.dump(unique_papers, file, indent=4)
        print(f"{duplicate_count} duplicates removed")


    if len(no_abstract_papers) > 0:
        with open("output/no_abstract_papers.json", "w") as file:
            json.dump(no_abstract_papers, file, indent=4)
            print(f"{len(no_abstract_papers)} papers lack abstract and require manual checks")
