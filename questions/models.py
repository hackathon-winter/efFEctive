from django.db import models

# Create your models here.
    def __str__(self):
        return f"Answer {self.answer_id} - Session {self.session.session_id}"
