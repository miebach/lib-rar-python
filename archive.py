import os
import subprocess


def shellcall(cmd,silent=False):
  # do a system call with shell = true
  # taken from 
  # http://stackoverflow.com/questions/699325/suppress-output-in-python-calls-to-executables
  import os
  import subprocess

  # silent will suppress stdoud and stderr, good for testing!  
  if silent:
    fnull = open(os.devnull, 'w')
    # we need shell = true to keep the cwd 
    result = subprocess.call(cmd, shell = True, stdout = fnull, stderr = fnull)
    fnull.close()
    return result
  else:
    result = subprocess.call(cmd, shell = True)
    return result


class Archive(object):

  def __init__(self,archive_fullpath,sevenbin = "/usr/bin/7za"):
    self.archive_fullpath = archive_fullpath
    self.include_files = []
    self.include_dirs = []
    self.sevenbin = sevenbin
    
  def add_file(self,fullpath):
    self.include_files.append(fullpath)
    
  def add_dir(self,fullpath):
    self.include_dirs.append(fullpath)
    
  def extract(self,target_path,silent=True):
    import os
    os.chdir(target_path)
    cmd = self.sevenbin + " e " + self.archive_fullpath
    return shellcall(cmd,silent=silent)
    
  def run(self,silent=True):
    cmd = self.sevenbin + " a " + self.archive_fullpath 
    for p in self.include_files: 
      cmd = cmd +  " " + p
    for p in self.include_dirs: 
      cmd = cmd +  " " + p
    return shellcall(cmd,silent=silent)
    
    
"""

z7ip commands

Command 	Description
a 	Add - create a new archive, or add files to an existing archive
d 	Delete - remove files from an existing archive
e 	Extract - unarchive files
l 	List - display the contents of an archive
t 	Test - validate the integrity of an archive
u 	Update - overwrite existing files in an existing archive
x 	Extract - same as "e", except that the files are restored to their exact original 
    locations (if possible)
"""