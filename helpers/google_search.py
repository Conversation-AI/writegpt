from googleapiclient.discovery import build
import os, re

def google_search(query, mode="company", num_results=5):
  # Replace YOUR_API_KEY with your actual API key
  api_key = os.environ.get('GOOGLE_API_KEY')
  # Replace YOUR_CSE_ID with your actual Custom Search Engine ID
  cse_id = os.environ.get('CSE_ID')

  # Build the service object for the Custom Search API
  service = build('customsearch', 'v1', developerKey=api_key)


  if mode=="company":
    date_restriction='m1' # Past month: m1, Past week: w1, Past 6 months: m6, Past year: y1
    site_urls=None
    # Construct the search query with regex
    query += r" (news|blog|launch)"
    query = re.sub(r"\s+", r" ", query)
  else:
    date_restriction=None
    site_urls = 'linkedin.com'
    num_results=1

  # Restrict the search results to specific websites
  # site_urls = 'linkedin.com,twitter.com,medium.com,techcrunch.com,crunchbase.com'
  # optional search site limitation: 

  print("site_urls: ", site_urls)

  # Execute the search
  results = service.cse().list(q=query, cx=cse_id, dateRestrict=date_restriction, siteSearch=site_urls, num=num_results).execute() 
  

  # Extract the relevant information from the search results
  items = results.get('items', [])
  search_results = []
  for item in items:
      search_results.append({
          'title': item['title'],
          'link': item['link'],
          'snippet': item['snippet']
      })

  return search_results
