from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('like/<int:pk>', views.LikeView, name='like_post'),
    # autenticate user
    path('login/', views.LoginUser.as_view(), name='login'),
    path('signup/', views.UserRegister.as_view(), name='signup'),

    path('signout/', LogoutView.as_view(next_page='home'), name='signout'),

    path('homepage/', views.homePage, name='home'),

    path('post-create/', views.PostCreate.as_view(), name='post-create'),
    path('post-update/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('post-detail/<int:pk>', views.PostDetail.as_view(), name='post-detail'),
    path('delete_post/<int:pk>', views.PostDelete.as_view(), name='delete_post'),
    path('post-category/<str:cats>', views.PostCatagory, name='post-category'),

    path('profile/', views.profile, name='profile'),
    path('edit-profile/<int:pk>', views.ProfileUpdate.as_view(), name='edit-profile'),
    path('get-profile/<int:pk>', views.ViewProfile.as_view(), name='get-profile'),

    path('add-comment/<int:pk>', views.AddPostComment.as_view(), name='add-comment'),
    path('view-comment/<int:pk>', views.PostComment.as_view(), name='view-comment'),
    path('edit-comment/<int:pk>', views.EditComment.as_view(), name='edit-comment'),
    path('delete-comment/<int:pk>',
         views.DeleteComment.as_view(), name='delete-comment'),

    path('add-user/', views.RegisterAdmin.as_view(), name='add-user'),
    path('users/', views.UserView.as_view(), name='users'),
    path('edit-user/<int:pk>', views.UpdateUserStatus.as_view(), name='edit_user'),
    path('delete-user/<int:pk>', views.DeleteUser.as_view(), name='delete-user'),

    # reply for comment urls
    path('add-reply/<int:pk>', views.ReplyForComment.as_view(), name='add-reply'),
    path('view-reply/<int:pk>', views.ReplyLists.as_view(), name='view-reply'),

    # change password urls
    path('password/', views.ChangePassword.as_view(), name='change-password'),


    # sucsessfull urls
    path('registered-succsess', views.successful_registered,
         name='registered-succsess'),
    path('password-changed', views.successful_change_password,
         name='password-changed'),

   #JSON AND AJAX URLS
   path('json-list/',views.getPostAjax,name='json-list'),      
   path('json-home/',views.jsonHome,name='json-home') ,     
    # password reset urls
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password/password_reset_form.html'), name='password-reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='blog/change-password.html'),
        name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'), name='password_reset_complete'),

       
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
