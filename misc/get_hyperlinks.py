import requests
from bs4 import BeautifulSoup
import json
import re
import argparse

def get_number_of_hyperlinks(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return 0

        soup = BeautifulSoup(response.content, 'html.parser')
        hyperlinks = soup.find_all("a", href=lambda x: x and x.startswith('/wiki/'))
        return len(hyperlinks)

    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return 0

def count_words(text):
    words = re.split(r'\s+', text)
    return len([w for w in words if w.strip()])

def get_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page content. Status code: {response.status_code}")
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get all text, not just paragraphs
        content = soup.get_text(separator=" ")
        return content

    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return ""

def process_articles(file_path, output_file='link_updated.json'):
    # List of titles to process, if empty, process all
    titles_to_process = ['Discografia di Gloria Gaynor', 'NGC 874', 'Dragon Ball Side Story: Vita da Yamcha', 'Jean Cossin', 'NGC 790', 'NGC 722', 'William Garnett', 'Zanchi (cognome)', 'NGC 809', 'Supercopa de España 2025', 'An Se-young', 'Rune Bækgaard', 'NGC 830', 'Anaheim Ducks 2024-2025', 'Citipes', 'Referendum sulla sovranità di Gibilterra del 1967', 'Martin Huston', 'EA Sports College Football 25', 'NGC 794', 'Incidente di Gramos', 'Devil Goddess', 'NGC 833', 'NGC 712', 'Kevin Abstract', 'Atletica leggera ai XVII Giochi paralimpici estivi - 100 metri piani T47 maschili', 'I Hope You Dance', 'Alboris', 'Poveda - Amico forte di Dio', 'Jackpot - Se vinci ti uccido!', 'NGC 835', 'Franco Mosca (chirurgo)', 'NGC 739', 'NGC 795', 'NGC 789', 'Storia militare di Porto Rico', 'Notion (software di produttività)', 'Il Signore degli Anelli - La guerra dei Rohirrim', 'The Piano Lesson (film)', 'Nicola Garrone', 'Crisi Israele-Hezbollah del 2023-2024', 'Bozza:Lachnellula willkommii', 'NGC 780', 'NGC 751', 'NGC 778', 'NGC 842', 'Jelena Begović', 'Helgoland 513', 'NGC 863', 'San Miguel Beermen', 'Psophocarpus tetragonolobus', 'Perugia (disambigua)', 'Città sostenibile', 'Scottish Championship 2024-2025', 'NGC 814', 'Bozza:Huffington Post Italia', 'NGC 837', 'NGC 774', 'Yunisleidy García', 'Ginnastica ai Giochi della XXXIII Olimpiade - Concorso individuale maschile', 'NGC 754', 'Tabyana Ali', 'Bozza:Semiotica del vino', 'Seggiovia Monte Moro', 'NGC 721', 'Bozza:Enzo Neri', 'Ugolino Novelli', 'Equitazione ai Giochi della XXXIII Olimpiade - Concorso completo individuale', 'Taylor Swift vs Scooter Braun: Bad Blood', 'Ammi majus', 'Referendum sulla sovranità di Gibilterra del 2002', 'Dunya (Islam)', 'Milan Futuro 2024-2025', 'NGC 749', 'Halka', 'Maja Gullstrand', 'NGC 732', 'Football League One 2024-2025', 'NGC 829', 'ESO 383-76', 'Storia del conflitto Israelo-Palestinese', 'Arnaud Binard', 'Campionati mondiali juniores di sci nordico 2025', 'Amanda Shires', '395. Infanterie-Division (Wehrmacht)', 'La fedeltà del cane', 'Nicole Sabouné', 'NGC 756', 'NGC 873', 'Liga Nacional de Honduras 2024-2025', '223. Infanterie-Division (Wehrmacht)', 'Gridalo Forte Records', 'Episodi di Wanted (serie televisiva australiana) (seconda stagione)', 'NGC 786', 'Don Ciccone', 'Zemheri', 'Loris Bianchi', 'NGC 769', 'NGC 872', 'NGC 750', 'Darth Maul: Shadow Hunter', 'Star Wars: Tales of the Empire', 'Divorzio in nero', 'Who Loves You (brano)', 'Ruined King: A League of Legends Story', 'FlyArystan', 'NGC 836', 'Passage Pommeraye', 'Teatro Cavour', 'Atletica leggera ai XVII Giochi paralimpici estivi - Getto del peso F55 maschile', 'Trio per pianoforte n.2 (Schubert)', 'Lassie - Una nuova avventura', 'Cyamopsis tetragonoloba', 'NGC 762', 'NGC 787', 'Campo di concentramento di Mataina', 'Corrado Scivoletto', 'Battle Chasers: Nightwar', 'Kahraman Babam', 'Pietro Paolo Caruana', 'Ubuntu Cinnamon', 'NGC 773', 'The Thicket (film)', 'Florebat olim studium', 'NGC 798', 'Bozza:Antonino Barbetta', 'Bozza:Assalto a Kiev (1918)', 'I 10+2 Comandamenti', 'NGC 827', 'FirstGroup', 'Giacomo Filippo Sacco', 'YUBA liga (1992-2006, pallacanestro femminile)', 'NGC 775', 'Bobana Veličković', 'Mappa di Abel Tasman', 'Luka Vušković', 'Canarium luzonicum', 'NGC 848', 'Ashwini Ponnappa', 'Manus ferens munera', 'NGC 781', 'Martin Olesen', 'NGC 840', 'Crush - La storia di Tamina', 'Sottozero (EP)', '320. Infanterie-Division (Wehrmacht)', 'Eizan Electric Railway', 'Bozza:Giovanni Maria Arduino', "Accordo Giappone-Corea dell'agosto 1905", 'Camping di famiglia', 'Ciclismo ai Giochi della XXXIII Olimpiade - BMX maschile', 'Coke Zero Sugar 400 2024', 'Il mondo gira', 'Bozza:Infocilento', 'Amaris stupens casibus', 'La stanza accanto (film 2024)', 'Raimondo Cagiano de Azevedo', 'Ernesto Chiacchierini', 'Simone Grillo', 'Flete flenda', 'Sayen - La terra ha sete', 'Annie Swynnerton', 'Bozza:Ovovia Malanotte', 'Bozza:PL-9', 'Kül Masalı', 'Macapea', 'Smart factory', 'Canadian Open 2024', 'NGC 768', 'Norombega', 'Emanuel Vigeland Mausoleum', 'NGC 746', 'Adda (cantante)', 'Alma Basket Patti', 'NGC 797', 'Andrea Hall', 'Strongylodon macrobotrys', 'Luca Magrini', 'Andreotto Saraceno', 'Spedizione di Domínguez-Escalante', 'Andrea Rossi (patriota)', '141. Reserve-Division (Wehrmacht)', 'Shy (manga)', 'Togo ai Giochi della XXXIII Olimpiade', 'NGC 761', 'Fairy Five', 'Bernard White', 'Sociedad Patriótica', 'Vendredi Soir', 'Bozza:Fatica da contatto di rotolamento', 'Bozza:Russia meridionale', 'Il trenino Thomas - Sodor e il tesoro dei pirati', 'Maes (rapper)', 'Batman: Caped Crusader', 'NGC 799', 'Yoga Radio Bruno Estate', 'Slumafia', 'Serie D 2024-2025 (gironi G-H-I)', 'NGC 758', 'NGC 831', 'NGC 782', 'NGC 791', 'NGC 766', '5. Armee (Wehrmacht)', "Selezioni giovanili della nazionale di pallavolo femminile dell'Irlanda", 'Mario Bandini', 'NGC 792']

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output_data = []

    for article in data:
        title = article['title']
        url = article['url']

        if titles_to_process and title not in titles_to_process:
            continue

        print(f"Processing article: {title}")
        
        num_hyperlinks = get_number_of_hyperlinks(url)
        content = get_article_content(url)
        num_words = count_words(content)
        hyperlinks_per_word = num_hyperlinks / num_words if num_words > 0 else 0

        output_data.append({
            'title': title,
            'num_hyperlinks': num_hyperlinks,
            'num_words': num_words,
            'hyperlinks_per_word': hyperlinks_per_word
        })

        print(f"Found {num_hyperlinks} hyperlinks and {num_words} words for article '{title}'. Hyperlinks per word: {hyperlinks_per_word:.6f}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"Updated data saved to '{output_file}'")

def main():
    parser = argparse.ArgumentParser(description='Scrape recent Wikipedia articles.')
    parser.add_argument('--lang', type=str, default='en', help='Language code for Wikipedia API (e.g., "en" for English, "de" for German).')
    args = parser.parse_args()
    file_path = f'{args.lang}_links.json'
    output_file = f'hyperlinks_jsons/{args.lang}/combo_hyperlinks.json'
    process_articles(file_path, output_file=output_file)

if __name__ == "__main__":
    main()
