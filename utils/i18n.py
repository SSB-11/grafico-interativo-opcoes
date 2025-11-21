import json

class I18N:
    def __init__(self, language:str):
        self.lang = language
        with open(f'locales/{self.lang}.json') as file:
            self.data = json.load(file)

    def t(self, key:str) -> str:
        return self.data.get(key, key) # if the key is not found, show the key itself
    