import scrapy
import requests
import json
import csv
from scrapy.crawler import CrawlerProcess

class zameen(scrapy.Spider):
    name = "zameen"
    start_urls = ["https://www.zameen.com/all_locations/Lahore-1-1-1.html"]

    def parse(self, response):
        csv_columns = ['Location', 'Baths', 'Bedrooms', 'Price', 'Area', 'Pic Links', 'Person name', 'Contact Number']
        csvfile = open('lahore.csv', 'w', newline='', encoding="utf-8")
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        links = response.css("ul.line-list li a::attr(href)").extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.scrapeHouse)

    def scrapeHouse(self, response):
        for resp in response.css("div.f74e80f3"):
            link = resp.css("a._7ac32433::attr(href)").extract_first()
            yield scrapy.Request(url="https://www.zameen.com"+link, callback=self.scrapeData)

        nextpage = response.css("a.b7880daf::attr(href)")[-1].extract()
        nextpagetitle = response.css("a.b7880daf::attr(title)")[-1].extract()

        if nextpagetitle == "Next":
            yield scrapy.Request(url='https://www.zameen.com' + nextpage, callback=self.scrapeHouse)



    def scrapeData(self,response):
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-length': '20',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'G_ENABLED_IDPS=google; _gcl_au=1.1.1473468360.1603343989; _ga=GA1.2.798039822.1603343989; device_id=kgkeaifdmpgcmbuvp; sib_cuid=ab8aed4c-45ea-4385-ab33-31515bd80e42; __cfduid=d85e0cdf57042bd1edb6c3e880c34c27f1606391779; anonymous_session_id=0c183096-7242-4781-891d-7230cf559c9e; PHPSESSID=4942ivlkg94mmmd5ilkjkabtk4; pop_ads=3; _gid=GA1.2.533816681.1606712980; settings=%7B%22area%22%3Anull%2C%22currency%22%3A%22PKR%22%2C%22installBanner%22%3Atrue%2C%22searchHitsLayout%22%3A%22LIST%22%7D; abTests=%7B%7D; banners=%7B%7D; userCity=1; userLocation=%7B%22countryCode%22%3Anull%2C%22countryName%22%3Anull%2C%22cityName%22%3Anull%7D; AMP_TOKEN=%24NOT_FOUND; referrer=%2FHomes%2FLahore_DHA_Defence-9-2.html; XSRF-TOKEN=eyJpdiI6IkxKTnBlNlhQYTE2dUpnbER0V05mNnc9PSIsInZhbHVlIjoiZW5lRGkzUUxiZjc4b0hxRVRaM0NOZEJ4VVR1UFwvdm12bWxxT2RhSDlYUTFOVDN5VTF1VDFMQnV3czcyXC9WaEtJcUl3c3Z3RHdETUFSeVJpdElUaTN6QT09IiwibWFjIjoiYzNkYmFlM2NmNzc2ZTQ4ZGYwZWI3NjY5ZDNhN2JkNGVmMjAxOTg3YzE3NTM1ZWEyZDNmMDg4YzliYjdmNjA5YyJ9; zam_session=eyJpdiI6IlFWUFVWcjVXalwvWThhUnl0SWduMHdRPT0iLCJ2YWx1ZSI6Im5HK0J6UHZWVDNGWEV3UEE1eVpzVGFPcElMbGtudzQwQUF6azZqa1wvZmIyd3JwaUhGOTdydGdvSGFDckFKVnlLcHN5Wm04NGc0WG10akp4ZVFxQ0RZZz09IiwibWFjIjoiYjY1OWJhZGVmYTgwNzY5MzVhNmQyZTA2MzMyZDMxYjliMDkxZThlMGMzODkwNTY5YzU0OTQyNTE1YmFkMjAyMyJ9; AWSALB=DNqaaElIF/jFKWmzjrPeE3Si1sAFr0GFayF4XYH/dvhu8vIB96Ufu4ST0svKZDffx9g3A1e3CapbClIhsa5Q1mqMtwMXlqqUbdBR2+L6fjovBTS380RrJC2I+Rt0; AWSALBCORS=DNqaaElIF/jFKWmzjrPeE3Si1sAFr0GFayF4XYH/dvhu8vIB96Ufu4ST0svKZDffx9g3A1e3CapbClIhsa5Q1mqMtwMXlqqUbdBR2+L6fjovBTS380RrJC2I+Rt0; _gat_UA-201547-7=1',
            'origin': 'https://www.zameen.com',
            'referer': 'https://www.zameen.com/Property/dha_phase_3_dha_phase_3_block_xx_2_kanal_furnished_brand_new_house_for_sale_in_dha_phase_3_block_xx_lahore-25891314-1586-1.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'x-csrftoken': 'undefined',
            'x-requested-with': 'XMLHttpRequest'
        }
        property_id = response.url.split('-')[1]
        body = 'property_id={}'.format(property_id)
        url = 'https://www.zameen.com/nfpage/async/show-numbers/'
        resp = requests.post(url, headers=headers, data=body)
        data = json.loads(resp.text)
        mobile = data.get('result').get('number').get('mobile')
        personname = data.get('result').get('number').get('contact_person')

        otherinfo = response.css("span._812aa185::text").extract()
        price = response.css("span._812aa185 div.c4fc20ba::text").extract()
        area = response.css("span._812aa185 span::text").extract()
        picslinks = response.css(
            "div.image-gallery-thumbnails-container a.image-gallery-thumbnail picture._219b7e0a img::attr(src)").extract()

        #
        with open("lahore.csv", "a", encoding="utf-8", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([otherinfo[1], otherinfo[2], otherinfo[4], price, area, picslinks, personname, str(mobile)])


process = CrawlerProcess({ 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)' })
process.crawl(zameen)
process.start()
