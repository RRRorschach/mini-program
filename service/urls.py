from django.urls import path

from . import views

urlpatterns = [
    path('testRequest/', views.testRequest, name='testRequest'),
    path('showImage/<str:fileName>/', views.showImage, name='showImage'),
    path('showFace/<str:fileName>/', views.showFace, name='showFace'),
    path('login/', views.login, name='login'),
    path('registerTeacher/', views.registerTeacher, name='registerTeacher'),
    path('registerStudent/', views.registerStudent, name='registerStudent'),
    path('getSignInData/', views.getSignInData, name='getSignInData'),
    path('startSignIn/', views.startSignIn, name='startSignIn'),
    path('cancelSignIn/', views.cancelSignIn, name='cancelSignIn'),
    path('signIn/', views.signIn, name='signIn'),
    path('updateFace/', views.updateFace, name='updateFace'),
    path('signedInStudents/', views.signedInStudents, name='signedInStudents'),
    path('signInLog/', views.signInLog, name='signInLog'),
    path('getCourse/', views.getCourse, name='getCourse'),
    path('getIfHasSigned/', views.getIfHasSigned, name='getIfHasSigned'),
    path('addSup/', views.addSup, name='addSup'),
    path('getSup/', views.getSup, name='getSup'),
    path('confirmSup/', views.confirmSup, name='confirmSup'),
    path('refuseSup/', views.refuseSup, name='refuseSup'),

]