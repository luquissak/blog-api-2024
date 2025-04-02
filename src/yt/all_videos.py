from dotenv import load_dotenv
import os
import requests
import json
import csv

load_dotenv()
YT_API_KEY = os.getenv('YT_API_KEY')
YT_CHANNEL_ID = os.getenv('YT_CHANNEL_ID')

json_file="files/all_videos.json"
csv_file="files/all_videos.csv"

def buscar_videos_canal(max_results=250):

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet%2Cid&channelId={YT_CHANNEL_ID}&maxResults={max_results}&type=video&key={YT_API_KEY}"
    todos_os_resultados = []
    try:
        while url:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            todos_os_resultados.extend(data.get("items", []))  # Adiciona os itens da página atual à lista total

            next_page_token = data.get("nextPageToken")
            if next_page_token:
                url = f"https://www.googleapis.com/youtube/v3/search?part=snippet%2Cid&channelId={YT_CHANNEL_ID}&maxResults={max_results}&type=video&key={YT_API_KEY}&pageToken={next_page_token}"
            else:
                url = None  # Não há mais páginas

        with open(json_file, "w") as arquivo:
            json.dump(todos_os_resultados, arquivo, indent=4)  # Salva o JSON com indentação para melhor legibilidade
        print(f"JSON salvo com sucesso em '{json_file}'")

        return todos_os_resultados

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")



all_videos_json = buscar_videos_canal()

with open(csv_file, 'w', newline='', encoding='utf-8') as arquivo_csv:
    chaves = ['publishedAt', 'title', 'description']
    escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=chaves)
    escritor_csv.writeheader()
    for video in all_videos_json:
        print(f"""{video["snippet"]["publishedAt"]} :: {video["snippet"]["title"]} :: {video["snippet"]["description"]}""")
        #print({"publishedAt":f"{video["snippet"]["publishedAt"]}", "title":f"{video["snippet"]["title"]}","description":f"{video["snippet"]["description"]}"})
        escritor_csv.writerow({"publishedAt":f"{video["snippet"]["publishedAt"]}", "title":f"{video["snippet"]["title"]}","description":f"{video["snippet"]["description"]}"})

print(f"total: {len(all_videos_json)+1}")
