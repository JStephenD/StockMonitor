import discord, os, random, requests, asyncio
from discord.ext import commands
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession, HTML

description = '''A Bot to monitor stocks,
made for an Upwork job.'''

BOT_TOKEN = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

loop = asyncio.get_event_loop()

#  -----------------------------------------------------------
async def open_site(url):
    for _ in range(3):
        try:
            asession = AsyncHTMLSession()
            page = await asession.get(url)
            await page.html.arender()
            return page
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
    if page := await open_site(url):
    
        if site == 'shopee':        
            details = page.html.find('.wPNuIn', first=True)
            soup = BeautifulSoup(details.html, 'html.parser')
            title = soup.find('div').find('span').text
            price = soup.find('div', class_='bBOoii').text
            price2 = soup.find('div', class_='AJyN7v').text
            stock = soup.find('div', class_='_2_ItKR').find_all('div')[-1].text

            print(f'description: {title}')
            print(f'price: {price}', f'now {price2}' if price2 else '')
            print(f'stocks: {stock}')

            ctx.send(f'description: {title} \n\n price: {price2} now {price}' if price2 else f'price: {price}')

        if site == 'lazada':
            try:
                soup = BeautifulSoup(page.content, 'html.parser')
                title = soup.find('div', id="module_product_title_1").text
                price = soup.find('span', class_='pdp-price_type_normal').text
                orig_price = None
                if deleted_price := soup.find('span', class_='pdp-price_type_deleted'):
                    orig_price = deleted_price.text
                
                print(f'description: {title}')
                print(f'price: {orig_price} now {price}' if orig_price else f'price: {price}')

                ctx.send(f'description: {title} \n\n price: {orig_price} now {price}' if orig_price else f'price: {price}')

            except Exception as e:
                print(e)
                with open('lazada.html', 'wb') as f:
                    f.write(page.content)

def track():
    pass

bot.run(BOT_TOKEN)