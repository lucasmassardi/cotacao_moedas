import asyncio

from playwright.async_api import Playwright, async_playwright, expect
from bs4 import BeautifulSoup

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.infomoney.com.br/ferramentas/cambio/")
    await page.wait_for_timeout(1500)

    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.find("table", {"class": "default-table"})
    linhas = tabela.find_all("tr")
   
    
    cotacoes = []
    
    for linha in linhas:
        coluna = linha.find_all("td")
        if not coluna:
            continue
        
        cotacao = {
            "moeda": coluna[0].text,
            "valor_de_compra": coluna[2].text,
            "valor_de_venda": coluna[3].text,
            "variavel": coluna[4].text,
        }


        cotacoes.append(cotacao)   
    
    print(cotacoes)


    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
