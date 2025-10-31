"""
GitBook scraper for Kamino documentation.
Scrapes, chunks, and indexes documentation into PostgreSQL with embeddings.
"""

import asyncio
import argparse
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.core.database import AsyncSessionLocal
from app.services.rag_service import get_rag_service


class GitBookScraper:
    """Scraper for GitBook documentation."""
    
    def __init__(self, base_url: str, dapp: str = "kamino", use_playwright: bool = False):
        self.base_url = base_url
        self.dapp = dapp
        self.visited_urls = set()
        self.documents = []
        self.use_playwright = use_playwright
        self.client = None
    
    async def scrape(self, max_pages: int = 100) -> List[Dict[str, Any]]:
        """
        Scrape GitBook documentation.
        
        Args:
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of scraped documents
        """
        print(f"🕷️  Starting scrape of {self.base_url}")
        
        if self.use_playwright:
            return await self._scrape_with_playwright(max_pages)
        else:
            return await self._scrape_with_httpx(max_pages)
    
    async def _scrape_with_httpx(self, max_pages: int) -> List[Dict[str, Any]]:
        """Scrape using simple HTTP client (faster, more reliable)."""
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }
        ) as client:
            self.client = client
            
            # Track which URLs we've scraped (different from visited_urls which includes discovered links)
            scraped_urls = set()
            urls_to_scrape = [self.base_url]
            
            while urls_to_scrape and len(scraped_urls) < max_pages:
                url = urls_to_scrape.pop(0)
                
                if url in scraped_urls:
                    continue
                
                try:
                    # Scrape the page
                    await self._scrape_page_httpx(url)
                    scraped_urls.add(url)
                    
                    # Add newly discovered links to the queue
                    new_links = [u for u in self.visited_urls if u not in scraped_urls and u not in urls_to_scrape]
                    urls_to_scrape.extend(new_links[:max_pages - len(scraped_urls)])
                    
                    await asyncio.sleep(0.3)  # Be nice to the server
                except Exception as e:
                    print(f"❌ Error scraping {url}: {e}")
                    scraped_urls.add(url)  # Mark as attempted
        
        print(f"✅ Scraped {len(self.documents)} documents from {len(scraped_urls)} pages")
        return self.documents
    
    async def _scrape_with_playwright(self, max_pages: int) -> List[Dict[str, Any]]:
        """Scrape using Playwright (for JS-heavy sites)."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                ]
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            # Start with base URL
            await self._scrape_page(page, self.base_url)
            
            # Find and scrape linked pages
            links = await self._extract_links(page)
            
            for link in links[:max_pages]:
                if link not in self.visited_urls:
                    try:
                        await self._scrape_page(page, link)
                        # Small delay to avoid overwhelming the server
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"❌ Error scraping {link}: {e}")
            
            await context.close()
            await browser.close()
        
        print(f"✅ Scraped {len(self.documents)} documents")
        return self.documents
    
    async def _scrape_page_httpx(self, url: str):
        """Scrape a single page using HTTP client."""
        print(f"📄 Scraping: {url}")
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract title
            title_tag = soup.find("title")
            title = title_tag.text if title_tag else url
            
            # Extract main content
            main_content = self._extract_content(soup)
            
            # Extract links for further scraping
            for link_tag in soup.find_all("a", href=True):
                href = link_tag["href"]
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                base_parsed = urlparse(self.base_url)
                
                # Only add internal links
                if parsed.netloc == base_parsed.netloc and full_url not in self.visited_urls:
                    # Avoid anchors and duplicates
                    clean_url = full_url.split("#")[0]
                    if clean_url and clean_url not in self.visited_urls:
                        self.visited_urls.add(clean_url)
            
            if main_content and len(main_content) > 100:
                self.documents.append({
                    "title": title,
                    "content": main_content,
                    "url": url,
                    "dapp": self.dapp,
                })
                print(f"✅ Successfully scraped: {title[:50]}...")
            else:
                print(f"⚠️  Skipped (no content): {url}")
        
        except Exception as e:
            print(f"⚠️  Warning: Could not scrape {url}: {e}")
    
    async def _scrape_page(self, page, url: str):
        """Scrape a single page."""
        if url in self.visited_urls:
            return
        
        print(f"📄 Scraping: {url}")
        self.visited_urls.add(url)
        
        try:
            # Navigate with longer timeout and different wait strategy
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for content to load with multiple selectors
            try:
                await page.wait_for_selector("article, main, .content, [role='main']", timeout=15000)
            except:
                # If specific selector fails, wait a bit and continue
                await asyncio.sleep(2)
            
            # Extract content
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # Extract title
            title = await page.title()
            
            # Extract main content
            main_content = self._extract_content(soup)
            
            if main_content and len(main_content) > 100:  # Only save if we got meaningful content
                self.documents.append({
                    "title": title,
                    "content": main_content,
                    "url": url,
                    "dapp": self.dapp,
                })
                print(f"✅ Successfully scraped: {title[:50]}...")
            else:
                print(f"⚠️  Skipped (no content): {url}")
        
        except Exception as e:
            print(f"⚠️  Warning: Could not scrape {url}: {e}")
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from page."""
        # Try different content selectors
        content_selectors = [
            "article",
            "main",
            ".content",
            ".markdown-body",
            ".page-content",
            "#content",
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Remove script and style elements
                for script in content_elem(["script", "style", "nav", "footer"]):
                    script.decompose()
                
                # Get text
                text = content_elem.get_text(separator="\n", strip=True)
                
                # Clean up
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                return "\n".join(lines)
        
        return ""
    
    async def _extract_links(self, page) -> List[str]:
        """Extract internal links from page."""
        links = await page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('a[href]'));
                return links.map(a => a.href);
            }
        """)
        
        # Filter internal links
        base_domain = urlparse(self.base_url).netloc
        internal_links = []
        
        for link in links:
            parsed = urlparse(link)
            if parsed.netloc == base_domain and link not in self.visited_urls:
                internal_links.append(link)
        
        return internal_links
    
    def chunk_content(self, content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split content into overlapping chunks.
        
        Args:
            content: Content to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            
        Returns:
            List of content chunks
        """
        if len(content) <= chunk_size:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + chunk_size
            chunk = content[start:end]
            
            # Try to break at sentence boundary
            if end < len(content):
                last_period = chunk.rfind(".")
                last_newline = chunk.rfind("\n")
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # Only break if we're past halfway
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks


async def scrape_and_index(source: str = "kamino", max_pages: int = 100):
    """
    Scrape documentation and index into database.
    
    Args:
        source: Source to scrape (kamino, etc.)
        max_pages: Maximum pages to scrape
    """
    # Define sources
    sources = {
        "kamino": {
            "url": "https://docs.kamino.finance",
            "dapp": "kamino",
        },
    }
    
    if source not in sources:
        print(f"❌ Unknown source: {source}")
        print(f"Available sources: {', '.join(sources.keys())}")
        return
    
    source_config = sources[source]
    
    # Initialize scraper
    scraper = GitBookScraper(
        base_url=source_config["url"],
        dapp=source_config["dapp"]
    )
    
    # Scrape documents
    documents = await scraper.scrape(max_pages=max_pages)
    
    if not documents:
        print("⚠️  No documents scraped")
        return
    
    # Index documents
    print(f"\n📊 Indexing {len(documents)} documents...")
    
    rag_service = get_rag_service()
    indexed_count = 0
    
    async with AsyncSessionLocal() as db:
        for doc in documents:
            # Chunk large documents
            chunks = scraper.chunk_content(doc["content"], chunk_size=1000, overlap=200)
            
            for i, chunk in enumerate(chunks):
                title = doc["title"]
                if len(chunks) > 1:
                    title = f"{title} (Part {i+1}/{len(chunks)})"
                
                try:
                    await rag_service.add_document(
                        title=title,
                        content=chunk,
                        url=doc["url"],
                        db=db,
                        dapp=doc["dapp"],
                        doc_type="documentation",
                        metadata={
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                        }
                    )
                    indexed_count += 1
                    
                    if indexed_count % 10 == 0:
                        print(f"  Indexed {indexed_count} chunks...")
                
                except Exception as e:
                    print(f"❌ Error indexing document: {e}")
        
        await db.commit()
    
    print(f"\n✅ Successfully indexed {indexed_count} document chunks")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Scrape and index documentation")
    parser.add_argument(
        "--source",
        type=str,
        default="kamino",
        help="Source to scrape (kamino, etc.)"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Maximum pages to scrape"
    )
    
    args = parser.parse_args()
    
    # Run scraper
    asyncio.run(scrape_and_index(
        source=args.source,
        max_pages=args.max_pages
    ))


if __name__ == "__main__":
    main()
