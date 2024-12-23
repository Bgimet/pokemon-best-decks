import requests
from bs4 import BeautifulSoup

# URL de la page principale contenant les informations sur les decks
BASE_URL = 'https://www.millenium.org/guide/419010.html'

# Fonction pour extraire les informations des decks sur la page
def scrape_decks():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(BASE_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver tous les éléments correspondant aux tiers
    tiers = soup.select('.article__subsubtitle')
    deck_data = []

    for tier in tiers:
        tier_name = tier.get_text(strip=True)

        # Trouver les decks associés à ce tier
        decks = tier.find_next_siblings('div', class_='w-list-items__subtitle')
        for deck in decks:
            deck_name = deck.get_text(strip=True)

            # Trouver le contenu du deck (description ou détails)
            content_element = deck.find_next('p', class_='article__paragraph')
            deck_content = content_element.get_text(strip=True) if content_element else "No content available"

            deck_data.append({
                'tier': tier_name,
                'name': deck_name,
                'content': deck_content
            })

    return deck_data

# Exécuter le script et afficher les résultats
if __name__ == '__main__':
    decks = scrape_decks()
    for deck in decks:
        print(f"Tier: {deck['tier']}")
        print(f"Nom du deck: {deck['name']}")
        print(f"Contenu: {deck['content']}\n")
