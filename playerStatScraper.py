from lxml import html
import requests

page = requests.get('http://www.premierleague.com/players/4413/Joe-Allen/stats?se=-1')
tree = html.fromstring(page.content)
stats = tree.xpath('//div[@class="normalStat"]/span[@class="stat"]')

for stat in stats:
     stat_name = stat.text.strip()
     stat_value = stat[0].text.strip()
     print('{}: {}'.format(stat_name, stat_value))