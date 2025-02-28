import uuid
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import transaction
from questions.models import Question
from questions.utils import load_question
from questions.data import QUESTIONS_DATA

@receiver(post_migrate)
def populate_questions(sender, **kwargs):

    # マイグレーション後に、data.pyのデータを自動登録する
    if sender.name == 'questions':
        print('マイグレーション完了！問題データを登録します。')
    
        with transaction.atomic():  # データ登録のトランザクションを確保
            for q_data in QUESTIONS_DATA:
                print("デバッグ: q_data =", q_data)

                # UUIDがq_dataに既に存在するかチェック
                if 'uuid' not in q_data:
                    q_data['uuid'] = str(uuid.uuid4())
                    print(f"新規 UUID を生成: {q_data['uuid']}")

                existing_question = Question.objects.filter(uuid=q_data['uuid']).first()

                if existing_question:
                    print(f"問題 (UUID: {q_data['uuid']}) は既に登録済みのためスキップ")
                    continue

                # 新しい問題を登録
                Question.objects.create(
                    uuid=q_data['uuid'],
                    content=q_data['content'],
                    choices=q_data['choices'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data['explanation'],
                    difficulty=q_data['difficulty'],
                    category=q_data['category']
                )
                print(f"問題 (UUID: {q_data['uuid']}) を登録しました！")

        print('すべての問題データの登録が完了しました。')