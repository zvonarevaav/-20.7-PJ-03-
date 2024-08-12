from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import (
    AnnouncementsList,
    AnnouncementDetail,
    CategoryListView,
    SearchAnnouncementsList,
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementDelete,
    IndexView,
    logout_user,
    subscribe,
    upgrade_me
)

urlpatterns = [
    path('announcements/', AnnouncementsList.as_view(), name='announcements'),
    path('announcements/<int:pk>', AnnouncementDetail.as_view(), name='announcement'),
    path('announcements/search/', SearchAnnouncementsList.as_view(), name='search'),
    path('announcement/create/', AnnouncementCreate.as_view(), name='announcement_create'),
    path('announcement/<int:pk>/edit', AnnouncementUpdate.as_view(), name='announcement_edit'),
    path('announcements/<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('user_page/', IndexView.as_view(template_name="user_page.html"), name='user_page'),
    path('logout/user', logout_user, name='logout_user'),
    path('upgrade/', upgrade_me, name='upgrade_status'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
