from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from warehouse.models import Home, Product, Category
from warehouse.forms import CategoryForm, HomeForm, ProductForm

        
class TestHomeView(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='password')
        self.home_url = reverse('warehouse:home')
        Home.objects.create(name='test_home')
        Home.objects.create(name='test_home2')
        home = Home.objects.get(name='test_home')
        home2 = Home.objects.get(name='test_home2')
        home.client.add(test_user.client)

    def test_not_logged_user_redirect(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 302)

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.get(self.home_url)
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        #Check if logged user get his home
        self.assertEqual(str(response.context['object_list'][0]), 'test_home')
        #Check if logged user doesnt get not his home in response
        home2 = Home.objects.get(name='test_home2')
        self.assertFalse(home2 in response.context['object_list'])
        #Check template
        self.assertTemplateUsed(response, 'warehouse/home.html')
    

class TestCreateHomeView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.create_url = reverse('warehouse:create_home')

    def test_not_logged_user_redirect(self):
        client = Client()
        response = client.get(self.create_url)
        self.assertEquals(response.status_code, 302)

    def test_logged_user_post(self):
        login = self.client.login(username='testuser', password='password')
        #Ceck if get not allowed check
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 405)
        #Check if create view redirect after post request
        post_response = self.client.post(self.create_url, {
            'name': 'Home',
            'client': self.test_user.client
        })
        self.assertEqual(post_response.status_code, 302)
        #Check if home is created correctly
        home = Home.objects.get(name='Home')
        self.assertTrue(self.test_user.client in home.client.all())


class TestUpdateHomeView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_home = Home.objects.create(
            name= 'home_to_update',
        )
        self.test_home.client.add(self.test_user.client)
        self.update_url = reverse('warehouse:update_home', args=[self.test_home.pk])

    def test_update_request(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(self.update_url, {
            'name': 'updated_home',
        })
        #Check redirect after post request
        self.test_home.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        #Check if name is changed
        self.assertTrue(self.test_home.name == 'updated_home')
        #Check if client has not been changed
        self.assertTrue(self.test_user.client in self.test_home.client.all())


class TestRemoveFromHome(TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_home = Home.objects.create(name='test_home')
        self.test_home.client.add(self.test_user.client.pk)
        self.remove_url = reverse('warehouse:leave_home', args=[self.test_home.pk, 
                                                                self.test_user.client.pk])
        self.test_user2 = User.objects.create_user(username='testuser2', password='password')
        self.test_home2 = Home.objects.create(name='test_home2')
        self.test_home2.client.add(self.test_user2.client.pk)

    def test_not_logged_user_redirect(self):
        client = Client()
        response = client.get(self.remove_url)
        self.test_home.refresh_from_db()
        self.assertEqual(response.status_code, 302)

    def test_leave_home_request(self):
        #Check if client can leave his home
        login = self.client.login(username='testuser', password='password')
        self.assertTrue(self.test_user.client in self.test_home.client.all())
        response = self.client.get(reverse('warehouse:leave_home', kwargs={
            'pk': self.test_home.pk,
            'userpk': self.test_user.pk
        }))
        self.assertFalse(self.test_user.client in self.test_home.client.all())
        #check if other client isnt able to remove someone else from his home
        self.assertTrue(self.test_user2.client in self.test_home2.client.all())
        response_2 = self.client.get(reverse('warehouse:leave_home', kwargs={
            'pk': self.test_home2.pk,
            'userpk': self.test_user.pk
        }))
        self.assertTrue(self.test_user2.client in self.test_home2.client.all())
        #Check situation when in one home there are two users and one of them
        #try to kick through this view second user.
        self.test_home.client.add(self.test_user.client, self.test_user2.client)
        response_3 = self.client.get(reverse('warehouse:leave_home', kwargs={
            'pk':self.test_home.pk,
            'userpk':self.test_user2.pk
        }))
        self.assertTrue(self.test_user2.client in self.test_home.client.all() and 
                        self.test_user2.client in self.test_home.client.all())


class TestDeleteHomeView(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_home = Home.objects.create(name='test_home')
        self.test_home.client.add(self.test_user.client.pk)

    def test_not_logged_user_redirect(self):
        response = self.client.get(reverse('warehouse:delete_home', args=[self.test_home.pk]))
        self.assertEqual(response.status_code, 302)

    def test_owner_user_GET(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('warehouse:delete_home', args=[self.test_home.pk]))
        self.assertEqual(response.status_code, 200)

    def test_owner_user_POST(self):
        login = self.client.login(username='testuser', password='password')
        self.assertEqual(Home.objects.all().count(), 1)
        response = self.client.post(reverse('warehouse:delete_home', args=[self.test_home.pk]))
        self.assertEqual(Home.objects.all().count(), 0)

    def test_home_delete_from_non_owner_user(self):
        test_user2 = User.objects.create_user(username='testuser2', password='password')
        test_home2 = Home.objects.create(name='test_home2')
        test_home2.client.add(test_user2.client.pk)
        login = self.client.login(username='testuser', password='password')
        self.assertEqual(Home.objects.all().count(), 2)
        response = self.client.post(reverse('warehouse:delete_home', args=[test_home2.pk]))
        self.assertEqual(Home.objects.all().count(), 2)


class BaseHomeCategoryProductTest(TestCase):
    # Basic setup involve 2 instances of users, homes, categories and products 
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_home = Home.objects.create(name='test_home')
        self.test_home.client.add(self.test_user.client.pk)
        self.test_category_a = Category.objects.create(
            name = 'test_category_a',
            home = self.test_home
        )
        self.test_product_a = Product.objects.create(
            name='test_product',
            category = self.test_category_a,
            new_quantity = 30,
            unit = 'kg'
        )
        self.test_user_2 = User.objects.create_user(username='testuser_2', password='password')
        self.test_home_2 = Home.objects.create(name='test_home_2')
        self.test_home_2.client.add(self.test_user_2.client.pk)
        self.test_category_b = Category.objects.create(
            name = 'test_category_b',
            home = self.test_home_2
        )
        self.test_product_b = Product.objects.create(
            name='test_product_b',
            category = self.test_category_b,
            new_quantity = 50,
            unit = 'kg'
        )
        return super().setUp()


class TestHomeDetailsView(BaseHomeCategoryProductTest):
    def test_not_logged_user_redirect(self):
        response = self.client.get(reverse('warehouse:home_detail', args=[self.test_home.pk]))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_GET(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('warehouse:home_detail', args=[self.test_home.pk]))
        self.assertEqual(response.status_code, 200)
        #check context
        self.assertEqual(str(response.context['home']), 'test_home')
        self.assertTrue(self.test_category_a in response.context['categories'])
        self.assertFalse(self.test_category_b in response.context['categories'])
        category_form = CategoryForm
        self.assertIn('category_form', response.context)
        self.assertIn('product_form', response.context)

    def test_logged_user_valid_POST(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('warehouse:home_detail', args=[self.test_home.pk]),{
            'category_add':'Add category',
            'name': 'posted_category',
            'home': self.test_home.pk
        })
        self.test_home.refresh_from_db()
        self.assertEqual(self.test_home.category_set.all().count(), 2)
        posted_category = Category.objects.get(name='posted_category',home=self.test_home)
        response = self.client.post(reverse('warehouse:home_detail', args=[self.test_home.pk]),{
            'product_add':'Add product',
            'name': 'posted_product',
            'category': posted_category.pk,
            'new_quantity': 20,
            'unit': 'KG'
        })
        posted_category.refresh_from_db()
        self.assertTrue(Product.objects.filter(name='posted_product', 
                        category=posted_category).exists())

    def test_logged_user_not_valid_POST(self):
        login = self.client.login(username='testuser', password='password')
        #test user posting category to not his home
        response = self.client.post(reverse('warehouse:home_detail', args=[self.test_home.pk]),{
            'category_add':'Add category',
            'name': 'posted_category',
            'home': self.test_home_2.pk
        })
        self.test_home_2.refresh_from_db
        self.assertEqual(Category.objects.filter(name='posted_category').count(), 0)
        #Test user posting product to category not in his home
        response = self.client.post(reverse('warehouse:home_detail', args=[self.test_home.pk]),{
            'product_add':'Add product',
            'name': 'posted_product',
            'category': self.test_category_b.pk,
            'new_quantity': 20,
            'unit': 'KG'
            })
        self.test_home_2.refresh_from_db()
        self.assertEqual(Product.objects.filter(name='posted_product').count(), 0)


class TestUpdateProduct(BaseHomeCategoryProductTest):
    def test_not_logged_user_redirect(self):
        response = self.client.get(reverse('warehouse:update_product', args=[self.test_product_a.pk]))
        #response = self.client.get(reverse('warehouse:update_product', args=[self.test_product_a.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRegex(str(response.url), r'accounts/login')

    def test_logged_user_POST(self):
        #valid post
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('warehouse:update_product', 
                    args=[self.test_product_a.pk]),{
                    'name':'new_product_name',
                    'category':self.test_category_a.pk,
                    'new_quantity':50,
                    'unit':"kg"
                    })
        self.test_product_a.refresh_from_db()
        self.assertTrue(self.test_product_a.name == 'new_product_name')
        #Not valid post
        response = self.client.post(reverse('warehouse:update_product', 
                    args=[self.test_product_b.pk]),{
                    'name':'new_product_b_name',
                    'category':self.test_category_a.pk,
                    'new_quantity':50,
                    'unit':"kg"
                    })
        self.assertFalse(self.test_product_b.name == 'new_product_b_name')


class TestUpdateCategory(BaseHomeCategoryProductTest):
    def test_not_logged_user_redirect(self):
        response = self.client.get(reverse('warehouse:update_category', args=[self.test_category_a.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRegex(str(response.url), r'accounts/login')

    def test_logged_user_POST(self):
        #valid post
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('warehouse:update_category', 
                    args=[self.test_category_a.pk]),{
                    'name':'new_category_name',
                    'home': self.test_home.pk,
                    })
        self.test_category_a.refresh_from_db()
        self.assertTrue(self.test_category_a.name == 'new_category_name')
        #Not valid post
        response = self.client.post(reverse('warehouse:update_category', 
                    args=[self.test_category_b.pk]),{
                    'name':'new_category_b_name',
                    'home': self.test_home.pk,
                    })
        self.assertFalse(self.test_category_b.name == 'new_category_b_name')


class TestDeleteProduct(BaseHomeCategoryProductTest):
    def test_not_logged_user_redirect(self):
        response = self.client.get(reverse('warehouse:delete_product', args=[self.test_product_a.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRegex(str(response.url), r'accounts/login')

    def test_delete_request_from_owner(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('warehouse:delete_product', args=[self.test_product_a.pk]))
        self.assertFalse(Product.objects.filter(name='test_product').exists())

    def test_dlete_request_from_not_owner(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('warehouse:delete_product', args=[self.test_product_b.pk]))
        self.assertTrue(Product.objects.filter(name='test_product_b').exists())


class TestDeleteCategory(BaseHomeCategoryProductTest):
    def test_not_logged_user_redirect(self):
        response = self.client.get(reverse('warehouse:delete_category', args=[self.test_category_a.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRegex(str(response.url), r'accounts/login')

    def test_delete_request_from_owner(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('warehouse:delete_category', args=[self.test_category_a.pk]))
        self.assertFalse(Category.objects.filter(name='test_category_a').exists())

    def test_dlete_request_from_not_owner(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('warehouse:delete_category', args=[self.test_category_b.pk]))
        self.assertTrue(Category.objects.filter(name='test_category_b').exists())
