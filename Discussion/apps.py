from django.apps import AppConfig


class DiscussionConfig(AppConfig):
    name = 'Discussion'

    def ready(self):
        import Discussion.signal