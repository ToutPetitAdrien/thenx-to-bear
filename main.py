import scrapy
from scrapy.http import FormRequest


class LoggedThenXSpider(scrapy.Spider):
    name = 'logged_thenx'
    start_urls = ['https://thenx.com/sign_in']

    def parse(self, response):
        token =  response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'authenticity_token': token,
            'session[email]': 'adrien.mulattieri@icloud.com',
            'session[password]': 'qefrUc-zuptir-2giqdy',
            'commit': 'Login',
        }, callback=self.after_login)

    def after_login(self, response):
        yield scrapy.Request('https://thenx.com/programs/48', callback=self.scrap_program)

    def scrap_program(self, response):
        parts_selector = response.css('.card')
        result = {}
        for part in parts_selector:
            part_title = part.css('.card-title::text').get()
            workouts_urls = part.css('a.list-group-item::attr(href)').getall()
            result[part_title] = workouts_urls

        for part_title in result:
            for url in result[part_title]:
                yield scrapy.Request('https://thenx.com' + url, callback=self.scrap_workout)

    def scrap_workout(self, response):
        parts_selector = response.css('.card')
        result = {}
        for part in parts_selector:
            part_title = part.css('.card-title::text').get()
            exercises_selector = part.css('a.list-group-item')
            exos_list = []
            for idx, exercise in enumerate(exercises_selector):
                exo_name = exercise.css('h6::text').get()
                exo_quantity = exercise.css('p::text').get()
                exos_list.append({
                    'order': idx + 1,
                    'name': exo_name, 
                    'quantity': exo_quantity
                })
            result[part_title] = exos_list
        print(result)
