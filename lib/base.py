#!/user/bin/env python
class File:
	def __init__(self,fileName=None,filePath=None,fileHash=None,fileContent=None,fileMetadata=None):
		self.fileName=fileName
		self.filePath=filePath
		self.fileHash=fileHash
		self.fileContent=fileContent
		self.fileMetadata=fileMetadata

	def printContents(self):
		print "Filename: "+self.fileName
		print "Full Path: "+self.filePath
		print "MD5 Hash: "+self.fileHash