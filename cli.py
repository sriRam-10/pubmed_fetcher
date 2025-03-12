 
import argparse
from pubmed_fetcher import get_pubmed_ids, fetch_paper_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Output file name (CSV).")

    args = parser.parse_args()

    if args.debug:
        print(f"Searching for: {args.query}")

    pubmed_ids = get_pubmed_ids(args.query)
    if args.debug:
        print(f"Found PubMed IDs: {pubmed_ids}")

    papers = fetch_paper_details(pubmed_ids)

    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
