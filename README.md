# literature_screening
"""
📚 Literature Screening Script – Multi-Source Academic Search Tool

This Python script allows researchers and students to automatically retrieve academic papers
from 8 major databases using a single search query. It collects metadata including title,
authors, abstract, year, and URL, and saves the results in an Excel file.

👨‍🔬 Databases Queried:
- Springer
- CORE
- arXiv
- Semantic Scholar
- Elsevier Scopus (API key required)
- OpenAlex
- PubMed
- Crossref

🔧 How to Use:
1. ✅ Install dependencies (in your terminal or Anaconda prompt):
   pip install pandas requests openpyxl

2. ✏️ Customize your search term:
   Change the following line to your topic of interest:
       SEARCH_QUERY = ('"flow dynamics in carbonates"')

3. 🔐 API Keys:
   - Springer: Get a free API key at https://dev.springernature.com
   - CORE: Register at https://core.ac.uk/services#api
   - Scopus (Elsevier): Requires institutional access or personal API key: https://dev.elsevier.com

   Replace the default keys in the section:
       SPRINGER_API_KEY = "your_key_here"
       CORE_API_KEY = "your_key_here"
       SCOPUS_API_KEY = "your_key_here"

4. 📁 Output:
   Results are saved to an Excel file in your current directory as:
       literature_screening.xlsx

5. 🖥 Run the script:
   Open a terminal and navigate to your folder:
       cd C:/Users/your_username/Documents/my_script_folder

   Then run:
       python literature_screening.py

6. 📝 Optional:
   You can increase the number of papers fetched by changing:
       TOTAL_PAPERS = 20

💡 Tips:
- Each data source has its own structure and may return overlapping results.
- You can filter, clean, or deduplicate the Excel file afterward using Excel or Python.
- For large-scale use, consider using batching or adding delays to avoid rate limits.

🧠 How to Structure Your Search Query

You can use Boolean operators to refine your literature search:

🔤 Examples:
    SEARCH_QUERY = 'desalination AND energy'
    SEARCH_QUERY = '("groundwater recharge" OR "aquifer storage")'
    SEARCH_QUERY = '("flow dynamics" AND carbonate AND NOT petroleum)'
    SEARCH_QUERY = '(wetlands OR lakes OR ponds) AND "methane emissions"'

📝 Syntax Tips:
- Use **double quotes** for exact phrases: "greenhouse gas"
- Use **AND**, **OR**, **NOT** (uppercase recommended)
- Use **parentheses** to group terms and control logic

🌐 Supported by:
- Springer, CORE, arXiv, Semantic Scholar
- Scopus (Elsevier), OpenAlex, PubMed, Crossref

⚠️ Final query must be encoded:
    from urllib.parse import quote
    ENCODED_QUERY = quote(SEARCH_QUERY)

💡 Feel free to experiment. Most APIs support full Boolean logic, especially Springer, CORE, and Scopus.
"""


Author: Natalie De Falco
"""
