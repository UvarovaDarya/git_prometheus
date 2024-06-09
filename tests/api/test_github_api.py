import unittest
import json
from typing import List

import pytest
import re
import requests
from modules.api.clients.github import GitHub


@pytest.mark.api
def test_user_exists(github_api):
    api = GitHub()
    user = github_api.get_user('defunkt')
    assert user['login'] == 'defunkt'


@pytest.mark.api
def test_user_not_exists(github_api):
    api = GitHub()
    r = github_api.get_user('dariauvarova')
    assert r['message'] == 'Not Found'


@pytest.mark.api
def test_repo_exists(github_api):
    r = github_api.search_repo('become-qa-auto')
    assert r['total_count'] == 58
    assert 'become-qa-auto' in r['items'][0]['name']


@pytest.mark.api
def test_repo_cannot_be_found(github_api):
    r = github_api.search_repo('dariauvarova_repo_not_exist')
    assert r['total_count'] == 0


@pytest.mark.api
def test_repo_with_single_char_be_found(github_api):
    r = github_api.search_repo('s')
    assert r['total_count'] != 0


@pytest.mark.api
class GitHubEmojisTestCases(unittest.TestCase):
    github_emojis = GitHub.get_emojis()

    def test_get_emojis_returns_200_OK(self):
        self.assertEqual(self.github_emojis.status_code, 200, "Status should be 200 OK")

    def test_emojis_response_body_is_not_empty(self):
        response_body = self.github_emojis.json()
        self.assertIsNotNone(response_body)
        self.assertIsInstance(response_body, dict)

    def test_response_body_contains_valid_urls_only(self):
        body = self.github_emojis.json()
        url_pattern = re.compile(
            r'^(https?|ftp)://'  # http:// or https:// or ftp://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.))'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for url in body.values():
            self.assertIsNotNone(re.match(url_pattern, url), "Values in response should be a valid URL")


@pytest.mark.api
class GitHubTemplatesTestCases(unittest.TestCase):
    github_templates = GitHub.get_all_templates()

    def test_get_all_templates_returns_200_OK(self):
        self.assertEqual(self.github_templates.status_code, 200, "Status should be 200 OK")

    def test_get_all_templates_returns_string_list(self):
        response_body = self.github_templates.json()
        self.assertIsInstance(response_body, list)

    def test_get_template_by_name_returns_200_ok_and_valid_body(self):
        template_by_name = GitHub.get_template_by_name("C++")
        self.assertEqual(200, template_by_name.status_code, "Returned status should be 200 OK")
        response_body = template_by_name.json()
        self.assertIsNotNone(response_body, "Response body shouldn't be empty")

    def test_get_template_by_unknown_name_returns_404_not_found(self):
        template_by_name = GitHub.get_template_by_name("C--")
        self.assertEqual(404, template_by_name.status_code, "Returned status should be 404 Not Found")
        response_body = template_by_name.json()

        self.assertIsNotNone(response_body, "Body should contain error details")
        self.assertEqual(response_body['message'], "Not Found")
        self.assertEqual(response_body['status'], "404")
