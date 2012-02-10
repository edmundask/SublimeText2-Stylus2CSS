import sublime, sublime_plugin, subprocess, os, threading

class Stylus2CSS(sublime_plugin.EventListener):
   def on_post_save(self, view):

      if not view.scope_name(0).strip().startswith('source.stylus'):
         return

      thread = StylusApiThread(view.file_name())
      thread.start()

class StylusApiThread(threading.Thread):
   def __init__(self, input_file):
      self.input = input_file
      self.result = ''
      self.filename = os.path.basename(self.input)
      self.filename = os.path.splitext(self.filename)[0]
      threading.Thread.__init__(self)
   
   def run(self):

      if os.name == "nt":
         startupinfo = subprocess.STARTUPINFO()
         startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

      process = subprocess.Popen(('curl','-F', 'style=@' + self.input, 'http://styl.herokuapp.com'),
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo)

      stdout = process.communicate()
      self.result = stdout[0]

      f = open(os.path.dirname(self.input) + '/'+ self.filename +'.css', 'w')
      f.write(self.result)
      f.close()

      print 'Compiled ' + self.input + ' to '+ self.filename + '.css'



