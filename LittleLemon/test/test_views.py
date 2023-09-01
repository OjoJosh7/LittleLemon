from django.test import TestCase
from restaurant import views
from restaurant.models import Menu


class MenuItemViewTest(TestCase):

    def setUp(self):
        Menu.objects.create(ID = 4, Title ='Vnilla', price=50, Inventory=14)
        
    def test_getall(self):
        self.item = Menu.objects.create(Title='Vanilla')
        response = views.MenuItemView.as_view()
        
        #self.assertEqual(response.status_code, 200)
        self.assertIn(self.item, response)
