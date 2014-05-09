import os,shutil
import hashlib
import sys
sys.path.insert(0,"../../lib")
import base,config
system_root = os.path.abspath('.')

class DataStore:
	def __init__(self):
		os.chdir(config.root_path)
		try:
			os.mkdir(config.dest_path)
		except:
			print "Destination path already created"

		self.ignore = [config.dest_path]
		self.hashPath = os.path.join(config.root_path,config.dest_path,config.hash_record)


	def getRandomFile(self,directory):
		fullList = os.listdir(directory)
		fullList.pop(fullList.index(self.ignore[0]))
		fileList = filter(os.path.isfile,fullList)
		dirList = filter(os.path.isdir,fullList)
		if fileList!=[]:
			return os.path.abspath(fileList[0])
		elif dirList!=[]:
			return self.getRandomFile(directory+"/"+dirList[0])
		else:
			return 1

	def getMD5ofFile(self,f):
		md5 = hashlib.md5()
		while True:
			data = f.read(128)
			if not data:
				break
			md5.update(data)
		return md5.digest()

	def obtainFile(self,filePath=None):
		currfile=None
		if not (filePath):
			currfile = base.File(filePath=self.getRandomFile("."))
			if currfile.fileName == 1:
				currFile=None
		else:
			if os.path.isfile(filePath):
				currfile = base.File(filePath=filePath)

		if not currfile:
			return 0
		if currfile:
			currfile.fileName = os.path.split(currfile.filePath)[-1]
			with open(currfile.filePath,'r') as f:
				currfile.fileHash = self.getMD5ofFile(f)

		return currfile

	

	def createDirectoryTreeIfNotExists(self,dirPath):
		dPath = reduce(os.path.join,os.path.split(dirPath)[:-1])
		if not os.path.exists(dPath):
			os.makedirs(dPath)
		return 0

	def uploadFile(self,fileO,filePath):
		try:
			createDirectoryTreeIfNotExists(filePath)
			shutil.copy2(fileO.filePath,filePath)
			return 0
		except:
			return 1

	def moveFile(self,sourcePath,destPath):
		self.createDirectoryTreeIfNotExists(destPath)
		os.rename(sourcePath,destPath)
		return 0
		#try:
		#	shutil.move(sourcePath,destPath)
		#	return 0
		#except:
		#	return 1

	def downloadFile(sef,fileO):
		try:
			shutil.copy2(fileO.filePath,os.path.join(system_root,fileO.fileName))
			return 0
		except:
			return 1

	def createHashIfNotExists(self):
		self.createDirectoryTreeIfNotExists(self.hashPath)
		if not os.path.exists(self.hashPath):
			with open(self.hashPath,"w") as f:
				pass

	def checkHash(self,fileO):
		self.createHashIfNotExists()
		with open(self.hashPath,"r") as f:
			for line in f:
				if line.split(",")[1]==fileO.fileHash:
					return 1

		return 0

	def updateHash(self,fileO):
		self.createHashIfNotExists()
		with open(self.hashPath,"a") as f:
			f.write(fileO.fileName+","+fileO.fileHash)

		return 0

if __name__=="__main__":
	d = DataStore()
	p = d.obtainFile()
	p.printContents()
	print d.checkHash(p)
	if not d.checkHash(p):
		d.updateHash(p)
	d.moveFile(p.filePath,os.path.join(config.dest_path,"music",p.fileName))
