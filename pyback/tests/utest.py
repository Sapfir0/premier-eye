import unittest
#import sys, os
# sys.path.append("../neural_network")
# import maskCNN
from neural_network.modules.decart import DecartCoordinates as decart
import datetime
import helpers.dateHelper as dh


class FunctionTest(unittest.TestCase):
    objectsInFrame = [  # прогоняем все эти объекты для каждой ареи
        [299, 658, 539, 1173],
        [422, 0, 714, 331],
        [68, 1032, 131, 1111]
    ]
    highlightedArea = [
        [20, 20, 800, 1200],
        [0, 0, 0, 0],
        [0, 0, 600, 1000],
        [0, 0, 800, 1200]
    ]
    expected_output = [
        [False, True, True],
        [False, False, False],
        [False, False, False],  # полностью не входит ни один
        [True, True, True]
    ]

    def testConcetration(self):
        start_date = dh.parseFilename("3_20190702082436.jpg")
        finish_date = dh.parseFilename("3_20190702085716.jpg")
        for area in range(0, len(self.highlightedArea)):
            res = decart.getConcetration(self.highlightedArea[area], start_date, finish_date)
            # self.assertEqual(res, self.expected_output[area][obj]) #не
            # продуманы выходные

    def testCompletelyInside(self):
        for area in range(0, len(self.highlightedArea)):
            for obj in range(0, len(self.objectsInFrame)):
                res = decart.isCompletelyInside(self.highlightedArea[area], self.objectsInFrame[obj])
                self.assertEqual(res, self.expected_output[area][obj])

    def testPartiallyInside(self):
        for area in range(0, len(self.highlightedArea)):
            for obj in range(0, len(self.objectsInFrame)):
                res = decart.isPartiallyInside(self.highlightedArea[area], self.objectsInFrame[obj])
                self.assertEqual(res, self.expected_output[area][obj])


if __name__ == '__main__':
    unittest.main()
