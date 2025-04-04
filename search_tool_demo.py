"""
Search Tool Demo

This script demonstrates how to use the SerperDev search tool and web scraping tool
from CrewAI without needing to run a Flask server.
"""

from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv
import os
import json
from pprint import pprint

# Load environment variables from .env file
load_dotenv()

# Verify that the SerperDev API key is available
if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY not found in environment variables. Please check your .env file.")

def search_web(query, num_results=5):
    """
    Search the web using SerperDev API
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return
        
    Returns:
        dict: Search results
    """
    search_tool = SerperDevTool()
    
    # Execute the search
    print(f"Searching for: {query}")
    results = search_tool.search(query)
    
    # Parse the results
    if isinstance(results, str):
        try:
            results = json.loads(results)
        except json.JSONDecodeError:
            print("Error parsing results as JSON")
            return {"error": "Failed to parse results"}
    
    # Extract and format the organic search results
    formatted_results = []
    
    if "organic" in results:
        for i, result in enumerate(results["organic"][:num_results]):
            formatted_result = {
                "position": i + 1,
                "title": result.get("title", "No title"),
                "link": result.get("link", "No link"),
                "snippet": result.get("snippet", "No snippet")
            }
            formatted_results.append(formatted_result)
    
    return formatted_results

def scrape_website(url):
    """
    Scrape content from a website
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: The scraped content
    """
    scrape_tool = ScrapeWebsiteTool()
    
    # Execute the scraping
    print(f"Scraping website: {url}")
    content = scrape_tool.scrape_website(url)
    
    return content

def main():
    """Main function to demonstrate search and scrape tools"""
    
    # Get user input for search query
    query = input("Enter your search query: ")
    
    # Search the web
    search_results = search_web(query)
    
    # Display search results
    print("\n=== Search Results ===")
    for result in search_results:
        print(f"\n{result['position']}. {result['title']}")
        print(f"URL: {result['link']}")
        print(f"Snippet: {result['snippet']}")
    
    # Ask if user wants to scrape a specific result
    scrape_option = input("\nEnter the number of the result you want to scrape (or press Enter to skip): ")
    
    if scrape_option and scrape_option.isdigit():
        index = int(scrape_option) - 1
        if 0 <= index < len(search_results):
            url = search_results[index]["link"]
            
            # Scrape the website
            content = scrape_website(url)
            
            # Display a preview of the scraped content
            print("\n=== Scraped Content Preview ===")
            preview_length = min(500, len(content))
            print(f"{content[:preview_length]}...\n")
            
            # Save the scraped content to a file
            filename = f"scraped_content_{query.replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Full content saved to {filename}")
        else:
            print("Invalid result number.")
    
if __name__ == "__main__":
    main()
