# -*- coding: utf-8 -*-
import stores.local_store.local_store as dataStore
import os
import filters.music_filter.music_filter as music_filter

class Worker:
	def __init__(self):
		self.filters = []
		self.filters.append(music_filter.Filter())
		self.dataStore = dataStore.DataStore()
		self.currentFile = self.dataStore.obtainFile()

	def start(self):
		if(self.currentFile):
			extension = self.currentFile.fileName.split(".")[-1]
			if self.dataStore.checkHash(self.currentFile):
				self.dataStore.moveFile(self.currentFile.filePath,os.path.join(self.dataStore.dst,
					"dup",
					self.currentFile.fileName))
			else:
				self.dataStore.updateHash(self.currentFile)

				for f in self.filters:
					if extension in f.extensions:
						f.filterMethod(self)
						break

				if extension not in [item for sublist in [foo.extensions for foo in self.filters] for item in sublist]:
					self.dataStore.moveFile(self.currentFile.filePath,os.path.join(self.dataStore.dst,
						"misc",
						self.currentFile.fileName))

			self.currentFile = self.dataStore.obtainFile()
			return 0
		else:
			return 1

if __name__ == "__main__":
	worker = Worker()
	#worker.start()
	while not (worker.start()):
		pass
