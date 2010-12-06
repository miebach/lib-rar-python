#!/usr/bin/python
import os
import unittest2 as unittest

import file_helper, archive 

opj = os.path.join

class TestArchive(unittest.TestCase):

  def testMakeArchive(self):
    # Part A creates a single file, archives it, then deletes it
    # Part B extracts the file again from the archive and checks the content
    
    # Part A:
    file_helper.create_file(opj(self.tempdir,"testfile"),"content123test")
    
    a = archive.Archive(opj(self.tempdir,"testarchive1.7zip"))
    a.add_file(opj(self.tempdir,"testfile"))

    self.assertEqual(a.run(),0) 
    self.assertEqual(file_helper.file_exists(opj(self.tempdir,"testarchive1.7zip")),True)

    file_helper.remove_file(opj(self.tempdir,"testfile"))
    self.assertEqual(file_helper.file_exists(opj(self.tempdir,"testfile")),False)
       
    # Part B:
    b = archive.Archive(opj(self.tempdir,"testarchive1.7zip"))
    syscode = b.extract(target_path=self.tempdir)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_head(opj(self.tempdir,"testfile")),"content123test")
    
  def testMakeArchiveSubdirs(self):
    # create an archive at not YET existing directory
    # (7zip will create the directory if it can!)
    aname = opj(self.tempdir,"dir/will/be/created","testarchive1.7zip")
    a = archive.Archive(aname)
    file_helper.create_file(opj(self.tempdir,"testfile")) # empty file is ok
    a.add_file(opj(self.tempdir,"testfile"))
    syscode = a.run() 
    self.assertEqual(syscode,0)
    zipfileexists = file_helper.file_exists(aname)
    self.assertEqual(zipfileexists,True)
    
  def testMakeArchiveCannotWrite(self):
    # create an archive at a directory without permissions (or impossible to write)
    # (7zip will create the directory if it can!)
    aname = opj("/dev/null/testarchive1.7zip")
    a = archive.Archive(aname)
    file_helper.create_file(opj(self.tempdir,"testfile")) # empty file is ok
    a.add_file(opj(self.tempdir,"testfile"))
    syscode = a.run() 
    self.assertNotEqual(syscode,0)
        
  def testMakeArchiveFail1(self):
    # create an archive of not existing file
    a = archive.Archive(opj(self.tempdir,"testarchive1.7zip"))
    a.add_file(opj(self.tempdir,"this-file-does-not-exist"))
    syscode = a.run() 
    self.assertNotEqual(syscode,0)
        
    
  def setUp(self):
    #get a temp dir:
    self.tempdir = file_helper.get_random_temp_dir_name()
    #create the temp dir:
    file_helper.create_dir(self.tempdir)

    
  
  def tearDown(self):
    file_helper.destroy_dir_recursive(self.tempdir)
  
     
    

if __name__ == "__main__":
    unittest.main()