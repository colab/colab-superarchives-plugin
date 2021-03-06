# -*- coding:utf-8 -*-

from django.test import TestCase,  Client
from django.core.management import call_command


class SuperarchivesSearchViewTest(TestCase):

    fixtures = ['test_data_superachives.json']

    def setUp(self):
        call_command('rebuild_index', interactive=False, verbosity=1)
        self.client = Client()

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=1)

    def test_search_thread(self):
        request = self.client.get('/search/?q=thread')
        thread_list = request.context['page'].object_list

        self.assertEqual(3,  len(thread_list))

        condition = any('This is a repply to Thread 1 on list A' in
                        t.description for t in thread_list)
        self.assertTrue(condition)
        condition = any('This is a repply to Thread 1 on list B' in
                        t.description for t in thread_list)
        self.assertTrue(condition)
        condition = any('This is a repply to Thread 1 on list C' in
                        t.description for t in thread_list)
        self.assertTrue(condition)

    def test_search_multiple_filters(self):
        request = self.client.get('/search/?q=&type=thread+user')
        user_list = request.context['page'].object_list
        user_list.sort(key=lambda i: i.name)

        self.assertEqual(6, len(user_list))

        self.assertIn('Admin Administrator',  user_list[0].author)
        self.assertIn('Response to Thread 1A',  user_list[0].title)

        self.assertIn('Admin Administrator',  user_list[1].author)
        self.assertIn('Message 1 on Thread 1B',  user_list[1].title)

        self.assertIn('Admin Administrator',  user_list[2].author)
        self.assertIn('Message 1 on Thread 1C',  user_list[2].title)
