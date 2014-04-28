
from django.conf.urls import patterns, include, url

from views.account import Register, QuickRegister,ShowAllAccounts, ResetPassword, ForgetPassword
from views.auth import RequireLogin, Login, Logout
from views.profile import UpdateProfile, GetProfile
urlpatterns = patterns('',

    url(r'^account/register/$', Register),
    url(r'^account/quickregister/$', QuickRegister),
    url(r'^account/resetpassword/$', ResetPassword),
    url(r'^account/forgetpassword/$', ForgetPassword),
    url(r'^account/showall/$', ShowAllAccounts),

    url(r'^auth/login/$', Login),
    url(r'^auth/logout/$', RequireLogin(Logout)),

    url(r'^profile/update/$', UpdateProfile),
    url(r'^profile/show/$', GetProfile),

)
