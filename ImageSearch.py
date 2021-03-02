from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from base64 import b64decode

def get_query_link(query):
	return "https://www.google.com/search?q=" + "+".join(filter(lambda char: char != " ", query.split())) + "&source=lnms&tbm=isch"

async def get_page(link):
	assession = AsyncHTMLSession()
	request = await assession.get(link)

	page = request.html
	await page.arender()

	return page

def get_first_image(page):
	soup = BeautifulSoup(page.html, "html.parser")
	src = soup.find("img", {"class": "rg_i Q4LuWd"}).get_attribute_list("src")[0]

	extension = src[src.find("image/") + 6 : src.find(";")]
	data = b64decode(src[src.find(",") + 1 : ])

	return extension, data

