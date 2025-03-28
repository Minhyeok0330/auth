from django.db import models
# 1번 방식을 위해 필요 from accounts.models import User
from django.conf import settings
# from django.contrib.auth import get_user_model

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # 1. 직접참조 - 해당 방식을 추천하지 않음.
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 2. settings.py 변수 활용 - 나는 아마 두 번째 방식을 선호할 것 같네요.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # # 3. get_user_model
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)