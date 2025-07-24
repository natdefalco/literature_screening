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

Author: [Your Name]
"""
