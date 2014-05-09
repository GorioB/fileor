#!/user/bin/env python
class File:
	def __init__(fileName=None,filePath=None,fileHash=None,fileContent=None,fileMetadata=None):
		self.fileName=fileName
		self.filePath=filePath
		self.fileHash=fileHash
		self.fileContent=fileContent
		self.fileMetadata=fileMetadata
