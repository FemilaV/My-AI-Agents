import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# 1. Search Tool (Tavily)
search_tool = TavilySearchResults(k=2)

# 2. Scraping Tool (Async with httpx)
async def scrape_website(url: str) -> str:
    """
    Optimized scraper using httpx for true async support.
    Skips non-HTML files and limits content length.
    """
    print(f"  - Scraping: {url}")
    try:
        # Skip potential binary files by checking extension or headers
        if url.lower().endswith(('.pdf', '.jpg', '.png', '.zip', '.exe')):
            print(f"  - Skipping non-HTML file: {url}")
            return f"Skipped non-HTML content: {url}"

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url)
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                print(f"  - Skipping non-HTML content type: {content_type}")
                return f"Skipped non-HTML content: {url}"

            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
                script_or_style.decompose()
                
            # Get text
            text = soup.get_text(separator=' ')
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit content length to avoid overloading local LLM
            # 5,000 characters is usually enough for a research summary
            if len(text) > 5000:
                print(f"  - Truncating long content ({len(text)} chars to 5000)")
                text = text[:5000] + "... [TRUNCATED]"
                
            return text
    except Exception as e:
        print(f"  - Error scraping {url}: {e}")
        return f"Error scraping {url}: {e}"