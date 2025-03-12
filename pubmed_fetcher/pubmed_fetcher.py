import requests
import pandas as pd
import re
import html

# PubMed API Endpoints
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Month mapping for short & full names
MONTH_MAPPING = {
    "January": "01", "Jan": "01", "February": "02", "Feb": "02", "March": "03", "Mar": "03",
    "April": "04", "Apr": "04", "May": "05", "June": "06", "Jun": "06",
    "July": "07", "Jul": "07", "August": "08", "Aug": "08", "September": "09", "Sep": "09",
    "October": "10", "Oct": "10", "November": "11", "Nov": "11", "December": "12", "Dec": "12"
}

def get_pubmed_ids(query: str, max_results: int = 10):
    """Fetch PubMed IDs matching the query."""
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results}
    try:
        response = requests.get(PUBMED_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("esearchresult", {}).get("idlist", [])
    except requests.RequestException as e:
        print(f"❌ Error fetching PubMed IDs: {e}")
        return []

def fetch_paper_details(pubmed_ids):
    """Fetch details of research papers from PubMed."""
    papers = []
    for pubmed_id in pubmed_ids:
        params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}
        try:
            response = requests.get(PUBMED_FETCH_URL, params=params, timeout=10)
            response.raise_for_status()
            papers.append(parse_paper_data(response.text, pubmed_id))
        except requests.RequestException as e:
            print(f"❌ Error fetching details for PubMed ID {pubmed_id}: {e}")
    return papers

def parse_paper_data(xml_data, pubmed_id):
    """Extract relevant details from PubMed XML response."""

    # Extract title
    title_match = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", xml_data)
    title = title_match.group(1) if title_match else "N/A"

    # Extract publication date (formatted as YYYY-MM-DD)
    year_match = re.search(r"<Year>(\d{4})</Year>", xml_data)
    month_match = re.search(r"<Month>([A-Za-z]+)</Month>", xml_data)
    day_match = re.search(r"<Day>(\d{1,2})</Day>", xml_data)

    year = year_match.group(1) if year_match else "Unknown"
    month = MONTH_MAPPING.get(month_match.group(1), "01") if month_match else "01"
    day = day_match.group(1) if day_match else "01"  # Default to 1st if missing

    publication_date = f"{year}-{month}-{day}" if year != "Unknown" else "N/A"

    # Extract author affiliations & decode HTML entities
    author_matches = re.findall(r"<Affiliation>(.*?)</Affiliation>", xml_data)
    company_authors = [html.unescape(aff) for aff in author_matches if not re.search(r"university|college|institute|lab", aff, re.IGNORECASE)]

    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": publication_date,
        "Company-Affiliated Authors": ", ".join(set(company_authors)) if company_authors else "None"
    }

def save_to_csv(papers, filename):
    """Save papers to a CSV file."""
    if not papers:
        print("⚠️ No papers found. Skipping CSV creation.")
        return
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"✅ Saved results to {filename}")
