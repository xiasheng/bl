
from django.conf.urls import patterns, include, url

from views.account import Register, QuickRegister,ShowAllAccounts, ResetPassword, ForgetPassword, CreateTestUsers, DeleteTestUsers
from views.auth import RequireLogin, Login, Logout, ShowOnlineUsers
from views.profile import UpdateProfile, GetProfile
from views.file import UploadMessageFile

urlpatterns = patterns('',

    url(r'^account/register/$', Register),
    url(r'^account/quickregister/$', QuickRegister),
    url(r'^account/resetpassword/$', ResetPassword),
    url(r'^account/forgetpassword/$', ForgetPassword),
    url(r'^account/showall/$', ShowAllAccounts),
    url(r'^account/createtestuser/$', CreateTestUsers),
    url(r'^account/deletetestuser/$', DeleteTestUsers),

    url(r'^auth/login/$', Login),
    url(r'^auth/logout/$', RequireLogin(Logout)),
    url(r'^auth/showall/$', ShowOnlineUsers),

    url(r'^profile/update/$', RequireLogin(UpdateProfile)),
    url(r'^profile/show/$', RequireLogin(GetProfile)),

    url(r'^file/upload/$', RequireLogin(UploadMessageFile)),
)
