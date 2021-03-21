# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from warehouse.views import (HomeView, HomeDetailsView, DeleteProductView, 
#     DeleteCategoryView, UpdateProductView, UpdateCategoryView, CreateHomeView,
#     UpdateHomeView, DeleteHomeView, remove_from_home)

# class TestUrls(SimpleTestCase):

#     #home urls tests
#     def test_home_url(self):
#         url = reverse('warehouse:home')
#         self.assertEquals(resolve(url).func.view_class, HomeView)

#     def test_create_home_url(self):
#         url = reverse('warehouse:create_home')
#         self.assertEquals(resolve(url).func.view_class, CreateHomeView)

#     def test_update_home_url(self):
#         url = reverse('warehouse:update_home', args=['1'])
#         self.assertEquals(resolve(url).func.view_class, UpdateHomeView)

#     def test_delete_home_url(self):
#         url = reverse('warehouse:delete_home', args=['1'])
#         self.assertEquals(resolve(url).func.view_class, DeleteHomeView)

#     def test_leave_home_url(self):
#         url = reverse('warehouse:leave_home', args=['2','3'])
#         self.assertEquals(resolve(url).func, remove_from_home)

#     #category urls test
#     def test_delete_category_url(self):
#         url = reverse('warehouse:delete_category', args=['1'])
#         self.assertEquals(resolve(url).func.view_class, DeleteCategoryView)

#     def test_update_category_url(self):
#         url = reverse('warehouse:update_category', args=['1'])
#         self.assertEquals(resolve(url).func.view_class, UpdateCategoryView)

#     #product url tests
#     def test_delete_product_url(self):
#         url = reverse('warehouse:delete_product', args=['1'])
#         self.assertEquals(resolve(url).func.view_class, DeleteProductView)

#     def test_update_product_url(self):
#         url = reverse('warehouse:update_product', args=['1'])
#         self.assertEquals(resolve(url).func.view_class, UpdateProductView)