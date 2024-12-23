import os
import requests as r
import database as d

if __name__ == '__main__':
    roster = d.fetch_all("roster", "data/stats_2425.db")
    for p in roster:
        name = p[2].replace(" ", "_").lower() + ".png"
        headshot = p[1]

        files = os.listdir("assets/headshots")
        if name in files:
            continue

        with open(f"assets/headshots/{name}", 'wb') as handle:
            response = r.get(headshot, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
