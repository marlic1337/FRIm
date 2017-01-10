from .models import CustomUser as MyUser
import re
import requests
import uuid

class CustomAuth(object):
    def authenticate(self, username=None, password=None):
        try:
            localuser = MyUser.objects.get(username=username, password=password)
            if localuser.is_superuser:
                return localuser
        except:
            localuser = None

        try:
            localuser = MyUser.objects.get(username=username)
        except:
            localuser = None

        loginUrl = 'https://ucilnica.fri.uni-lj.si/login/index.php'

        response = requests.post(loginUrl, dict(username=username, password=password, verify=False, allow_redirects=False))
        cookies = dict(MoodleSession=response.request._cookies['MoodleSession'])

        if (response.url != 'https://ucilnica.fri.uni-lj.si/my/'):
            return None

        if localuser is not None:
            return localuser

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
        if len(studentId[0]) is not 8:
            return None
        else:
            studentId = studentId[0]

        self.register(username, name, studentId)
        try:
            localuser = MyUser.objects.get(username=username)
        except:
            return None

        return localuser

    def register(self, mail, name, sid):
        flname = re.findall(r'^(.*?) (.*?)$', name)
        fname = flname[0][0]
        lname = flname[0][1]
        user = MyUser(username=mail, email='empty@email.com', password=str(uuid.uuid4()), first_name=fname, last_name=lname,
                      studentId=sid)
        return user.save()

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None
