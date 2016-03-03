import os
from django.test import TestCase
from django.template import TemplateDoesNotExist
from django.core.management import call_command
from storeys.management.commands.collect_storeyjs_routes import StoreysUrlsNotFound


class UrlsParseSuccess(TestCase):

    def test_urls_parse_success(self):
        call_command('collect_storeyjs_routes', *['test'], **{})
        self.assertTrue(os.path.isfile('./test/static/urls.js'))
        self.assertTrue(os.path.isfile('./test/static/additional_app/urls.js'))

        with open('./test/static/additional_app/urls.js') as f:
            file_content = f.read()
        self.assertEqual(file_content.count("url("), 6)
        self.assertEqual(file_content.count(
            "url("), file_content.count("test_success"))

        # Temporary stub
        with open('./test/static/urls.js') as f:
            file_content = f.read()
        self.assertEqual(file_content.count("url("), 6)
        self.assertEqual(file_content.count("test_success"), 3)

        # Test case for 'non_exported_urlpatterns'
        # with open('./test/static/urls.js') as f:
        #     file_content = f.read()
        # self.assertEqual(file_content.count("url("), 3)
        # self.assertEqual(file_content.count("url("), file_content.count("test_success"))


class UrlsParseErrors(TestCase):

    def test_urls_parse_template_not_exist(self):
        template_not_exists_flag = False

        # Replase template path with broken path
        file_path = './test/main_app/urls.py'
        content = file_read(file_path)
        file_write(file_path, content.replace('storeys_urls_js/main.html',
                                              'notexist/main.html'))

        with self.assertRaises(TemplateDoesNotExist) as e:
            call_command('collect_storeyjs_routes', *['test'], **{})

        file_write(file_path, content)

    def test_urls_parse_entries_not_found(self):
        template_not_exists_flag = False

        # Replase all needed functions with uninteresting for script functions
        file_path = './test/additional_app/urls.py'
        content = file_read(file_path)
        empty_content = content.replace('TemplateView.as_view','empty_view')\
            .replace('StoreysView.as_view', 'empty_view.as_view')\
            .replace('include(', 'empty_include(')

        file_write(file_path, empty_content)

        with self.assertRaises(StoreysUrlsNotFound) as e:
            call_command('collect_storeyjs_routes', *['test'], **{})

        file_write(file_path, content)


def file_read(path):
    f = open(path, 'r')
    file_content = f.read()
    return file_content


def file_write(path, content):
    f = open(path, 'w')
    f.seek(0)
    f.truncate()
    f.write(content)
