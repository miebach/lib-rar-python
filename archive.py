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

  def __init__(self,archive_fullpath,base_path,rarbin = "/usr/bin/rar"):
    self.archive_fullpath = archive_fullpath
    self.base_path = base_path
    self.rarbin = rarbin

    self.include_files = []
    self.include_dirs = []
    
    
  def add_file(self,fullpath):
    self.include_files.append(fullpath)
    
  def add_dir(self,fullpath):
    self.include_dirs.append(fullpath)
    
  def extract(self,target_path,silent=True):
    import os
    os.chdir(target_path)
    # e = extract to current dir, x = extract using full path
    # -r = recurse subdirectories
    # (-r could be introduced, because single added files otherwise are extrated 
    #  to the wrong place. But this should bex fixed on archiving, nit unarchiving!)
    cmd = self.rarbin + " x " + self.archive_fullpath
    return shellcall(cmd,silent=silent)
    
  def run(self,silent=True):
    # -ep1 remove base directory from paths (store only relative directory)

    import os
    os.chdir(self.base_path)

    res = 0

    if len(self.include_dirs) > 0:   
      cmd = self.rarbin + " a " + self.archive_fullpath 
      for p in self.include_dirs: 
        cmd = cmd +  " " + p
      res = shellcall(cmd,silent=silent)
      if res != 0:
        return res

    if len(self.include_files) > 0:
      cmd = self.rarbin + " a " + self.archive_fullpath 
      for p in self.include_files: 
        cmd = cmd +  " " + p
      res = shellcall(cmd,silent=silent)
    
    return res
