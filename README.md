# Paper Filter Project

**Video Demo:** https://youtu.be/jzeczD56QKE

## Description

The Paper Filter Project automates the processing and filtering of large academic paper collections. It supports parsing files from multiple formats, identifying duplicates, and applying custom criteria for filtering—all while storing structured output for easy review. This project is ideal for academic and research workflows requiring efficient organization and quality control of research papers.

## Features

- **Multi-Format Parsing:** Supports EBSCO, PubMed, and savedrecs formats, extracting metadata like title, abstract, and DOI.
- **Duplicate Removal:** Detects duplicates based on DOI, title, and abstract, ensuring unique entries are kept.
- **Abstract Verification:** Flags papers missing abstracts for manual review.
- **Criteria-Based Filtering:** Utilizes OpenAI’s API to filter papers according to specific criteria, segregating approved and disqualified papers.

## Project Structure

```
.
├── README.md                    # Project documentation
├── main.py                      # Orchestrates parsing, cleaning, and filtering
├── criteria.py                  # Filtering criteria for disqualification
├── data/
│   ├── raw/                     # Raw data files in RIS and TXT formats
│   └── parsed/
│       ├── cleaned_papers.json  # Unique, cleaned papers with abstracts
│       ├── parsed_papers.json   # Parsed data before processing
│       └── test.json            # Test file for experimentation
├── output/
│   ├── approved_papers.json     # Papers that passed criteria
│   ├── disqualified_papers.json # Disqualified papers and reasons
│   └── no_abstract_papers.json  # Papers missing abstracts
└── utils/
    ├── parse.py                 # Functions for parsing formats
    ├── clean.py                 # Deduplication and filtering functions
    ├── check.py                 # OpenAI API-based paper checks
    └── text_utils.py            # Text normalization utilities
```

## Key Functionalities

- **Parsing:** `parse.py` extracts and normalizes metadata, storing it in `parsed_papers.json`.
- **Duplicate Cleaning:** `clean.py` removes duplicates, retains unique papers, and flags those missing abstracts.
- **Criteria Filtering:** `check.py` filters papers using OpenAI’s API based on `criteria.py`.

## Usage

1. **Run Pipeline:** Execute `main.py` to parse, deduplicate, and filter papers.
2. **Check Outputs:** Review results in the `output/` directory:
   - `approved_papers.json` for accepted papers.
   - `disqualified_papers.json` for disqualified entries and reasons.
   - `no_abstract_papers.json` for manual review of papers missing abstracts.

## Future Enhancements

- **Support More Formats:** Extend parsing capabilities to include additional academic formats.
- **Improved Filtering:** Add more detailed criteria for finer control over the filtering process.
- **User Interface:** Develop a user interface for easier manual review of flagged papers.
