import requests


class GitHub:
    def get_user(self, username):
        r = requests.get(f'https://api.github.com/users/{username}')
        body = r.json()

        return body

    def search_repo(self, name):
        r = requests.get(
            'https://api.github.com/search/repositories',
            params={'q': name}
        )
        body = r.json()

        return body

    @staticmethod
    def get_emojis():
        return requests.get('https://api.github.com/emojis')

    @staticmethod
    def get_all_templates():
        return requests.get(f'https://api.github.com/gitignore/templates')

    @staticmethod
    def get_template_by_name(name):
        return requests.get(f'https://api.github.com/gitignore/templates/{name}')
