import sublime, sublime_plugin
import os, time

#TODO: Hide [Finished in 0.0s] text box
#TODO: Work with different configurations per folder
#TODO: React to compilation faliure

class SimpleSass(sublime_plugin.EventListener):
	sourceExtensions = []
	filesToCompile = []
	compilerPath = ""
	outputExtension = ""
	outputDirectory = ""

	# Reload settings
	def reload_settings(self):
		print "reload"
		settings = sublime.load_settings("SimpleSass.sublime-settings")

		self.sourceExtensions = settings.get('sourceExtensions')
		self.compilerPath = settings.get('compilerPath')
		self.filesToCompile = settings.get('filesToCompile')
		self.outputExtension = settings.get('outputExtension')
		self.outputDirectory = settings.get('outputDirectory')

	# Compile the file at sourceFullPath
	def compile_file(self, sourceFullPath, view):
		sourceName = os.path.basename(sourceFullPath)
		sourceFolder = os.path.dirname(sourceFullPath)
		sourceNameWithoutExtension = os.path.splitext(sourceName)[0]
		outputPath = self.outputDirectory + sourceNameWithoutExtension + self.outputExtension

		view.window().run_command('exec', {
			'cmd': [self.compilerPath, sourceName, outputPath],
			'working_dir': sourceFolder
		})


	# Returns the root directory path in Sublime Text for a given full path
	# Receives the array of folder paths that Sublime Text has open
	def getRootPath(self, sourceFullPath, folders):
		print sourceFullPath
		for dirPath in folders:
			if dirPath in sourceFullPath:
				return dirPath

		return ""


	# React to a file being saved -> Run compilation tasks if allowed
	def on_post_save(self, view):
		print 'SimpleSass: on_post_save ' + time.ctime()

		self.reload_settings()
		sourceFullPath = view.file_name()

		#print self.outputDirectory
		sourceExt = (os.path.splitext(sourceFullPath))[1]
		if sourceExt in self.sourceExtensions:
			sourceName = os.path.basename(sourceFullPath)
			if sourceName[0] != '_':
				self.compile_file(sourceFullPath, view)
			else:
				#print "SimpleSass: File has a monitored extension but is private."
				rootPath = self.getRootPath(sourceFullPath, view.window().folders())
				for path in self.filesToCompile:
					self.compile_file(rootPath + "\\" + path, view)
		else:
			print "SimpleSass: Not monitored."