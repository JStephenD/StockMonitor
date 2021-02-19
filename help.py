from requests_html import AsyncHTMLSession

asession = AsyncHTMLSession()

async def f():
    return await asession.get('https://python.org/')

results = asession.run(f)

for result in results:
    print(help(result.html))
    print(result.html.url)