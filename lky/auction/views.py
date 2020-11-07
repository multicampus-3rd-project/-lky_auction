from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.models import User

from .forms import registerForm
from .models import Product

from user.models import My_user
from PIL import Image

import uuid
import datetime

# Create your views here.
from datetime import datetime

def index(request):
    product = Product.objects.all().order_by('-pub_date')[:6]
    user_id=request.user
    credit=My_user.objects.get(user_id=user_id.id)

    # 경매 마감날짜 지나면 데이터 삭제 - 나중에 테스트해봐야 함
    # today = datetime.now()
    # for p in product:
    #     if p.end_date < today:
    #         print("경매 마감 -> 데이터 삭제")
    #         p.delete()

    return render(request, 'auction/index.html', {'product': product, 'credit':credit})


# def auctionRegister(request):
#     return render(request, 'auction/auction_register.html')

def auctionRegister(request):
    # return render(request, 'auction/auction_register.html')
    if request.method == 'POST':
        file_data = request.FILES
        file_name = file_data['photo'].name
        idx = list(file_name).index('.')
        f_type_list = list(file_name)[idx:]
        f_type = ''.join(f_type_list)
        data_name = str(datetime.now())[:10] + '-' + str(uuid.uuid1()) + f_type
        file_data['photo'].name = data_name
        form = registerForm(request.POST, request.FILES)

        if form.is_valid():
            prod = form.save(commit=False)
            thumbnail_name = 'thumbnail-' + data_name
            prod.thumbnail = thumbnail_name
            # prod.author = request.user
            # prod.published_date = timezone.now()
            prod.save()
            img = Image.open(settings.MEDIA_ROOT + data_name)
            img_resize = img.resize((int(img.width / (img.height / 240)), 240))
            img_resize.save(settings.MEDIA_ROOT + thumbnail_name)

            return redirect('index')
    else:
        form = registerForm()

    return render(request, 'auction/auction_register.html', {'form': form})



# 홈 상단 바 - 크레딧 충전 클릭
def auction_credit(request):
    return render(request,'auction/auction_credit.html')


# auction_credit.html에서 실행할 충전 함수
# 현재 로그인 중인 auth_user의 id에 해당하는 크레딧을 50000원 증가시킨다.
def charging(request):
    user_id=request.user
    print(user_id.id)

    now_credit=My_user.objects.get(user_id=user_id.id)
    now_credit.credit=int(now_credit.credit)+50000
    now_credit.save()
    return render(request,'auction/auction_credit.html')


# def showProductList(request):
#     product = Product
#     return render(request, product)


def auction_list(request):
    id = request.POST.get("products", None)
    print(id)
    product=Product.objects.filter(category=id).order_by('-pub_date')[:6]
    print(product)
    return render(request,'auction/auction_list.html',{"product":product})

def do_bid(request):

    if request.POST:
        input_price = int(request.POST['bid-value'])
        min_price = int(request.POST['product-min'])
        max_price = int(request.POST['product-max'])
        product_id=request.POST['product-id']
        now_max = Product.objects.get(id=product_id)

        user_id = request.user
        now_credit = My_user.objects.get(user_id=user_id.id)
        if input_price>min_price and input_price>max_price and now_credit.credit>input_price:
            now_max.max_price = input_price
            now_max.save()
            now_credit.credit =int(now_credit.credit)-input_price
            now_credit.save()
            print(min_price,max_price,input_price,now_credit)
        return redirect('/')
    else:
        return redirect('/')


