import unittest
import os
import services.datehelper as dh
import datetime


class FunctionTest(unittest.TestCase):
    positive = [
        ["3_20190702082219.jpg", True, True],
        ["7_20190702082219.jpg", True, False],
        ["3_20190702082219.jpg", False, True],
        ["3_20190702082219.jpg", False, False],
        ["2_20700702082219.png", False, True] # большая дата
    ]
    expectedPositive = [
        [datetime.datetime(2019, 7, 2, 8, 22, 19), "08"],
        ["08"],
        [datetime.datetime(2019, 7, 2, 8, 22, 19)],
        Exception,
        [datetime.datetime(2070, 7, 2, 8, 22, 19)]
    ]

    negative = [  # expectedNegative = ValueError
        ["7_20190702082219", False],
        ["27_20190702082219.jpg", True, True],
        ["7_20190702082219.jp", True, True],
        ["7_20190702082219.g", True, False],
        ["7_20190702082219.g", True],
        ["7_0190702082219.g", False, True],
        ["7_201907020822191.jpg", True, True]
    ]


    def testGetDateOrHours(self):
        for i, item in enumerate(self.positive):
            self.assertEqual(dh.getDateOrHours(item[0], getHours=item[1], getDate=item[1]), self.expectedPositive[i])

       for i, item in enumerate(self.negative):
            self.assertRaises(ValueError, dh.getDateOrHours(item[0], getHours=item[1], getDate=item[1]), self.expectedPositive[i]))



if __name__ == '__main__':
    unittest.main()

