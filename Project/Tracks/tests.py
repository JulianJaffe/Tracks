"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from Tracks.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class GetTest(TestCase):
  def setUp(self):
    self.c = Client()

  def test_get_home(self):
    response = self.c.get('/Tracks/')
    self.assertEqual(response.status_code, 200)

  def test_get_register(self):
    response = self.c.get('/Tracks/register/')
    self.assertEqual(response.status_code, 200)

  def test_get_signin(self):
    response = self.c.get('/Tracks/signin')
    self.assertEqual(response.status_code, 200)

class SignUpTest(TestCase):
  def setUp(self):
    self.c = Client()
    response = self.c.post('/Tracks/register/',{'firstName':'a','lastName':'b','email':'a@a.a', 'password':'a', 'confirm':'a'}, follow=True)

  def test_new_user(self):
    response = self.c.post('/Tracks/register/',{'firstName':'a','lastName':'b','email':'b@b.b', 'password':'b', 'confirm':'b'})
    self.assertEqual(response.status_code, 302)

  def test_duplicate_email(self):
    a = 0
    try:
      response = self.c.post('/Tracks/register/',{'firstName':'c','lastName':'c','email':'a@a.a','password':'c','confirm':'b'})
    except:
      a = 1
    self.assertEqual(a, 1)
"""
  def test_bad_email(self):
    a = 0
    try:
      response = self.c.post('/Tracks/register/',{'firstName':'','lastName':'','email':'','password':'','confirm':''}, follow=True)
    except:
      a = 1
    print(response.status_code)
    print("redirect: " , response.redirect_chain)
    self.assertEqual(a,1)
"""
class SignInTest(TestCase):
  def setUp(self):
    self.c = Client()
    response = self.c.post('/Tracks/register/', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})

  def test_sign_in(self):
    response = self.c.post('/Tracks/signin/',{'email':'a@a.a','password':'a'})
    self.assertEqual(response.status_code, 302)
  def test_user_doesnt_exist(self):
    a = 0
    try:
      response = self.c.post('/Tracks/signin/',{'email':'z@z.z','password':'z'})
    except:
      a = 1
    self.assertEqual(a,1)

  def test_wrong_passsword(self):
    a = 0
    try:
      response = self.c.post('/Tracks/signin/',{'email':'a@a.a','password':'1'})
    except:
      a = 1
    self.assertEqual(a,1)



class UserProfileTest(TestCase):
    def setUp(self):
        self.c = Client()
        response = self.c.post('/Tracks/register/', {'firstName':'a','lastName':'a','email':'a@a.a','password':'a','confirm':'a'})


"""
class TrackTest(TestCase):
class CollaborationTest(TestCase):
class UploadFileTest(TestCase):
	def test_valid_mp3_upload(self):
		filepathOfMp3 = '~/user_mp3_files/valid.mp3'
		#make a request with this file path
		request = self.assertEqual(upload_mp3(request), 'success')
		#then check if the file exists and is identical
		self.assertEqual(getFileFromDatabase, file(filepathOfMp3))
	def test_invalid_file_extension(self):
		filepathOfMp3 = '~/user_mp3_files/badExt.ogg'
		#make a request with this file path
		request = self.assertEqual(self.upload_mp3(request), 'File extension not supported')


	def test_sizeLimitExceeded_file(self):
		filepathOfMp3 = '~/user_mp3_files/long.mp3'
		#make a request with this file path
		request = self.assertEqual(self.upload_mp3(request), 'File exceeding size limit')


	def test_null_name(self):
		filepathOfMp3 = '~/user_mp3_files/ .mp3'
		#make a request with this file path
		request = self.assertEqual(self.upload_mp3(request), 'form not valid')

	def test_filenameTooLong_file(self):
		filepathOfMp3 = '~/user_mp3_files/qweirouqwepiorqwpjfslfj asjkdfhsjkfhiwqehr quiwerh qwiuerh qwuier hqwuierh qwic vhmc hvmc hvcm hv qweruqiwerhqwouiehfskvnkjsadfbkjsadfhjsfhsjkdf wqierhwiuerhqwuierhw uifahsd fuahsdfiu sfhuiasd fhuiasdfhuiasd fhisahfisd fhuias dfhiasf iasdfaidfsadfhasd.mp3'
		request = self.assertEqual(self.upload_mp3(request), 'form not valid')

	def test_invalidChars_file(self):
		filepathOfMp3 = '~/user_mp3_files/@#ds!fd.mp3'
		#make a request with this file path
		request = self.assertEqual(self.upload_mp3(request), 'form not valid')
"""
