from google import search
for url in search('hi world', tld='com', lang='ru', stop=5):
        print(url)
