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
    self.pwd = None
    # compression level: 0: store, 1: fastest, 2: fast, 3: normal, 4: good, 5: best
    self.compression_level = 3
    # Percentage of recovery record
    self.recovery_record = None
    # Volume size if necessary <size>[k|b|f|m|M|g|G] More info in rar.txt
    self.volume_size = None
    self.exclude_base_dir = False

    self.include_files = []
    self.include_dirs = []
    self.exclude_patterns = []
  
  def exclude(self,pattern):
    self.exclude_patterns.append(pattern)
    
  def add_file(self,fullpath):
    self.include_files.append(fullpath)
    
  def add_dir(self,fullpath):
    self.include_dirs.append(fullpath)
    
  def set_password(self, pwd):
	self.pwd = pwd
	
  def set_compression_level(self, compression_level):
	self.compression_level = compression_level

  def set_exclude_base_dir(self, exclude_base_dir):
    self.exclude_base_dir = exclude_base_dir
  
  def set_recovery_record(self, rr_percent):
    self.recovery_record = rr_percent
  
  def set_volume_size(self, volume_size):
    self.volume_size = volume_size
	
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

    # rar add 
    cmd = self.rarbin + " a" 
    
    # exclude certain locations
    for p in self.exclude_patterns: 
      cmd = cmd +  " -x" + p

    # the archive path and name
    cmd = cmd + " " + self.archive_fullpath 

    # directories to include
    for p in self.include_dirs: 
      cmd = cmd +  " " + p

    # files to include
    for p in self.include_files: 
      cmd = cmd +  " " + p
	  
    # include password if necessary
    if self.pwd:
      cmd = cmd + " -p" + str(self.pwd)
	  
    # compression level
    cmd = cmd + " -m" + str(self.compression_level)
	
    # split to volumes based on volume size
    if self.volume_size:
      cmd = cmd + " -v" + str(self.volume_size)
	  
    # add recovery record if necessary
    if self.recovery_record:
      cmd = cmd + " -rr" + str(self.recovery_record)

    if self.exclude_base_dir:
      cmd = cmd + " -ep1"

    res = shellcall(cmd,silent=silent)
    return res
