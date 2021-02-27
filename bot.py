import discord, os, random, requests, asyncio, io
from discord.ext import commands
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession, HTML
from pyppeteer import launch

description = '''A Bot to monitor stocks,
made for an Upwork job.'''

BOT_TOKEN = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

#  -----------------------------------------------------------
async def open_site(ctx, url):
    for _ in range(3):
        try:
            browser = await launch(headless=True, 
                args=[
                    '--incognito',
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            )
            pages = await browser.pages()
            page = pages[0]
            await ctx.send('session start')
            await page.goto(url)
            await ctx.send('get')
            content = await page.content()
            await ctx.send('extracting html content')
            await browser.close()
            return content
            
        except Exception:
            pass
    return None


# ------------------------------------------------------------


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def update(ctx, site, url):
    await ctx.send('opening site')
    if page := await open_site(ctx, url):
        await ctx.send('site opened and rendered')
        if site == 'shopee':
            await ctx.send('shopee detected')

            # try:
            #     with io.open('page.html', 'w', encoding="utf-8") as f:
            #         f.write(page)
            # except Exception as e:
            #     print(e)

            soup = BeautifulSoup(page, 'html.parser')
            details = soup.find('div', class_='wPNuIn')
            price, price2 = None, None

            title = details.find('div', class_='_3ZV7fL').text
            if price_div := details.find('div', class_='bBOoii'):
                price = price_div.text
            if price2_div := details.find('div', class_='AJyN7v'):
                price2 = price2_div.text
            stock = details.find('div', class_='_2_ItKR').find_all('div')[-1].text

            print(f'description: {title}')
            print(f'price: {price}', f'now {price2}' if price2 else '')
            print(f'stocks: {stock}')

            await ctx.send(
                f'description: {title} \n' +
                f'price: {price} now {price2}' if price2 else f'price: {price}' + '\n' +
                f'stocks: {stock}'
            )

        if site == 'lazada':
            await ctx.send('lazada detected')            
            soup = BeautifulSoup(page, 'html.parser')
            details = soup.find('div', class_='pdp-block__product-detail')
            price, price2 = None, None

            title = details.find('div', id="module_product_title_1").text
            if price_div := details.find('span', class_='pdp-price_type_normal'):
                price = price_div.text
            if price2_div := soup.find('span', class_='pdp-price_type_deleted'):
                price2 = price2_div.text
            
            print(f'description: {title}')
            print(f'price: {price}', f'now {price2}' if price2 else '')

            await ctx.send(
                f'description: {title} \n' +
                f'price: {price} now {price2}' if price2 else f'price: {price}'
            )
    else:
        await ctx.send('error opening page')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

def track():
    pass


bot.run(BOT_TOKEN)


# async def main():
    # page = await open_site('x', 'https://shopee.ph/Hyundai-Platinum-DM-8000-Professional-Microphone-System-COD-i.39655159.1429657456')
    # page = await open_site('x', 'https://example.com/')
    # print(page)

# asyncio.get_event_loop().run_until_complete(main())