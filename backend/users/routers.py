from rest_framework.routers import SimpleRouter


class UsersSimpleRouter(SimpleRouter):
    def get_urls(self):
        urls = super().get_urls()
        allowed_names = [
            'user-list',
            'user-me',
            'user-set-password',
            'user-detail',
        ]
        new_urls = []
        for url in urls:
            if url.name in allowed_names:
                new_urls.append(url)
        return new_urls
