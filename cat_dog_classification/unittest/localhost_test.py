import os
import unittest

from utils import TargetURL, make_request

class TestAPIService_LOCALHOST_PREV(unittest.TestCase):
    
    def test_cat_1(self):
        img_path = os.path.join('unittest', 'imgs', 'input', 'cat1.jpg')
        resp = make_request(TargetURL.LOCALHOST, img_path)
        data = resp.json()

        self.assertEqual(data['pet_type'], 'CAT')
        self.assertEqual(data['status'], "Success")

    def test_cat_2(self):
        img_path = os.path.join('unittest', 'imgs', 'input', 'cat2.jpg')
        resp = make_request(TargetURL.LOCALHOST, img_path)
        data = resp.json()

        self.assertEqual(data['pet_type'], 'CAT')
        self.assertEqual(data['status'], "Success")

    def test_dog_1(self):
        img_path = os.path.join('unittest', 'imgs', 'input', 'dog1.jpg')
        resp = make_request(TargetURL.LOCALHOST, img_path)
        data = resp.json()

        self.assertEqual(data['pet_type'], 'DOG')
        self.assertEqual(data['status'], "Success")

    def test_dog_2(self):
        img_path = os.path.join('unittest', 'imgs', 'input', 'dog2.jpg')
        resp = make_request(TargetURL.LOCALHOST, img_path)
        data = resp.json()

        self.assertEqual(data['pet_type'], 'DOG')
        self.assertEqual(data['status'], "Success")


if __name__ == '__main__':
    unittest.main()
