from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questions'

    # Djangoサーバー起動時にsignal.pyを読み込む
    def ready(self):
        import questions.signals