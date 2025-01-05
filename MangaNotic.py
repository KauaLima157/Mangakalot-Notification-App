from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
from plyer import notification
from PIL import Image
import io
import re


# URL da página de favoritos
BOOKMARK_URL = "https://manganato.com/bookmark"

chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\\Users\\Kauã\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--profile-directory=Profile 1')

# Configurar o Selenium
chrome_service = Service("C:\\Users\\Kauã\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe") 
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Pasta para salvar imagens temporárias
IMAGE_DIR = "manga_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def fetch_manga_updates():
    try:
        print("Carregando página...")
        driver.get(BOOKMARK_URL)
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.user-bookmark-item')))
        print("Página carregada com sucesso.")

        manga_list = []
        items = driver.find_elements(By.CSS_SELECTOR, '.user-bookmark-item')  
        print(f"Quantidade de itens encontrados: {len(items)}")

        for item in items:
            try:
                # Captura o título do mangá
                title = item.find_element(By.CSS_SELECTOR, '.bm-title a').text.strip()

                # Tenta capturar o capítulo com o seletor CSS específico
                chapter_element = None
                try:
                    chapter_element = item.find_element(By.CSS_SELECTOR, 'span:nth-of-type(3) a[style*="color: #079eda"]')
                except Exception as e:
                    break

                # Se o elemento não foi encontrado, pula para o próximo item
                if not chapter_element:
                    continue

                chapter = chapter_element.text.strip()
                chapter_url = chapter_element.get_attribute('href')

                # Captura a URL da imagem
                image_url = item.find_element(By.CSS_SELECTOR, 'a img').get_attribute('src')


                # Adiciona os dados à lista
                manga_list.append({
                    "title": title,
                    "chapter": chapter,
                    "chapter_url": chapter_url,
                    "image_url": image_url,
                })

            except Exception as e:
                print(f"Erro ao processar item: {e}")

        return manga_list

    except Exception as e:
        print(f"Erro ao buscar atualizações: {e}")
        return []
def sanitize_title(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)[:50] 

def download_image(image_url, title):
    try:
        title = sanitize_title(title)  # Sanitiza o título
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join(IMAGE_DIR, f"{title}.ico")
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((64, 64))  # Redimensiona para 64x64
            image.save(image_path, format="ICO")  # Salva como .ico
            return os.path.abspath(image_path)  # Retorna o caminho absoluto
        else:
            print(f"Erro ao baixar imagem: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
        return None
    
# def send_notification(title, message, image_url=None):
#     try:
#         icon_path = None
#         if image_url:
#             icon_path = download_image(image_url, title)

#         print(f"Enviando notificação: {title}, com ícone: {icon_path}")
#         notification.notify(
#             title=title,
#             message=message,  
#             app_icon=icon_path,  
#             timeout=20
#         )
#         time.sleep(1)  # Pequeno delay entre notificações
#         print(f"Notificação enviada: {title}")
#     except Exception as e:
#         print(f"Erro ao enviar notificação: {e}")


# Monitoramento contínuo
def monitor_manga_updates(interval=1000):
    previous_data = {}

    while True:
        manga_data = fetch_manga_updates()
        if manga_data:
            for manga in manga_data:
                title = manga["title"]
                chapter = manga["chapter"]
                image_url = manga["image_url"]

                # Verifica se o título já foi notificado ou se há um novo capítulo
                if title not in previous_data or previous_data[title] != chapter:
                #     Envia a notificação com a imagem e o capítulo
                #     send_notification(
                #         f"Novo capítulo: {title}",
                #         f"Capítulo {chapter} disponível!",
                #         image_url=image_url,
                #     )
                     previous_data[title] = chapter

        print(f"Aguardando {interval} segundos para a próxima verificação...")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_manga_updates(interval=60)