import requests as r
import database as d

roster = d.fetch_all("roster", "data/stats_2425.db")
for p in roster:
    name = p[2].replace(" ", "_").lower() + ".png"
    headshot = p[1]

    with open(f"assets/headshots/{name}", 'wb') as handle:
        response = r.get(headshot, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
