from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Product(models.Model):
    # 상품명
    name = models.CharField(max_length=60, default='')
    # 사진 -> media file 설정 해주기
    photo = models.ImageField(blank=True, null=True)
    # 썸네일
    thumbnail = models.CharField(max_length=60, default='')
    # 글 내용
    content = models.TextField()
    register=models.IntegerField(null=False)
    # 최소가격
    min_price = models.IntegerField(default=0)
    # 현재가격 (최대가격)
    max_price = models.IntegerField(default=0)
    
    # 시작일 : 현재 시작
    start_date = models.DateTimeField(default=datetime.now())
    # 마감일 : 3일 후 마감
    end_date = models.DateTimeField(default=datetime.now()+timedelta(days=3))
    # 게시글 등록 날짜
    pub_date = models.DateTimeField(auto_now_add=True)
    # 대분류
    category = models.CharField(max_length=60, default='')
    # 마감유무(True=진행중 / False=마감)
    visible_status = models.BooleanField(default=True)
    last_bidder_id=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name