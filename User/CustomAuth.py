# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import smart_text
from .models import CustomUser as MyUser
import re
import requests
import uuid

class CustomAuth(object):
    def authenticate(self, username=None, password=None, update_user=False):
        try:
            localuser = MyUser.objects.get(username=username)
            if localuser.check_password(raw_password=password) and localuser.is_superuser:
                return localuser
        except:
            pass

        try:
            localuser = MyUser.objects.get(username=username)
        except:
            localuser = None

        loginUrl = 'https://ucilnica.fri.uni-lj.si/login/index.php'

        response = requests.post(loginUrl, dict(username=username, password=password, verify=False, allow_redirects=False))
        cookies = dict(MoodleSession=response.request._cookies['MoodleSession'])

        if response.status_code is 200:
            try:
                return MyUser.objects.get(username='ucilnicaDown')
            except:
                self.register('ucilnicaDown', 'ucilnica Down', 123123123, is_active=False)
                return MyUser.objects.get(username='ucilnicaDown')

        if (response.url != 'https://ucilnica.fri.uni-lj.si/my/'):
            try:
                return MyUser.objects.get(username='incorrectCredentials')
            except:
                self.register('incorrectCredentials', 'incorrect Credentials', 123123123, is_active=False)
                return MyUser.objects.get(username='incorrectCredentials')

        if localuser is not None and not update_user:
            return localuser

        # parse name and profile id
        profile = re.findall(
            r'Prijavljeni ste kot <a href="https://ucilnica.fri.uni-lj.si/user/profile.php\?id=(\d+)" title="Poglej profil">(.*?)</a>',
            response.content)

        id = int(profile[0][0])
        name = smart_text(profile[0][1], encoding='utf-8', strings_only=False, errors='strict').title()

        # get student id
        editProfileUrl = 'https://ucilnica.fri.uni-lj.si/user/edit.php?id=' + str(id)
        response = requests.get(editProfileUrl, cookies=cookies, verify=False)

        studentId = re.findall(
            r'<input maxlength="255" size="25" name="idnumber" type="text" value="(\d{8})" id="id_idnumber" />',
            response.content)

        if len(studentId) == 0 or (len(studentId) != 0 and len(studentId[0]) != 8):
            try:
                return MyUser.objects.get(username='noStudentId')
            except:
                self.register('noStudentId', 'noStudent Id', 123123123, is_active=False)
                return MyUser.objects.get(username='noStudentId')
        else:
            studentId = studentId[0]

        if localuser is None:
            self.register(username, name, studentId)
        else:
            flname = re.findall(r'^(.*?) (.*?)$', name)
            fname = flname[0][0]
            lname = flname[0][1]
            localuser.first_name = fname
            localuser.last_name = lname
            localuser.studentId = studentId
            localuser.save()

        try:
            localuser = MyUser.objects.get(username=username)
        except:
            return None

        return localuser

    def register(self, mail, name, sid, is_active=True):
        flname = re.findall(r'^(.*?) (.*?)$', name)
        fname = flname[0][0]
        lname = flname[0][1]
        user = MyUser(username=mail, email='', password=str(uuid.uuid4()), first_name=fname, last_name=lname,
                      studentId=sid, is_active=is_active)
        return user.save()

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

