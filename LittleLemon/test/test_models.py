from django.test import TestCase
from restaurant.models import Menu

class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(ID = 2, Title ='Vanilla', price=50, Inventory=14)
        self.assertEqual(item, 'Vanilla:50')
