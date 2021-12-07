from bs4 import BeautifulSoup
import lxml
# import requests

# url = 'https://mobiledevelop.git.protei.ru/Protei_HLR_HSS/docs/api/commands/'

# req = requests.get(url)

# soup = BeautifulSoup(req.text, 'lxml')

# with open('hlr_api.html', 'w') as file:
#     file.write(req.text)

with open('hlr_api.html', 'r') as file:
    soup = BeautifulSoup(file, 'lxml')

commands = soup.find(class_='td-content').find_all(class_='entry')
urls = soup.find(class_='td-content').find(class_='entry').find('h5').find('a')
print(urls)
#
# for item in commands:
#     new = item.text.replace('\n\n', ' ')
#     print(f'{new.strip()}')
