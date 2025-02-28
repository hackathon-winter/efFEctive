import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from questions.models import Question
from questions.data import QUESTIONS_DATA

def load_question():
    for question_data in QUESTIONS_DATA:

        try:
            question, created = Question.objects.get_or_create(
                content=question_data['content'],
                defaults={
                    'choices': json.dumps(question_data['choices']),
                    'correct_answer': question_data['correct_answer'],
                    'explanation': question_data['explanation'],
                    'difficulty': question_data['difficulty'] ,
                    'category': question_data['category'],
                    'created_at': now()
                }
            )

            if created:
                print(f'登録に成功しました。: {question_data["content"]}')
            else:
                print(f'既に登録済みです。: {question_data["content"]}')
    
        except Exception as e:
            prtin(f'エラー発生：{str(e)}')
        
    print('問題の登録が完了しました。')