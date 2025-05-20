from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from management.member.models import UserProfile
from TripWeb_NFT_Management.createAccount import get_account_info
from TripWeb_NFT_Management.mintAndBurnNFT import get_tokens
from management.tokens.models import TripToken


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('trip')
        else:
            print("⚠️ 註冊表單驗證失敗！錯誤內容：", form.errors)  # <== 加上這行印出錯誤
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('trip')
#     else:
#         form = RegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def login(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('/trip')
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = auth.authenticate(username=username, password=password)
#     if user is not None and user.is_active:
#         auth.login(request, user)
#         return HttpResponseRedirect("/trip")
#     else:
#         return render(request, 'login.html', locals())
    
def main_page(request):
    return render(request, 'main_page.html')

def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect('/main_page')

# @login_required
# def profile(request):
#     user = request.user
#     try:
#         profile = user.profile
#         xrpl_data = get_account_info(profile.xrpl_address)
#         xrpl_nfts = get_tokens(profile.xrpl_address).get("account_nfts", [])  # ✅ 取得 NFT 清單
#     except Exception as e:
#         xrpl_data = None
#         xrpl_nfts = []
#         print(f"⚠️ XRPL 資訊獲取失敗：{e}")

#     tokens = TripToken.objects.filter(owner=user).select_related("trip_schedule", "trip_schedule__trip")

#     return render(request, "profile.html", {
#         "user": user,
#         "profile": profile,
#         "xrpl_data": xrpl_data,
#         "xrpl_nfts": xrpl_nfts,  # ✅ 傳入模板
#         "tokens": tokens,
#     })

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
        xrpl_data = get_account_info(profile.xrpl_address)

        # ✅ 加上手動 HEX 解碼器
        def hex_to_str(hex_str):
            try:
                return bytes.fromhex(hex_str).decode("utf-8")
            except Exception:
                return "Invalid HEX"

        from uuid import UUID
        from management.order.models import TripOrder
        import re

        nft_data = get_tokens(profile.xrpl_address)["account_nfts"]
        print(nft_data)
        for nft in nft_data:
            try:
                decoded_uri = hex_to_str(nft["URI"])
                nft["decoded_uri"] = decoded_uri

                match = re.search(r'/metadata/([0-9a-f-]+)/?$', decoded_uri)
                if match:
                    order_id = UUID(match.group(1))
                    nft["order"] = TripOrder.objects.get(id=order_id)
                else:
                    nft["order"] = None
            except Exception as e:
                nft["decoded_uri"] = "❌ Invalid URI"
                nft["order"] = None

    except Exception as e:
        xrpl_data = None
        nft_data = []
        print(f"⚠️ XRPL 資訊獲取失敗：{e}")

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'xrpl_data': xrpl_data,
        'nft_data': nft_data,
    })



# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_my_profile(request):
#     user = request.user
#     return Response({
#         "username": user.username,
#         "email": user.email,
#         "is_staff": user.is_staff,
#         "groups": [g.name for g in user.groups.all()],
#     })
