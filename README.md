📚 PubMed Fetcher
🚀 Overview
PubMed Fetcher is a Python-based command-line tool that:
✅ Searches PubMed for research papers based on a user query.
✅ Extracts publication details such as title, date, and author affiliations.
✅ Filters papers to include only company-affiliated authors (excluding academic institutions).
✅ Saves the results in a CSV file for easy access.

📌 Features
✔️ Fetches PubMed articles based on a user query.
✔️ Extracts title, publication date, and affiliations.
✔️ Filters company-affiliated authors.
✔️ Saves the results in a CSV file.

## ⚙️ Installation

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/sriRam-10/pubmed_fetcher
cd pubmed_fetcher

```

2️⃣ Install Dependencies (Using Poetry)

poetry install

📜 Usage
Run the following command to fetch research papers:

poetry run get-papers-list "cancer research" -f results.csv

🛠️ Development
Running Locally
Activate virtual environment:
poetry shell

Run the script manually:

python cli.py "diabetes treatment" -f output.csv

📜 License
This project is open-source and licensed under the MIT License.

🤝 Contributing
Feel free to fork this repository and submit pull requests! 🚀

📝 Author
👤 Sri Ram
📧 sriramshanmugam10@gmail.com
