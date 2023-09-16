# import time
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from tqdm import tqdm


headers = {
    "authority": "www.beecrowd.com.br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "pt-BR,pt;q=0.9",
    "cache-control": "no-cache",
    "cookie": "judge=mk1t1hnntg982e403gdqtm4hn0; csrfToken=90c163adeb2626676e72e4270d2687a23d7399ad5ddd007f35019370055e8d093839ab8feb7472556b9dee757a065066c524b365d89a467e5a8ef56b2720a5fe; _gid=GA1.3.9988277.1694784447; cf_clearance=B07xhJUm0JXXxp07DXW9MgNlnJsCzTXzPe.44sLnO.g-1694784447-0-1-87ee3157.ee86e56d.3c023823-0.2.1694784447; _gat=1; _clck=11rd9s6|2|ff1|0|1353; _gali=container; _ga_2RSK6HJVYH=GS1.1.1694784447.1.1.1694784455.52.0.0; _ga=GA1.1.1756228126.1694784447; _clsk=1srr114|1694784455572|2|1|z.clarity.ms/collect",
    "dnt": "1",
    "pragma": "no-cache",
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}


def parser_profile_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    avatar_photo = (
        soup.find("div", {"class": "perfil-photo"})["style"]
        .split("url(")[1]
        .split("); ")[0]
    )
    user_name = soup.find("div", {"class": "pb-username"}).text.strip()
    user_information = [
        msg.text.strip().split(":\n")
        for msg in soup.find("ul", {"class": "pb-information"}).findAll("li")
    ]
    university = ""
    if len(user_information[2]) > 1:
        university = user_information[2][1]
    result_profile_data = {
        "avatar_photo": avatar_photo,
        "user_name": user_name,
        "ranking": user_information[0][1],
        "country": user_information[1][1],
        "university": university,
        "since": user_information[3][1],
        "points": user_information[4][1],
        "solved_problems": user_information[5][1],
        "tryed_problems": user_information[6][1],
        "submissions": user_information[7][1],
    }
    return result_profile_data


def get_profiles_data(profileIDs):
    profiles_data = []
    with sync_playwright() as p:
        browser = p.firefox.launch(
            headless=True
        )  # para mostrar o browser na tela é so colocar headless=False
        page = browser.new_page()
        stealth_sync(page)
        for profileID in tqdm(profileIDs):
            page.goto(f"https://www.beecrowd.com.br/judge/pt/profile/{profileID}")
            # page.screenshot(path=f"images/becrowd_{profileID}.png")
            try:
                _profiles_data = parser_profile_data(page.content())
            except Exception:
                continue
            profiles_data.append(_profiles_data)
            # time.sleep(2)
        browser.close()
        json.dump(profiles_data, open("profiles_data.json", "w"), indent=4)
        return profiles_data


if __name__ == "__main__":
    profile_list = [
        "882915",
        "882916",
        "882918",
        "882919",
        "882920",
        "882921",
        "882922",
        "882923",
    ]
    print("Starting...")
    results = get_profiles_data(profile_list)
    print("Finished!")
