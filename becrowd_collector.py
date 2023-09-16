# import time
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from tqdm import tqdm


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
