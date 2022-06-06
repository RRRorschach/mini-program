import datetime
import json
import os
from pickle import TRUE
import time
import requests
from haversine import haversine,Unit
from backend import settings
from .models import Course, CourseForUser, SignInForStudent, SignInForTeacher, SupSignIn, User

def test():
    # print(selectLatestSignInForTeacher(0,123))
    # a=datetime.datetime.now()
    # b=datetime.datetime(2022, 5, 5, 2, 14, 49)
    # print(a<b)


    # res=selectSignInRecord('[SE31213]-001',2)
    res=0
    return res
    # return 0

#获取openId
def getOpenId(code):
    url='https://api.weixin.qq.com/sns/jscode2session?'
    data={
        'appid':'wxde2ea8736e13db88',
        'secret':'13594bbdc87cbd9638d88830843853a4',
        'js_code': code,
        'grant_type':'authorization_code',
    }
    res = requests.get(url, params=data)
    res_json=json.loads(res.content.decode('utf-8'))
    # print(res_json)
    openId=res_json.get('openid')
    return openId

#该微信用户是否第一次登录
def getIfHasLogin(openId):
    #微信第一次登录
    if User.objects.filter(openId=openId).count()==0:
        #dict
        return {'openId':openId}
    #微信已经登录过
    else:
        #dict
        # print('已经登录过')
        return User.objects.filter(openId=openId).values()[0]

#查询教师注册情况
def getTeacherRegisterResult(name,number):
    if User.objects.filter(identity=None,name=name).count()==0:
        #还没分配账号
        return 201
    else:
        if User.objects.filter(identity=None,name=name).values()[0]['number']!=number:
            #输入了错误的账号
            return 202
        else:
            #可以注册
            return 200

#注册教师
def updateTeacherUser(openId,identity,name):
    User.objects.filter(identity=None,name=name).update(openId=openId,identity=identity)
    return User.objects.filter(openId=openId).values()[0]

#上传图片
def uploadImage(image,number):
    # timeStr = time.strftime("%Y-%m-%d_%H-%M-%S")
    # fileName=number+'_'+timeStr+'.jpg'
    fileName=number+'.jpg'
    path = os.path.join(settings.FACES_DIR,fileName) 
    with open(path,'wb') as f:
        f.write(image)
    imageUrl='http://127.0.0.1:8000/service/showFace/'+fileName   
    return imageUrl

#查询学生账号是否已被使用
def getIfNumberHasRegistered(number):
    if User.objects.filter(number=number).count()==0:
        return False
    else:
        return True

#注册学生
def createStudentUser(openId,identity,name,number,faceUrl):
    User.objects.create(openId=openId,identity=identity,name=name,number=number,faceUrl=faceUrl)
    return User.objects.filter(openId=openId).values()[0]

# #获取课程信息
# def selectCourse(number):
#     courseIdList=CourseForUser.objects.filter(number=number).values('courseId')
#     currentCourseList=[]
#     for item in courseIdList:
#         currentCourseDict=Course.objects.filter(courseId=item['courseId']).values()[0]
#         if datetime.datetime.now()<currentCourseDict['endTime']:
#             if SignInForTeacher.objects.filter(courseId=item['courseId']).count()>0:
#                 section=SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-section').values('section')[0]['section']
#                 currentCourseDict.update({'section':section})
#                 currentCourseList.append(currentCourseDict)
#             else:
#                 currentCourseDict.update({'section':0})
#                 currentCourseList.append(currentCourseDict)
#     courseDict={'currentCourseList':currentCourseList}
#     return courseDict
#获取发起签到最新记录
def selectLatestSignInForTeacher(identity,number):
    if identity==0:
        latestRecord=SignInForTeacher.objects.filter(number=number).order_by('-endTime').values()[0]
        courseId=latestRecord['courseId']
        courseNameDict=Course.objects.filter(courseId=courseId).values('courseName')[0]
        latestRecord.update(courseNameDict)
        latestRecord['endTime']=str(latestRecord['endTime'])      
        latestRecord['startTime']=str(latestRecord['startTime'])      
        return latestRecord
    if identity==1:
        courseIdList=CourseForUser.objects.filter(number=number).values('courseId')
        latestTime=datetime.datetime.now()
        # latestRecord={}
        for item in courseIdList:
            if SignInForTeacher.objects.filter(courseId=item['courseId']).count()>0:
                if latestTime<SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-endTime').values('endTime')[0]['endTime']:
                    latestTime=SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-endTime').values('endTime')[0]['endTime']
                    latestRecord=SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-endTime').values()[0]
        courseId=latestRecord['courseId']
        courseNameDict=Course.objects.filter(courseId=courseId).values('courseName')[0]
        latestRecord.update(courseNameDict)
        latestRecord['endTime']=str(latestRecord['endTime'])   
        latestRecord['startTime']=str(latestRecord['startTime'])
        ifSignIn=getIfSignIn(courseId,number,latestRecord['section'])
        if ifSignIn:
            time=str(SignInForStudent.objects.filter(courseId=courseId,number=number,section=latestRecord['section']).values('time')[0]['time'])
            latestRecord.update({'ifSignIn':ifSignIn,'time':time})
        else:
            latestRecord.update({'ifSignIn':ifSignIn})
        return latestRecord
#是否已签到
def getIfSignIn(courseId,number,section):
    if SignInForStudent.objects.filter(courseId=courseId,number=number,section=section).count()>0:
        return True
    else:
        return False
#获取签到状态
def getSignInState(identity,number):
    if identity==0:
        if SignInForTeacher.objects.filter(number=number).count()>0:
            latestTime=SignInForTeacher.objects.filter(number=number).order_by('-endTime').values('endTime')[0]['endTime']
            # print(latestTime)
            if (datetime.datetime.now()-latestTime).total_seconds()>0:
                return False
            else:
                return True
        else:
            return False
    if identity==1:
        courseIdList=CourseForUser.objects.filter(number=number).values('courseId')
        endTimeList=[]
        for item in courseIdList:
            if SignInForTeacher.objects.filter(courseId=item['courseId']).count()>0:
                endTimeList.append(SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-endTime').values('endTime')[0]['endTime'])
        # print(endTimeList)
        if endTimeList:
            if ((datetime.datetime.now()-max(endTimeList)).total_seconds()>0):
                return False
            else:
                return True
        else:
            return False

#添加发起签到
def insertSignInForTeacher(courseId,number,section,startTime,time,longitude,latitude):
    startTime=datetime.datetime.strptime(startTime,"%Y-%m-%d %H:%M:%S")
    endTime=startTime+datetime.timedelta(minutes=int(time)+1)
    SignInForTeacher.objects.create(courseId=courseId,number=number,section=section,startTime=startTime,endTime=endTime,longitude=longitude,latitude=latitude)
    return True

#删除发起签到
def deleteSignInForTeacher(courseId,section):
    SignInForTeacher.objects.filter(courseId=courseId,section=section).delete()
    SignInForStudent.objects.filter(courseId=courseId,section=section).delete()
    return True

#判断位置
def ifWithinRange(courseId,section,longitude,latitude):
    longitudeForTeacher=SignInForTeacher.objects.filter(courseId=courseId,section=section).values('longitude')[0]['longitude']
    latitudeForTeacher=SignInForTeacher.objects.filter(courseId=courseId,section=section).values('latitude')[0]['latitude']
    teacherLoc=(latitudeForTeacher,longitudeForTeacher)
    studentLoc=(float(latitude),float(longitude))
    dis = haversine(teacherLoc,studentLoc)
    if dis<=0.1:
        return True
    else:
        return False

#添加签到
def insertSignInForStudent(courseId,number,section,time,longitude,latitude):
    time=datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
    SignInForStudent.objects.create(courseId=courseId,number=number,section=section,time=time,longitude=longitude,latitude=latitude)
    return True

# #更新faceUrl
# def updateFaceUrl(openId,faceUrl):
#     User.objects.filter(openId=openId).update(faceUrl=faceUrl)
#     return True

#课程、节次签到记录
def selectSignInRecord(courseId,section):
    signedInListQ=SignInForStudent.objects.filter(courseId=courseId,section=section).values()
    signedInList=[]
    for item in signedInListQ:
        item.update(User.objects.filter(number=item['number']).values()[0])
        item['time']=str(item['time'])
        signedInList.append(item)


    signedInNumberListQ=SignInForStudent.objects.filter(courseId=courseId,section=section).values('number')
    signedInNumberList=[]
    for item in signedInNumberListQ:
        signedInNumberList.append(item['number'])
    
    #获取学号List
    numberListQ=CourseForUser.objects.filter(courseId=courseId).values('number')
    studentNumberList=[]
    for item in numberListQ:
        if User.objects.filter(number=item['number']).values('identity')[0]['identity']==1:
            studentNumberList.append(item['number'])
    notsignedInList=[]
    for item in studentNumberList:
        if item not in signedInNumberList:
            notsignedInList.append(User.objects.filter(number=item).values()[0]) 
    res={'signedInList':signedInList,'notsignedInList':notsignedInList}
    return res

def selectSignInLog(number,identity):
    if identity==0:
        signInLogList=[]
        signInLogListQ=SignInForTeacher.objects.filter(number=number).values()
        for item in signInLogListQ:
            item['startTime']=str(item['startTime'])
            item['endTime']=str(item['endTime'])
            item.update(Course.objects.filter(courseId=item['courseId']).values('courseName')[0])
            signInLogList.append(item)
        res={'signInLogList':signInLogList}
        return res
    if identity==1:
        signInLogList=[]
        signInLogListQ=SignInForStudent.objects.filter(number=number).values()
        for item in signInLogListQ:
            item['time']=str(item['time'])
            item.update(Course.objects.filter(courseId=item['courseId']).values('courseName')[0])
            signInLogList.append(item)
        res={'signInLogList':signInLogList}
        return res

def selectCourse(number):
    courseIdListQ=CourseForUser.objects.filter(number=number).values('courseId')
    currentCourseList=[]
    historyCourseList=[]
    for item in courseIdListQ:
        thisCourseDict=Course.objects.filter(courseId=item['courseId']).values()[0]
        if datetime.datetime.now()<thisCourseDict['endTime']:
            if SignInForTeacher.objects.filter(courseId=item['courseId']).count()>0:
                section=SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-section').values('section')[0]['section']
                thisCourseDict.update({'maxSection':section})
                currentCourseList.append(thisCourseDict)
            else:
                thisCourseDict.update({'maxSection':0})
                currentCourseList.append(thisCourseDict)
        else:
            if SignInForTeacher.objects.filter(courseId=item['courseId']).count()>0:
                section=SignInForTeacher.objects.filter(courseId=item['courseId']).order_by('-section').values('section')[0]['section']
                thisCourseDict.update({'maxSection':section})
                historyCourseList.append(thisCourseDict)
            else:
                thisCourseDict.update({'maxSection':0})
                historyCourseList.append(thisCourseDict)
    courseDict={'currentCourseList':currentCourseList,'historyCourseList':historyCourseList}
    return courseDict

def selectSignInForStudent(number,courseId,section):
    if SignInForStudent.objects.filter(courseId=courseId,number=number,section=section).count()>0:
        signInRecord=SignInForStudent.objects.filter(courseId=courseId,number=number,section=section).values()[0]
        signInRecord['time']=str(signInRecord['time'])
        record={'code':200,'signInRecord':signInRecord}
    else:
        record={'code':201}
    return record

def insertSupSignIn(courseId,number,section,time,reason):
    time=datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
    SupSignIn.objects.create(courseId=courseId,number=number,section=section,time=time,reason=reason,state=1)
    return True

def selectSupSignIn(number):
    courseIdListQ=CourseForUser.objects.filter(number=number).values('courseId')
    supSignInList=[]
    for item in courseIdListQ:
        thisSupSignInQ=SupSignIn.objects.filter(courseId=item['courseId']).values()
        for t in thisSupSignInQ:
            t['time']=str(t['time'])
            thisCourseName=Course.objects.filter(courseId=t['courseId']).values('courseName')[0]['courseName']
            thisName=User.objects.filter(number=t['number']).values('name')[0]['name']
            t.update({'courseName':thisCourseName,'name':thisName})
            supSignInList.append(t)
    res={'supSignInList':supSignInList}
    return res

def updateSupState(id):
    SupSignIn.objects.filter(id=id).update(state=0)
    return True











    
    
