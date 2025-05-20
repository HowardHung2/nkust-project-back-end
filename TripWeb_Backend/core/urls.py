from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 管理後台
    path("admin/", admin.site.urls),

    # 各 app 路由註冊
    path('member/', include('management.member.urls')),
    path('order/', include('management.order.urls')),
    path('trip/', include('management.trip.urls')),
    path('tokens/', include('management.tokens.urls')),

    # Django 內建帳號功能：login/logout/password
    path('accounts/', include('django.contrib.auth.urls')),

    # 預設跳轉首頁（你可改成導向 trip main）
    path('', RedirectView.as_view(url='/trip/')),

    # # 1) 登录（获取 access + refresh）
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # # 2) 刷新 access
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # # 3) 登出（注销 refresh，选用）
    # path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('token/', include('management.tokens.urls')),  # 加入這一行
    path('', include('management.tokens.urls')),  # 加上這行
]

# 加上 static files 設定（僅限 DEBUG 模式）
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
