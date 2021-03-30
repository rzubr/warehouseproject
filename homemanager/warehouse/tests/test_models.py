from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from warehouse.models import Home, Category, Product


class TestHome(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_home = Home.objects.create(
            name = 'testhome'
        )
        self.test_home.client.add(self.test_user.client.pk)

    def test_absolute_url(self):
        self.assertEqual(self.test_home.get_absolute_url(), 
                        reverse('warehouse:home_detail', args=[self.test_home.pk]))


class TestProduct(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_home = Home.objects.create(
            name = 'testhome'
        )
        self.test_home.client.add(self.test_user.client.pk)
        self.test_category = Category.objects.create(
            name = 'test_category',
            home = self.test_home
        )
        self.test_product = Product.objects.create(
            name='test_product',
            category=self.test_category,
            new_quantity=40,
            unit='Kg'
        )

    def test_save_method(self):
        self.assertEqual(self.test_product.quantity, 40)
        self.assertEqual(self.test_product.max_quantity, 40)
        self.assertEqual(self.test_product.stock, "Full")

    def test_replenish_stock(self):
        self.test_product.new_quantity = 20
        self.test_product.save()
        self.assertNotEqual(self.test_product.max_quantity, self.test_product.quantity)
        self.test_product.new_quantity = 50
        self.test_product.save()
        self.assertEqual(self.test_product.max_quantity, self.test_product.quantity)

    def test_check_stock_state(self):
        self.test_product.new_quantity = 100
        self.test_product.save()
        self.assertEqual(self.test_product.stock, "Full")
        self.test_product.new_quantity = 45
        self.test_product.save()
        self.assertEqual(self.test_product.stock, "OK")
        self.test_product.new_quantity = 5
        self.test_product.save()
        self.assertEqual(self.test_product.stock, "Ends")
        self.test_product.new_quantity = 0.9
        self.test_product.save()
        self.assertEqual(self.test_product.stock, "empty")
