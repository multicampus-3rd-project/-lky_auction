from django.db.models import Q
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.models import User

from .forms import registerForm
from .models import Product

from user.models import My_user
from PIL import Image

import uuid
import datetime

from datetime import datetime


def index(request):
    category_id = request.GET.get("category")

    if category_id is not None:
        product = Product.objects.filter(Q(category=category_id) & Q(visible_status='True')).order_by('-pub_date')[:6]
    else:
        product = Product.objects.filter(visible_status='True').order_by('-pub_date')[:6]

    # 경매 마감시 visible_status = False 로 변환
    today = datetime.now()
    for p in product:
        if p.end_date < today:
            p.visible_status = False
            p.save()

    user_check = request.user.id
    if user_check is not None:
        credit = My_user.objects.get(user_id=user_check)
        context = {
            'product': product,
            'category_id': category_id,
            'credit': credit
        }

    else:
        context = {
            'product': product,
            'category_id': category_id,
        }

    return render(request, 'auction/index.html', context)


def auctionRegister(request):

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
            prod.register=request.user.id
            prod.thumbnail = thumbnail_name
            prod.save()
            img = Image.open(settings.MEDIA_ROOT + data_name)
            img_resize = img.resize((int(img.width / (img.height / 240)), 240))
            img_resize.save(settings.MEDIA_ROOT + thumbnail_name)

        return redirect('index')

    else:
        form = registerForm()

    return render(request, 'auction/auction_register.html', {'form': form})

def auction_credit(request):
    """홈 상단 바 - 크레딧 충전 클릭"""
    user_id = request.user
    if request.method == "POST":
        h_type = request.POST.get('h-type') # 라디오버튼 선택
        print(int(h_type))
        now_credit = My_user.objects.get(user_id=user_id.id)
        now_credit.credit = int(now_credit.credit) + int(h_type)
        now_credit.save()
        return redirect('/') # 충전완료
    else:
        nowuser = My_user.objects.get(user_id=user_id.id)
        context = {'credit' : nowuser.credit}
        return render(request, 'auction/auction_credit.html', context) # 충전하러 들어왔어

def do_bid(request):
    """입찰 시행"""

    if request.POST:
        input_price = int(request.POST['bid-value'])
        min_price = int(request.POST['product-min'])
        max_price = int(request.POST['product-max'])
        product_id = request.POST['product-id']
        now_max = Product.objects.get(id=product_id)
        print(product_id, '!!!!!!!', now_max.id)
        user_id = request.user
        now_credit = My_user.objects.get(user_id=user_id.id)
        print(user_id, now_credit)

        if now_max.register==request.user.id:
            return redirect('/')


        if min_price < input_price <= now_credit.credit and input_price > max_price:

            # 입찰자가 없을 떄
            if now_max.last_bidder_id is None:
                now_max.max_price = input_price
                now_max.last_bidder_id = user_id.id
                now_max.save()
                now_credit.credit = int(now_credit.credit) - input_price
                now_credit.save()

            # 입찰자 재입찰자 같을 때
            elif user_id.id == now_max.last_bidder_id:
                difference = input_price - max_price
                now_max.max_price = input_price
                now_max.save()
                now_credit.credit = int(now_credit.credit) - difference
                now_credit.save()

            else:
                # 입찰자 재입찰자 다를 때
                retrun_credit_id = now_max.last_bidder_id
                print(retrun_credit_id)

                return_credit_credit = now_max.max_price
                return_credit_user = My_user.objects.get(user_id=retrun_credit_id)

                return_credit_user.credit = int(return_credit_user.credit) + int(return_credit_credit)
                return_credit_user.save()

                now_max.max_price = input_price
                now_max.last_bidder_id = user_id.id
                now_max.save()
                now_credit.credit = int(now_credit.credit) - input_price
                now_credit.save()

        return redirect('/')

    else:
        return redirect('/')
