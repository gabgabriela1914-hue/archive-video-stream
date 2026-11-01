import json
import sys
import urllib.parse
import urllib.request

QUERIES = [
    'mediatype:movies AND (title:(filme OR série OR novela OR desenho OR cartoon OR movie) OR subject:(filme OR novela OR desenho OR cartoon OR animation))',
    'mediatype:audio AND (title:(música OR musica OR album) OR subject:(música OR music OR album))',
]

def search_archive():
    results = []
    for query in QUERIES:
        params = [
            ("q", query),
            ("fl[]", "identifier"),
            ("fl[]", "title"),
            ("fl[]", "mediatype"),
            ("rows", "30"),
            ("page", "1"),
            ("output", "json"),
        ]
        url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params)
        print("URL:", url)

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
        except Exception as e:
            print(f"Erro na busca: {e}", file=sys.stderr)
            continue

        docs = data.get("response", {}).get("docs", [])
        print(f"{len(docs)} itens para: {query[:50]}...")

        for item in docs:
            identifier = item.get("identifier")
            results.append({
                "title": item.get("title", "Sem título"),
                "type": item.get("mediatype"),
                "identifier": identifier,
                "url": f"https://archive.org/details/{identifier}",
            })

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Total de itens salvos: {len(results)}")
    if not results:
        sys.exit(1)  # faz o workflow falhar visivelmente

if __name__ == "__main__":
    search_archive()
