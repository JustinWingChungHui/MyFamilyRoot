from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestMapViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()


        user = User.objects.create_user(email='adam_lambert@queenonline.com', password='sexy boy', name='Adam Lambert', family_id=self.family.id)
        user.save()

        person1 = Person(name='Adam Lambert', gender='M', user_id = user.id, email='adam_lambert@queenonline.com', family_id=self.family.id, latitude = 39.768, longitude = -86.158, address = 'Indianapolis, Indiana')
        person1.save()

        person2 = Person(name='Paul Rodgers', gender='M', family_id=self.family.id, latitude = 54.574, longitude = -1.235, address = 'Middlesborough, UK')
        person2.save()



    def test_map_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(email='adam_lambert@queenonline.com', password='sexy boy')
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/family_map.html')

        self.assertTrue(b'Paul Rodgers' in response.content)

        self.assertTrue(b'x.push(54.574)' in response.content)
        self.assertTrue(b'y.push(-1.235)' in response.content)

        self.assertTrue(b'Adam Lambert' in response.content)
        self.assertTrue(b'x.push(39.768)' in response.content)
        self.assertTrue(b'y.push(-86.158)' in response.content)

        self.assertTrue(b'center: new google.maps.LatLng(39.768,-86.158)' in response.content)