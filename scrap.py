import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# Example URL: Replace with a real Pokémon TCG deck URL
SCRAPING_URL = "https://example.com/top-decks"

@app.route('/scrape-decks', methods=['GET'])
def scrape_decks():
    """Scrape top Pokémon TCG decks from a website."""
    try:
        # Fetch the webpage content
        response = requests.get(SCRAPING_URL)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant data (update selectors based on the target website)
        decks = []
        deck_elements = soup.select('.deck-card')  # Example CSS class for deck containers

        for element in deck_elements:
            name = element.select_one('.deck-name').text.strip()
            win_rate = element.select_one('.win-rate').text.strip()
            core_cards = [card.text.strip() for card in element.select('.core-card')]
            description = element.select_one('.deck-description').text.strip()

            decks.append({
                "name": name,
                "winRate": win_rate,
                "coreCards": core_cards,
                "description": description
            })

        return jsonify(decks)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
