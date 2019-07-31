import os

class Video(object):
	def __init__(self):
		self.videofile = ""
		self.videopath = ""
		self.videoname = ""

	def getVideoFile(self):
		return self.videofile
	
	def setVideoFile(self, videofile):
		self.videofile = videofile

	def getVideoPath(self):
		return self.videopath

	def setVideoPath(self, videopath):
		self.videopath = videopath

	def getVideoName(self):
		return self.videoname

	def setVideoName(self, videoname):
		self.videoname = videoname

	def setPaths(self):
		self.setVideoPath(os.path.dirname(os.path.abspath(self.getVideoFile())))
		self.setVideoName(self.getVideoFile()[len(self.getVideoPath())+1:])
