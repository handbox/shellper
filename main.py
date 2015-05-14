from google import search
for url in search('hi world', tld='ru', lang='ru', stop=5):
        print(url)
