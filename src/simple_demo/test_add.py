import unittest
from tasks import add
from parameterized import parameterized


class TestTasks(unittest.TestCase):

    @parameterized.expand([
        (1, 2, 3),
        (0, 1, 1),
        (-3, 2, -1)
    ])
    def test_add(self, x, y, expected):
        self.assertEqual(add(x, y), expected)


if __name__ == '__main__':
    unittest.main()
