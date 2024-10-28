from utils.parse import parse
from utils.clean import remove_duplicate
from utils.check import check
from criteria import criteria

RAW_PAPERS = "data/raw"
PARSED = "data/parsed"

parse(RAW_PAPERS, PARSED)
remove_duplicate(f"{PARSED}/parsed_papers.json")
check(criteria)
