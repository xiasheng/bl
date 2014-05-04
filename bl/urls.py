
from django.conf.urls import patterns, include, url

from views.account import Register, QuickRegister,ShowAllAccounts, ResetPassword, ForgetPassword, CreateTestUsers, DeleteTestUsers
from views.auth import RequireLogin, Login, Logout, LoginTestUsers, ShowOnlineUsers
from views.profile import UpdateProfile, GetProfile, AddPhoto, DelPhoto, ListPhoto
from views.file import UploadMessageFile
from views.status import PostStatus, GetStatusByID, GetStatusByUser

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
    url(r'^auth/logintestuser/$', LoginTestUsers), 
    url(r'^auth/showall/$', ShowOnlineUsers),

    url(r'^profile/update/$', RequireLogin(UpdateProfile)),
    url(r'^profile/show/$', RequireLogin(GetProfile)),
    url(r'^profile/photo/add/$', RequireLogin(AddPhoto)),
    url(r'^profile/photo/del/$', RequireLogin(DelPhoto)),
    url(r'^profile/photo/list/$', RequireLogin(ListPhoto)),

    url(r'^status/post/$', RequireLogin(PostStatus)),
    url(r'^status/show/id/$', RequireLogin(GetStatusByID)),
    url(r'^status/show/user/$', RequireLogin(GetStatusByUser)),
    url(r'^file/upload/$', RequireLogin(UploadMessageFile)),
)
