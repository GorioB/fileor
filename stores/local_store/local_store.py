import os,shutil
import hashlib
import sys
import pickle
if __name__=="__main__":
	sys.path.insert(0,"../../lib")
	import base
else:
	import lib.base as base
import config
def listdir_fullpath(d):
	return [os.path.join(d,f) for f in os.listdir(d)]

class DataStore:
	def __init__(self):
		self.downloadsFolder = os.path.join(os.getcwd(),'downloads')
		self.root = config.root_path
		self.dst = os.path.join(self.root,config.dest_path)
		self.hashPath = os.path.join(self.dst,config.hash_record)
		try:
			os.mkdir(self.dst)
			print "[+] local_store: Created dest folder."
		except:
			print "[*] local_store: Dest path already present."
		try:
			os.mkdir(self.downloadsFolder)
			print "[+] local_store: Created Downloads folder."
		except:
			print "[*] local_store: Downloads folder already present."

	def getRandomFile(self,directory):
		fullList = listdir_fullpath(directory)
		if fullList == [self.dst]:
			print "[-] local_store: Source directory is empty."
			return None
		if self.dst in fullList:
			fullList.pop(fullList.index(self.dst))
		fileList = filter(os.path.isfile,fullList)
		dirList = filter(os.path.isdir,fullList)
		if fileList!=[]:
			return os.path.abspath(fileList[0])
		elif dirList!=[]:
			print "[*] local_store: No files. Checking next directory"
			return self.getRandomFile(dirList[0])
		else:
			print "[-] local_store: This directory is empty. Removing directory and repeating on outer directory."
			os.rmdir(directory)
			return self.getRandomFile(os.path.split(directory)[0])

	def getMD5ofFile(self,f):
		md5 = hashlib.md5()
		while True:
			data = f.read(128)
			if not data:
				break
			md5.update(data)
		return md5.digest()

	def obtainFile(self,filePath=None):
		if not (filePath):
			randomFilePath = self.getRandomFile(self.root)
			if randomFilePath:
				currentFile = base.File(filePath=randomFilePath)
			else:
				return None
		else:
			if os.path.isfile(filePath):
				currentFile = base.File(filePath=filePath)
			else:
				print "[-] local_store: There does not to seem to be a file with that address."
				return None

		currentFile.fileName = os.path.split(currentFile.filePath)[-1]
		with open(currentFile.filePath,'r') as f:
			currentFile.fileHash = self.getMD5ofFile(f)
		print "[+] local_store: Obtained "+currentFile.fileName+"."
		return currentFile

	def createDirectoryTreeIfNotExists(self,dirPath):
		dPath = os.path.dirname(dirPath)
		if not os.path.exists(dPath):
			print "[*] local_store: Directory "+dPath+" created."
			os.makedirs(dPath)
		return 0

	def uploadFile(self,fileO,filePath):
		try:
			createDirectoryTreeIfNotExists(filePath)
			shutil.copy2(fileO.filePath,filePath)
			print "[+] local_store: File "+fileO.fileName+" uploaded to "+filePath+"."
			return 0
		except:
			return 1
	def clearSameFileName(self,path):
		while os.path.exists(path):
			directory,name = os.path.split(path)
			path = os.path.join(directory,"New_"+name)

		return path
	def moveFile(self,sourcePath,destPath):
		self.createDirectoryTreeIfNotExists(destPath)
		destPath = self.clearSameFileName(destPath)
		os.rename(sourcePath,destPath)
		print "[+] local_store: File moved."
		if os.listdir(os.path.dirname(sourcePath))==[]:
			print "[*] local_store: Source directory empty after move. Deleted."
			os.rmdir(os.path.dirname(sourcePath))
		return 0
 
	def downloadFile(self,fileO):
		shutil.copy2(fileO.filePath,os.path.join(self.downloadsFolder,fileO.fileName))
		print "[+] local_store: Downloaded File "+fileO.filePath+" to "+self.downloadsFolder+"."
		return 0
		

	def createHashIfNotExists(self):
		self.createDirectoryTreeIfNotExists(self.hashPath)
		if not os.path.exists(self.hashPath):
			with open(self.hashPath,"w") as f:
				hashes = {}
				pickle.dump(hashes,f)

	def checkHash(self,fileO):
		self.createHashIfNotExists()
		with open(self.hashPath,"r") as f:
			hashes = pickle.load(f)
			for key,value in hashes.items():
				if fileO.fileHash == value:
					print "[-] local_store: Hash matches for "+fileO.fileName+":"+fileO.fileHash+" and "+key+":"+value+"."
					return 1
		return 0

	def updateHash(self,fileO):
		self.createHashIfNotExists()
		with open(self.hashPath,"r") as f:
			hashes = pickle.load(f)

		hashes.update({fileO.fileName:fileO.fileHash})
		with open(self.hashPath,"w") as f:
			pickle.dump(hashes,f)

		return 0

if __name__=="__main__":
	d = DataStore()
	d.downloadFile(d.obtainFile())
