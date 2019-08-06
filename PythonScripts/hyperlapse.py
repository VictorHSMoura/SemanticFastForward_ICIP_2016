import matlab.engine
import os
from subprocess import Popen, PIPE, STDOUT

class InputError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return str(self.msg)

class SemanticHyperlapse(object):
    def __init__(self):
        self.video = None
        self.path = ''
        self.velocity = 0
        self.maxVel = 0
        self.alpha = []
        self.beta = []
        self.gama = []
        self.eta = []

    def getVideo(self):
        return self.video

    def setVideo(self, video):
        self.video = video

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, velocity):
        if self.isEmpty(velocity):
            raise InputError('Please insert speedup first')
        try:
            self.checkAndSetVelocity(velocity)
        except ValueError:
            raise InputError('Invalid speedup value')
            
    def getMaxVel(self):
        return self.maxVel

    def setMaxVel(self, maxVel):
        self.maxVel = maxVel

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, alpha):
        self.alpha = self.checkAndSetWeights(alpha)
        
    def getBeta(self):
        return self.beta

    def setBeta(self, beta):
        self.beta = self.checkAndSetWeights(beta)

    def getGama(self):
        return self.gama

    def setGama(self, gama):
        self.gama = self.checkAndSetWeights(gama)

    def getEta(self):
        return self.eta

    def setEta(self, eta):
        self.eta = self.checkAndSetWeights(eta)

    def setPaths(self):
        self.setPath(os.getcwd()) #get project path 
        self.video.setPaths()

    def checkAndSetVelocity(self, velocity):
        velocity = float(int(velocity))
        if velocity <= 1:
            raise InputError('Error: speedup <= 1')
        self.velocity = velocity
    
    def isEmpty(self, inputText):
        if inputText == '':
            return True
        return False

    def checkAndSetWeights(self, weights):
        try:
            return self.convertWeights(weights)
        except ValueError:
            raise InputError('Please fill correctly all weights inputs')

    def convertWeights(self, weights):
        for i in range(len(weights)):
            weights[i] = int(weights[i])	#if it isn't a number, it'll raises a ValueError
        return weights

    def opticalFlowCommand(self):
        videoFile = self.correctPath(self.video.getVideoFile())
        command = './optflow'
        videoParam = ' -v ' + videoFile
        configParam = ' -c default-config.xml'
        outputParam = ' -o ' + videoFile[:-4] + '.csv'

        fullCommand = command + videoParam + configParam + outputParam		
        
        return fullCommand

    def runOpticalFlow(self):
        os.chdir('../Vid2OpticalFlowCSV')

        os.system(self.opticalFlowCommand())
        
        os.chdir(self.getPath())


    def runMatlabSemanticInfo(self, eng):
        videoFile = self.video.getVideoFile()
        extractionFile = videoFile[:-4] + '_face_extracted.mat'

        eng.ExtractAndSave(videoFile, nargout=0)
        (aux, nonSemanticFrames, semanticFrames) = eng.GetSemanticRanges(extractionFile, nargout=3)

        return (float(nonSemanticFrames), float(semanticFrames))

    def getSemanticInfo(self, eng):
        eng.cd('SemanticScripts')
        eng.addpath(self.video.getVideoPath())
        eng.addpath(os.getcwd())
        
        nonSemanticFrames, semanticFrames = self.runMatlabSemanticInfo(eng)
        
        eng.cd(self.getPath())
        return (nonSemanticFrames, semanticFrames)

    def speedUp(self, eng, nonSemanticFrames, semanticFrames):
        eng.addpath(os.getcwd())
        eng.addpath('Util')
    
        alpha = matlab.double([self.getAlpha()])
        beta = matlab.double([self.getBeta()])
        gama = matlab.double([self.getGama()])
        eta = matlab.double([self.getEta()])
    
        (ss, sns) = eng.FindingBestSpeedups(nonSemanticFrames, semanticFrames,
                                            self.getVelocity(), True, nargout=2)
            
        eng.SpeedupVideo(self.video.getVideoPath(), self.video.getVideoName(), ss, sns, 
                        alpha, beta, gama, eta, 'Speedup', self.getVelocity(), nargout=0)

    def checkVideoInput(self):
        if self.getVideo().isEmpty():
            raise InputError('Please insert input video first')

        if self.getVideo().isInvalid():
            raise InputError('Video format invalid.\nValid formats: mp4, avi')

    def setup(self, inputSpeedUp, alphaInput, betaInput, gamaInput, etaInput):	
        self.checkVideoInput()

        self.setVelocity(inputSpeedUp)
        self.setMaxVel(self.getVelocity() * 10.0)

        self.setAlpha(alphaInput)
        self.setBeta(betaInput)
        self.setGama(gamaInput)
        self.setEta(etaInput)

    def run(self, writeFunction):
        function = writeFunction
        
        function('1/5 - Running Optical Flow\n', 'title')
        self.runOpticalFlow()
    
        function('2/5 - Starting Matlab\n', 'title')
        eng = matlab.engine.start_matlab('-nodisplay')
    
        function('3/5 - Getting Semantic Info\n', 'title')
        (nonSemanticFrames, semanticFrames) = self.getSemanticInfo(eng)

        function('4/5 - Speeding-Up Video\n', 'title')
        self.speedUp(eng, nonSemanticFrames, semanticFrames)
        eng.quit()
    
        function('5/5 - Finished\n', 'title')

    def correctPath(self, path):
        splittedPath = path.split(' ')
        finalPath = ''
        for i in splittedPath:
            finalPath += (i + '\ ')
        return finalPath[:-2]
