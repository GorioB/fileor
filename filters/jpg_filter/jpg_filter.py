if __name__=="__main__":
	import sys
	sys.path.insert(0,"../../lib")
	import base
else:
	import lib.base as base

import exifread,os

class Filter:
	def __init__(self):
		self.extensions = ['jpg','jpeg']
		self.downloadsPath = os.path.join(os.getcwd(),'downloads')

	def downloadFile(self,worker):
		worker.dataStore.downloadFile(worker.currentFile)
		return worker.currentFile

	def cleanDownloads(self,fileO):
		os.remove(os.path.join(self.downloadsPath,fileO.fileName))
		return 0

	def getExifData(self,fileO):
		f = open(os.path.join(self.downloadsPath,fileO.fileName),"rb")
		tags = exifread.process_file(f)
		print "[+] jpg_filter: Extracted EXIF data from image."
		return tags

	def commitChanges(self,dataStore,fileO,folderStruct):

		self.cleanDownloads(fileO)
		joinList = [dataStore.dst,"photos"]+folderStruct
		joinList.append(fileO.fileName)
		print "[+] jpg_filter: Committing changes."
		return dataStore.moveFile(fileO.filePath,
			reduce(os.path.join,joinList))

	def extractYearMonth(self,s):
		return s.split(" ")[0].split(":")[0],s.split(" ")[0].split(":")[1]

	def filterMethod(self,worker):
		workingFile = self.downloadFile(worker)
		imageTags = self.getExifData(workingFile)
		if 'EXIF DateTimeOriginal' in imageTags.keys():
			print "[+] jpg_filter: Year and Month extracted."
			year,month = self.extractYearMonth(imageTags['EXIF DateTimeOriginal'].values)
			return self.commitChanges(worker.dataStore,workingFile,[year,month])
		else:
			print "[-] jpg_filter: No date information found."
			return self.commitChanges(worker.dataStore,workingFile,["unsorted"])

if __name__=="__main__":
	d = Filter()
	f = base.File()
	f.fileName = "testimg.jpg"
	print d.getExifData(f)['EXIF DateTimeOriginal']