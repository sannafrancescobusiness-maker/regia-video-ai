import asyncio, json, os, sys
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto("file://" + os.path.join(HERE, "../comp/comp.html")); await pg.evaluate("window.__ready")
        d = await pg.evaluate("({ev:window.__events(),dur:window.__meta.dur,sezioni:window.__sezioni()})")
        json.dump(d, open(os.path.join(HERE, "events.json"), "w"), indent=0); await b.close()
        print(len(d["ev"]), "eventi, durata", d["dur"])
asyncio.run(main())
