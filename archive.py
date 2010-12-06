import os
import subprocess



class Archive(object):

  def __init__(self,archive_fullpath,sevenbin = "/usr/bin/7za"):
    self.archive_fullpath = archive_fullpath
    self.include_files = []
    self.sevenbin = sevenbin
    
  def add_file(self,fullpath):
    self.include_files.append(fullpath)
    
  def extract(self,target_path):
    import os
    os.chdir(target_path)
    cmd = self.sevenbin + " e " + self.archive_fullpath
    #print cmd
    return os.system(cmd)
    
  def run(self):
    import os
    cmd = self.sevenbin + " a " + self.archive_fullpath + " " + self.include_files[0]
    print cmd
    return os.system(cmd)
    
  