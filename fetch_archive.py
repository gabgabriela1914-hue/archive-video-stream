import json
import urllib.parse
import urllib.request

# Termos de busca no Internet Archive (filmes, séries, novelas, desenhos e músicas)
QUERIES = [
    'mediatype:movies AND (filme OR serie OR novela OR desenho)',
    'mediatype:audio AND (musica OR album)'
]

def search_archive():
    results = []
    for query in QUERIES:
        encoded_query = urllib.parse.quote(query)
        url = f"https://archive.org/advancedsearch.php?q={encoded_query}&fl[]=identifier,title,mediatype,format&sort[]=&rows=30&page=1&output=json"

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                docs = data.get('response', {}).get('docs', [])

                for item in docs:
                    identifier = item.get('identifier')
                    title = item.get('title', 'Sem título')
                    media_type = item.get('mediatype')
                    details_url = f"https://archive.org/details/{identifier}"

                    results.append({
                        "title": title,
                        "type": media_type,
                        "identifier": identifier,
                        "url": details_url
                    })
        except Exception as e:
            print(f"Erro na busca: {e}")

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Total de itens salvos: {len(results)}")

if __name__ == "__main__":
    search_archive()
              
