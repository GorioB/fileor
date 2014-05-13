import mutagen.easyid3,os
if __name__=="__main__":
	import sys
	sys.path.insert(0,"../lib")
	import base
else:
	import lib.base as base

class Filter:
	def __init__(self):
		self.extensions = ['mp3','flac']
		self.downloadsPath = os.path.join(os.getcwd(),'downloads')

	def commitChanges(self,dataStore,workingFile):
		self.cleanDownloads(workingFile)
		#print workingFile.filePath,os.path.join(dataStore.dst,"music","mp3")
		return dataStore.moveFile(workingFile.filePath,os.path.join(dataStore.dst,
			"music",
			"mp3",
			workingFile.fileMetadata['artist'][0],
			workingFile.fileMetadata['album'][0],
			workingFile.fileMetadata['title'][0]+".mp3"))


	def getFileAndDataStore(self,worker):
		workingFile = worker.currentFile
		worker.dataStore.downloadFile(workingFile)
		return workingFile,worker.dataStore

	def getMP3MetaData(self,fileO):
		data = mutagen.easyid3.Open(os.path.join(self.downloadsPath,fileO.fileName))
		fileO.fileMetadata.update(data)
	def cleanDownloads(self,fileO):
		os.remove(os.path.join(self.downloadsPath,fileO.fileName))
		return 0
	def filterMethod(self,worker):
		workingFile,dataStore = self.getFileAndDataStore(worker)
		extension = workingFile.fileName.split(".")[-1]
		if extension.lower() == 'mp3':
			self.getMP3MetaData(workingFile)
			if all (tag in workingFile.fileMetadata for tag in ('artist',
				'album',
				'title')):	
				return self.commitChanges(dataStore,workingFile)
			else:
				return 1

if __name__=="__main__":
	d = Filter()
	p = base.File()
	p.fileName = "eurydice.mp3"
	d.getMP3MetaData(p)
	print p.fileMetadata
