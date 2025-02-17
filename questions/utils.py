import json
from django.core.exceptions import ObjectDoesNotExit
from django.utils.timezone import now
from questions.models import Question
from questions.data import QUESTIONS_DATA

def load_question():
    for question_data in QUESTIONS_DATA:

        try:
            existing_question = Question.objects.get(content=question_data['content'])
            print(f'既に登録済みです。: {question_data["content"]}')
        except ObjectDoesNotExit:
            Question.objects.create(
                content=question_data['content'],
                choices=question_data['choices'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data['explanation'],
                difficulty=question_data['difficulty'],
                category=question_data['category'],
                created_at=now()
            )
            print(f'登録に成功しました。: {question_data["content"]}')
        
    print('問題の登録が完了しました。')