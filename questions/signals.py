from django.db.models.signals import post_migrate
from django.dispatch import receiver
from questions.utils import load_question

@receiver(post_migrate)
def populate_questions(sender, **kwargs):

    # マイグレーション後に、data.pyのデータを自動登録する
    if sender.name == 'questions':
        print('マイグレーション完了！問題データを登録します。')
        load_question()