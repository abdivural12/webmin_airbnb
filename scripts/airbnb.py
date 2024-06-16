import webbrowser
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from main import get_average_price, _write_to_file
import re
import json
import pandas as pd
import requests
import re
import os

import shutil





SBR_WS_CDP = ""

# Fonction pour intercepter les requêtes de ressources et les abandonner
def route_intercept(route):
    if route.request.resource_type == "image":
        return route.abort()
    return route.continue_()

# Fonction pour extraire les informations de chaque page d'annonce
async def extract_page_info(page, link):
    base_path = "https://www.airbnb.fr"

    # Interception des requêtes pour éviter les images
    await page.route("**/*", route_intercept)
    try:
        
        await page.goto(base_path + link["href"])

        # Extraction des informations de la page
        room_price = await page.locator('span[class="_1y74zjx"]').first.inner_text()
        room_price_old = await page.locator('span[class="_1l85cgq"]').first.inner_text()
        room = await page.locator('h2[class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 dir dir-ltr"]').first.inner_text()
        roomTitle = await page.locator("h1").first.inner_text()
        roomProperties = room.split("-",1)
        roomRating = await page.locator('span[class="_12si43g"]').first.inner_text()
        roomSub_data = await page.locator('li[class="l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr"]').first.inner_text()

        li_elements = await page.query_selector_all('li.l7n4lsf.atm_9s_1o8liyq_keqd55.dir.dir-ltr')
        # Extract inner text from each element
        roomALL_data = []
        for li_element in li_elements:
            inner_text = await li_element.inner_text()
            roomALL_data.append(inner_text)


        periode_raw = await page.query_selector_all('div._tekaj0')

        periode_all = []
        for elem in periode_raw:
            inner_text_periode = await elem.inner_text()
            periode_all.append(inner_text_periode)

        period_start = periode_all[0]
        period_end = periode_all[1]

        # Now you have all the inner texts of elements with the specified class
        '''
        response = requests.get(base_path + link["href"])
        soup = BeautifulSoup(response.content, 'html.parser')
        h2_all = soup.find_all("h2")
        period = int(re.findall(r'[-+]?\d*\.\d+|\d+', h2_all[3].text)[0])
        rating = soup.find("span", class_="_12si43g").text.split()[0]
        sub_data = soup.find_all("li", class_="l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr")
        voyageur = int(re.findall(r'[-+]?\d*\.\d+|\d+', sub_data[0].text)[0])
        rooms = int(re.findall(r'[-+]?\d*\.\d+|\d+', sub_data[1].text)[0])
        bed = int(re.findall(r'[-+]?\d*\.\d+|\d+', sub_data[2].text)[0])
        bathroom = int(re.findall(r'[-+]?\d*\.\d+|\d+', sub_data[3].text)[0])
        '''

        roomDetails = {
            "Prix" : room_price,
            "old_price" :room_price_old,
            "Type" : roomProperties[0].split(":",1)[-1].strip(),
            "pays" : room.split("-",1)[1].split(",")[1].strip(),
            "region" : room.split("-",1)[1].split(",")[0].strip(),
            "Title" : roomTitle,
            "Rating" : roomRating,
            "voyageurs" :roomSub_data,
            "rooms" : roomALL_data[1],
            "bed" : roomALL_data[2],
            "bathroom" : roomALL_data[3],
            "period_start" : period_start,
            "period_end" : period_end

        }

    finally:
        return roomDetails

# Fonction principale pour exécuter le scraping
async def run(pw,url,headless=False):
    print('Connecting to Scraping Browser...')

    # Lancement du navigateur
    browser = await pw.chromium.launch(headless=False)
    try:
        page = await browser.new_page()

        # Interception des requêtes pour éviter les images
        await page.route("**/*", route_intercept)

        # Chargement de l'URL
        await page.goto(url)

        next_page = page.locator('a[aria-label="Suivant"]')
        page_number = 1
        links=[]

        # Boucle pour naviguer à travers les pages et extraire les liens
        while True:
        #while page_number == 1 :

            print(f"Scraping page {page_number}...")

            # Attente du chargement complet de la page
            while True:

                cards = await page.locator('span[class="_1y74zjx"]').all()
                if len(cards) <18:
                    continue
                else:
                    break

            # Extraction des liens des annonces de la page actuelle
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            card_class = "l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_ywwsz3_1afjdsa_10saat9 atm_1lnvhrj_zhgkwc_10saat9 atm_8i46q5_63ecz1_10saat9 bn2bl2p atm_5j_223wjw atm_9s_1ulexfb atm_e2_1osqo2v atm_fq_idpfg4 atm_mk_stnw88 atm_tk_idpfg4 atm_vy_1osqo2v atm_26_1j28jx2 atm_3f_glywfm atm_kd_glywfm atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq_oggzyc atm_70_1b8lkes_1w3cfyq_oggzyc atm_uc_glywfm_1w3cfyq_pynvjw atm_uc_aaiy6o_pfnrn2_ivgyl9 atm_70_1b8lkes_pfnrn2_ivgyl9 atm_uc_glywfm_pfnrn2_61fwbc dir dir-ltr"
            links.append(soup.find_all("a",class_ = card_class))

            # Clic sur le bouton 'Suivant' pour passer à la page suivante
            await next_page.click()
            page_number += 1

    except PlaywrightTimeoutError:
        print("TimeOut")
    finally:
        # Fermeture du navigateur à la fin
        await browser.close()

        return links

# Fonction pour écrire le contenu dans un fichier JSON
def _write_to_file(content) -> bool:
    """Write content to file"""

    with open("pages.json", "a", encoding="utf-8") as file:
        json.dump(content,file)

# Fonction principale pour exécuter le scraping sur les URLs spécifiées
async def main(bright_data=False, headless=False):

    urls = ["https://www.airbnb.fr/s/Espagne/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&monthly_start_date=2024-06-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=31&monthly_end_date=2024-08-01&checkin=2024-07-31&checkout=2024-08-31&query=Espagne&zoom_level=5&place_id=ChIJi7xhMnjjQgwR7KNoB5Qs7KY",
            #"https://www.airbnb.fr/s/Suisse/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&monthly_start_date=2024-06-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=31&monthly_end_date=2024-08-01&checkin=2024-07-31&checkout=2024-08-31&query=Suisse&zoom_level=5&place_id=ChIJYW1Zb-9kjEcRFXvLDxG1Vlw",
            #"https://www.airbnb.fr/s/Allemagne/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&monthly_start_date=2024-06-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=31&monthly_end_date=2024-08-01&checkin=2024-07-31&checkout=2024-08-31&query=Allemagne&zoom_level=5&place_id=ChIJa76xwh5ymkcRW-WRjmtd6HU",
            #"https://www.airbnb.fr/s/Portugal/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&monthly_start_date=2024-06-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=31&monthly_end_date=2024-08-01&checkin=2024-07-31&checkout=2024-08-31&query=Portugal&zoom_level=5&place_id=ChIJ1SZCvy0kMgsRQfBOHAlLuCo",
            "https://www.airbnb.fr/s/Belgique/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&monthly_start_date=2024-06-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=31&monthly_end_date=2024-08-01&checkin=2024-07-31&checkout=2024-08-31&query=Belgique&zoom_level=4&place_id=ChIJl5fz7WR9wUcR8g_mObTy60c"
            ]

    # Initialisation d'un dictionnaire pour stocker les informations extraites
    allRooms = {
            "Prix" : [],
            "old_price" : [],
            "Type" : [],
            "pays" : [],
            "region" : [],
            "Title" : [],
            "Rating" : [],
            "voyageurs" :[],
            "rooms" :[],
            "bed" : [],
            "bathroom" : [],
            "period_start" : [],
            "period_end" : []
        }

    # Connexion à Playwright
    async with async_playwright() as playwright:
        for url in urls :
            links = await run(pw=playwright,url=url,
                headless=headless)

            count = 0
            browser = await playwright.chromium.launch(headless=False)
            page = await browser.new_page()

            nomi = 0
            # Boucle pour extraire les informations de chaque page d'annonce
            for pagelinks in links:
                for link in pagelinks:
                    print(len(link))
                    count +=1
                    await page.route("**/*", route_intercept)
                    try :
                        detail = await extract_page_info(page,link)
                        allRooms["Prix"].append(detail["Prix"])
                        allRooms["old_price"].append(detail["old_price"])
                        allRooms["Type"].append(detail["Type"])
                        allRooms["region"].append(detail["region"])
                        allRooms["pays"].append(detail["pays"])
                        allRooms["Title"].append(detail["Title"])
                        allRooms["Rating"].append(detail["Rating"])
                        allRooms["voyageurs"].append(detail["voyageurs"])
                        allRooms["rooms"].append(detail["rooms"])
                        allRooms["bed"].append(detail["bed"])
                        allRooms["bathroom"].append(detail["bathroom"])
                        allRooms["period_start"].append(detail["period_start"])
                        allRooms["period_end"].append(detail["period_end"])
                        df = pd.DataFrame.from_dict(allRooms)
                        df.to_csv("checkpoint_out.csv",index=False)
                    except:
                        continue

                #shutil.copy('checkpoint_out.csv', 'checkpoint_out'+str(nomi)+'.csv')
                #nomi += 1

        # Écriture des informations extraites dans un fichier CSV
        df = pd.DataFrame.from_dict(allRooms)
        df.to_csv("total_out.csv",index=False)
        await browser.close()

# Exécution du scraping lorsque le script est directement exécuté
if __name__ == '__main__':
        asyncio.run(main(bright_data=True,
        headless=True))
