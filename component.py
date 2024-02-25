import requests
from uuid import UUID, uuid4
from datetime import datetime
import unittest


user_url = 'http://localhost:8000'
get_users_url = f'{user_url}/get_users'
add_user_url = f'{user_url}/add_user'
get_user_by_id_url = f'{user_url}/get_user_by_id/'
delete_user_url = f'{user_url}/delete_user'

roulette_url = 'http://localhost:8001'


user = {
    "id": "8dcae814-7f01-407b-b85f-2bb12093d881",
    "name": "Nikita",
    "second_name": "Paramonov",
    "dick_size": "-7"
}


class TestComponent(unittest.TestCase):

    def test_1_get_users(self):
        res = requests.get(f"{get_users_url}")
        self.assertTrue(res != None)

    def test_2_add_user(self):
        res = requests.post(f"{add_user_url}", json=user)
        self.assertEqual(res.status_code, 200)

    def test_3_get_user_by_id(self):
        res = requests.get(f"{get_user_by_id_url}?user_id={user['id']}").json()
        self.assertTrue(res, user)

    def test_4_delete_user(self):
        res = requests.delete(f"{delete_user_url}?user_id={user['id']}").json()
        self.assertEqual(res, "Success")

if __name__ == '__main__':
    unittest.main()