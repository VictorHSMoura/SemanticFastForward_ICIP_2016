import unittest
from hyperlapse import SemanticHyperlapse, InputError
from video import Video
import os

class TestHyperlapse(unittest.TestCase):
    def setUp(self):
        video = Video()
        video.setVideoFile('/home/victorhugomoura/Documents/example.mp4')
        self.hyperlapse = SemanticHyperlapse()
        self.hyperlapse.setVideo(video)
        self.hyperlapse.setPaths()

    def testVideo(self):
        self.assertIsInstance(self.hyperlapse.getVideo(), Video)

    def testPath(self):
        self.assertEqual(self.hyperlapse.getPath(), os.getcwd())
        self.hyperlapse.setPath('/')
        self.assertEqual(self.hyperlapse.getPath(), '/')

    def testVelocity(self):
        self.assertRaises(InputError, self.hyperlapse.setVelocity, '')
        self.assertRaises(InputError, self.hyperlapse.setVelocity, 'A')
        self.assertRaises(InputError, self.hyperlapse.setVelocity, '1')
        self.hyperlapse.setVelocity('10')
        self.assertEqual(self.hyperlapse.getVelocity(), 10)

    def testMaxVel(self):
        self.hyperlapse.setMaxVel(100.0)
        self.assertEqual(self.hyperlapse.getMaxVel(), 100)

    def testCheckWeights(self):
        self.assertRaises(ValueError, self.hyperlapse.convertWeights, ['', ''])
        self.assertRaises(ValueError, self.hyperlapse.convertWeights, ['a', '10'])
        self.assertRaises(InputError, self.hyperlapse.checkAndSetWeights, ['', ''])
        self.assertListEqual(self.hyperlapse.checkAndSetWeights(['10', '10']), [10, 10])

    def testWeights(self):
        self.hyperlapse.setAlpha(['50', '50'])
        self.hyperlapse.setBeta(['20', '20'])
        self.hyperlapse.setGama(['30', '30'])
        self.hyperlapse.setEta(['40', '50'])

        self.assertListEqual(self.hyperlapse.getAlpha(), [50, 50])
        self.assertListEqual(self.hyperlapse.getBeta(), [20, 20])
        self.assertListEqual(self.hyperlapse.getGama(), [30, 30])
        self.assertListEqual(self.hyperlapse.getEta(), [40, 50])

    def testOpticalFlowCommand(self):
        command = self.hyperlapse.opticalFlowCommand()
        expectedCommand = './optflow -v /home/victorhugomoura/Documents/example.mp4 ' + \
            '-c default-config.xml -o /home/victorhugomoura/Documents/example.csv'

        self.assertEqual(command, expectedCommand)

    def testCheckVideoInput(self):
        self.hyperlapse.getVideo().setVideoFile('')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)

        self.hyperlapse.getVideo().setVideoFile('/home/victorhugomoura/Documents/example.csv')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)

    def testSetup(self):
        alpha = ['1', '2']
        beta = ['4', '3']
        gama = ['5', '6']
        eta = ['8', '7']
        speed = '10'

        # check if it don't raise an exception
        self.hyperlapse.setup(speed, alpha, beta, gama, eta)

        speed = '1'
        self.assertRaises(InputError, self.hyperlapse.setup, speed, alpha, beta, gama, eta)

    def testInputError(self):
        self.hyperlapse.getVideo().setVideoFile('')
        
        try:
            self.hyperlapse.checkVideoInput()
        except InputError as IE:
            self.assertEqual(IE.__str__(), 'Please insert input video first')

class TestVideo(unittest.TestCase):
    def setUp(self):
        self.video = Video()
        self.video.setVideoFile('/home/victorhugomoura/Documents/example.mp4')
        self.video.setPaths()

    def testFile(self):
        self.assertEqual(self.video.getVideoFile(), '/home/victorhugomoura/Documents/example.mp4')
        self.video.setVideoFile('/home/victorhugomoura/Documents/example2.mp4')
        self.assertNotEqual(self.video.getVideoFile(), '/home/victorhugomoura/Documents/example.mp4')
        self.assertEqual(self.video.getVideoFile(), '/home/victorhugomoura/Documents/example2.mp4')

    def testName(self):
        self.assertEqual(self.video.getVideoName(), 'example.mp4')
        self.video.setVideoFile('/home/victorhugomoura/Documents/example2.mp4')
        self.video.setPaths()
        self.assertEqual(self.video.getVideoName(), 'example2.mp4')

    def testPath(self):
        self.assertEqual(self.video.getVideoPath(), '/home/victorhugomoura/Documents')
        self.video.setVideoFile('/home/victorhugomoura/Downloads/example.mp4')
        self.video.setPaths()
        self.assertEqual(self.video.getVideoPath(), '/home/victorhugomoura/Downloads')

    def testEmpty(self):
        self.assertFalse(self.video.isEmpty())
        self.video.setVideoFile('')
        self.assertTrue(self.video.isEmpty())

    def testInvalid(self):
        self.assertFalse(self.video.isInvalid())
        self.video.setVideoFile('/home/victorhugomoura/Documents/example.csv')
        self.assertTrue(self.video.isInvalid())

if __name__ == '__main__':
    unittest.main()