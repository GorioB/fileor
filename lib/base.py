#!/user/bin/env python
import re
def replaceSpecialChar(s):
	return re.sub(r'[<>:"/\|?*]',' ',s).strip(" ")

class File:
	def __init__(self,fileName=None,filePath=None,fileHash=None,fileContent=None,fileMetadata=None):
		self.fileName=fileName
		self.filePath=filePath
		self.fileHash=fileHash
		self.fileContent=fileContent
		if fileMetadata==None:
			self.fileMetadata={}

	def printContents(self):
		print "Filename: "+self.fileName
		print "Full Path: "+self.filePath
		print "MD5 Hash: "+self.fileHash