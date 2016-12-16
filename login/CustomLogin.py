from .models import User
import re
import requests
from django.core.exceptions import PermissionDenied

class CustomLogin(object):
    def authenticate(self, username=None, password=None):
        localuser = User.objects.filter(mail=username)
        if localuser.count() is 1 and not localuser.is_active():
            raise PermissionDenied('User has been suspended.')

        loginUrl = 'https://ucilnica.fri.uni-lj.si/login/index.php'

        response = requests.post(loginUrl, dict(username=username, password=password, verify=False, allow_redirects=False))
        cookies = dict(MoodleSession=response.request._cookies['MoodleSession'])

        if (response.url != 'https://ucilnica.fri.uni-lj.si/my/'):
            raise PermissionDenied('Incorrect email or password.')

        # parse name and profile id
        profile = re.findall(
            r'Prijavljeni ste kot <a href="https://ucilnica.fri.uni-lj.si/user/profile.php\?id=(\d+)" title="Poglej profil">(.*?)</a>',
            response.content)

        id = int(profile[0][0])
        name = profile[0][1].title()

        # get student id
        editProfileUrl = 'https://ucilnica.fri.uni-lj.si/user/edit.php?id=' + str(id)
        response = requests.get(editProfileUrl, cookies=cookies, verify=False)

        studentId = re.findall(
            r'<input maxlength="255" size="25" name="idnumber" type="text" value="(\d{8})" id="id_idnumber" />',
            response.content)
        if not len(studentId) < 1:
            raise PermissionDenied('Invalid student ID.')
        else:
            studentId = studentId[0]

        if localuser is None:
            localuser = self.register(username, name, studentId)
        else:
            localuser = self.updateUserData(localuser[0], name, studentId)

        return localuser

    def register(self, mail, name, sid):
        user = User(displayName=name, mail=mail, studentId=sid, is_active=True)
        user.save()
        return user

    def updateUserData(self, localuser, name, sid):
        localuser.displayName = name
        localuser.studentId = sid
        localuser.save()
        return localuser

    def get_user(self, mailOrUserId):
        try:
            return User.objects.get(pk=mailOrUserId)
        except User.DoesNotExist:
            try:
                return User.objects.get(mail=mailOrUserId)
            except User.DoesNotExist:
                return None
