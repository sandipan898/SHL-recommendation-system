import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_shl_assessments():
    url = "https://www.shl.com/en/assessments/cognitive-ability/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    assessments = []

    # Example scraping logic – adjust this based on actual SHL HTML structure
    for card in soup.select(".card"):  # Replace with the real class from SHL
        name = card.find("h3").text.strip() if card.find("h3") else "N/A"
        description = card.find("p").text.strip() if card.find("p") else ""
        link = card.find("a")["href"] if card.find("a") else ""
        assessments.append({
            "name": name,
            "description": description,
            "link": f"https://www.shl.com{link}"
        })

    df = pd.DataFrame(assessments)
    df.to_csv("data/shl_assessments.csv", index=False)
    print("Scraping complete. Data saved to data/shl_assessments.csv")

# Run this if script is called directly
if __name__ == "__main__":
    scrape_shl_assessments()
