from asyncio.windows_events import NULL
import json
import os
from . import dataProcessing,faceRecognition
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from backend import settings

#测试函数
def testRequest(request):
    # res=dataProcessing.test()
    res=0
    return HttpResponse(res)

#设置图片路由
def showImage(request,fileName):
    path = os.path.join(settings.IMAGES_DIR,fileName) 
    image = open(path,"rb").read() 
    return HttpResponse(image,content_type="image/jpg")
def showFace(request,fileName):
    path = os.path.join(settings.FACES_DIR,fileName) 
    image = open(path,"rb").read() 
    return HttpResponse(image,content_type="image/jpg")

#用户登录
def login(request):
    code=json.loads(request.body)['code']
    openId=dataProcessing.getOpenId(code)
    res=dataProcessing.getIfHasLogin(openId)
    return JsonResponse(res)

#注册教师
def registerTeacher(request):
    openId=json.loads(request.body)['openId']
    identity=json.loads(request.body)['identity']
    name=json.loads(request.body)['name']
    number=json.loads(request.body)['number']

    if dataProcessing.getTeacherRegisterResult(name,number)==201:
        res={'code':201}
    else:
        if dataProcessing.getTeacherRegisterResult(name,number)==202:
            res={'code':202}
        else:
            res=dataProcessing.updateTeacherUser(openId,identity,name)
            res.update({'code':200})
    return JsonResponse(res)
    
#注册学生
def registerStudent(request):
    openId = request.POST.get('openId')
    identity = request.POST.get('identity')
    name = request.POST.get('name')
    number = request.POST.get('number')
    image = request.FILES.get('image',None).read()
    if dataProcessing.getIfNumberHasRegistered(number):
        res={'code':201}
    else:
        faceUrl=dataProcessing.uploadImage(image,number)
        res=dataProcessing.createStudentUser(openId,identity,name,number,faceUrl)
        res.update({'code':200})
    return JsonResponse(res)

#签到界面
def getSignInData(request):
    identity=json.loads(request.body)['identity']
    number=json.loads(request.body)['number']
    if dataProcessing.getSignInState(identity,number):
        res=dataProcessing.selectLatestSignInForTeacher(identity,number)
        res.update({'code':200})
    else:
        res=dataProcessing.selectCourse(number)
        res.update({'code':201})
    return JsonResponse(res)

#发起签到
def startSignIn(request):
    courseId=json.loads(request.body)['courseId']
    number=json.loads(request.body)['number']
    section=json.loads(request.body)['section']
    startTime=json.loads(request.body)['startTime']
    time=json.loads(request.body)['time']
    longitude=json.loads(request.body)['longitude']
    latitude=json.loads(request.body)['latitude']
    # print(json.loads(request.body))
    # print(latitude)
    dataProcessing.insertSignInForTeacher(courseId,number,section,startTime,time,longitude,latitude)
    res={'code':200}
    return JsonResponse(res)

#取消签到
def cancelSignIn(request):
    courseId=json.loads(request.body)['courseId']
    section=json.loads(request.body)['section']
    dataProcessing.deleteSignInForTeacher(courseId,section)
    res={'code':200}
    return JsonResponse(res)

#人脸识别签到
def signIn(request):
    #获取请求体中数据
    courseId = request.POST.get('courseId')#课程ID
    number = request.POST.get('number')#学号
    section = request.POST.get('section')#课程节次
    time = request.POST.get('time')#签到时间
    longitude = request.POST.get('longitude')#定位经度
    latitude = request.POST.get('latitude')#定位纬度
    image = request.FILES.get('image',None).read()#人脸识别图片

    # if longitude=='':
    #     predictRes=faceRecognition.predict(image)
    #     if predictRes['label']==int(number):
    #         dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
    #         res={'code':200}#未定位 人脸识别成功
    #     else:
    #         res={'code':201}#未定位 人脸识别失败
    # else:
    #     if dataProcessing.ifWithinRange(courseId,section,longitude,latitude):
    #         predictRes=faceRecognition.predict(image)
    #         if predictRes['label']==int(number):
    #             dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
    #             res={'code':200}#定位 在范围内 人脸识别成功
    #         else:
    #             res={'code':201}#定位 在范围内 人脸识别失败
    #     else:
    #         res={'code':202}#定位 在范围外
    # return JsonResponse(res)#返回结果
    if longitude=='999':
        longitude=NULL
        latitude=NULL
        predictRes=faceRecognition.predict(image)
        # print(predictRes)
        if predictRes['label']==int(number):
            dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
            res={'code':200}
        else:
            dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
            res={'code':201}
            res={'code':200}
    else:
        if dataProcessing.ifWithinRange(courseId,section,longitude,latitude):
            predictRes=faceRecognition.predict(image)
            if predictRes['label']==int(number):
                dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
                res={'code':200}
            else:
                dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
                res={'code':201}
                res={'code':200}
        else:
            dataProcessing.insertSignInForStudent(courseId,number,section,time,longitude,latitude)
            res={'code':202}   
            res={'code':200}
    return JsonResponse(res)

#更新人脸
def updateFace(request):
    # openId = request.POST.get('openId')
    number = request.POST.get('number')
    image = request.FILES.get('image',None).read()
    # print(type(image))
    faceUrl=dataProcessing.uploadImage(image,number)
    # dataProcessing.updateFaceUrl(openId,faceUrl)
    # print(faceUrl)
    # res={'code':200,'faceUrl':faceUrl}
    res={'code':200}
    return JsonResponse(res)

#签到记录
def signedInStudents(request):
    courseId=json.loads(request.body)['courseId']
    section=json.loads(request.body)['section']
    res=dataProcessing.selectSignInRecord(courseId,section)
    return JsonResponse(res)

def signInLog(request):
    number=json.loads(request.body)['number']
    identity=json.loads(request.body)['identity']
    res=dataProcessing.selectSignInLog(number,identity)
    return JsonResponse(res)

def getCourse(request):
    number=json.loads(request.body)['number']
    res=dataProcessing.selectCourse(number)
    return JsonResponse(res)

def getIfHasSigned(request):
    number=json.loads(request.body)['number']
    courseId=json.loads(request.body)['courseId']
    section=json.loads(request.body)['section']
    res=dataProcessing.selectSignInForStudent(number,courseId,section)
    return JsonResponse(res)

def addSup(request):
    courseId=json.loads(request.body)['courseId']
    number=json.loads(request.body)['number']
    section=json.loads(request.body)['section']
    time=json.loads(request.body)['time']
    reason=json.loads(request.body)['reason']
    dataProcessing.insertSupSignIn(courseId,number,section,time,reason)
    res={'code':200}
    return JsonResponse(res)

def getSup(request):
    number=json.loads(request.body)['number']
    res=dataProcessing.selectSupSignIn(number)
    return JsonResponse(res)

def confirmSup(request):
    id=json.loads(request.body)['id']
    courseId=json.loads(request.body)['courseId']
    number=json.loads(request.body)['number']
    section=json.loads(request.body)['section']
    time=json.loads(request.body)['time']
    dataProcessing.insertSignInForStudent(courseId,number,section,time,NULL,NULL)
    dataProcessing.updateSupState(id)
    res={'code':200}
    return JsonResponse(res)

def refuseSup(request):
    id=json.loads(request.body)['id']
    dataProcessing.updateSupState(id)
    res={'code':200}
    return JsonResponse(res)



















