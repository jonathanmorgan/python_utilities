#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Setup" data-toc-modified-id="Setup-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Setup</a></span></li><li><span><a href="#Create-a-bag" data-toc-modified-id="Create-a-bag-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Create a bag</a></span></li><li><span><a href="#Work-with-an-existing-bagit-bag" data-toc-modified-id="Work-with-an-existing-bagit-bag-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Work with an existing bagit bag</a></span><ul class="toc-item"><li><span><a href="#Load-existing-bag" data-toc-modified-id="Load-existing-bag-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Load existing bag</a></span></li><li><span><a href="#Update-bag-manifests" data-toc-modified-id="Update-bag-manifests-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Update bag manifests</a></span></li><li><span><a href="#Verify-existing-bag" data-toc-modified-id="Verify-existing-bag-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>Verify existing bag</a></span></li></ul></li></ul></div>

# # Setup
# 
# - Back to [Table of Contents](#Table-of-Contents)

# In[ ]:


import bagit
import datetime
import logging


# In[ ]:


# config

# folder paths
#work_folder = "/Volumes/Samsung_T5/projects/phd/proquest_hnp"
work_folder = "<folder_path>"
bag_folder = "{}/<folder_with_data_files>".format( work_folder )
process_count = 4
checksum_list = [ "sha256" ]
bagit_parameters = {}
bagit_parameters[ "Contact-Name" ] = "<name>"
bagit_parameters[ "Contact-Email" ] = "<email>"


# In[ ]:


cd $bag_folder


# In[ ]:


ls


# In[ ]:


# logging config
log_file_name = "{}/bagit-log.txt".format( work_folder )
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filename = log_file_name,
    filemode = "w" # set to "a" if you want to append each time
)


# # Create a bag
# 
# - Back to [Table of Contents](#Table-of-Contents)
# 
# In the `bag_folder`, will create a folder named "data", move all data into that folder exactly as it originally was within the `bag_folder`, including sub-folders, then create bagit manifest files alongside the "data" folder that can subsequently be used to walk the data folder and checksum each file within.
# 
# *NOTE: if you are on a Mac, you might need to go into the file `tagmanifest-sha256` and remove the line for "`.DS_store`".  This macos system file changes over time, and so will cause your bag to be invalid over time.*

# In[ ]:


get_ipython().run_line_magic('cd', '$bag_folder')


# In[ ]:


get_ipython().run_line_magic('pwd', '')


# In[ ]:


print( "bagit make_bag() started at {}".format( datetime.datetime.now() ) )
bag = bagit.make_bag( bag_folder, bag_info = bagit_parameters, processes = process_count, checksums = checksum_list )
print( "bagit make_bag() completed at {}".format( datetime.datetime.now() ) )


# # Work with an existing bagit bag
# 
# - Back to [Table of Contents](#Table-of-Contents)

# ## Load existing bag
# 
# - Back to [Table of Contents](#Table-of-Contents)

# In[ ]:


# load bag from folder:
bag = bagit.Bag( bag_folder )


# ## Update bag manifests
# 
# - Back to [Table of Contents](#Table-of-Contents)

# In[ ]:


# make changes
import shutil, os

# add a file
shutil.copyfile( "newfile", "{}/data/newfile".format( bag_folder ) )

# remove a file
os.remove( "{}/data/deleteme".format( bag_folder ) )


# In[ ]:


# load bag from folder:
#bag = bagit.Bag( bag_folder )

# persist changes
print( "bagit save() started at {}".format( datetime.datetime.now() ) )
bag.save( manifests = True, processes = 4 )
print( "bagit save() completed at {}".format( datetime.datetime.now() ) )


# ## Verify existing bag
# 
# - Back to [Table of Contents](#Table-of-Contents)

# In[ ]:


# load bag from folder:
#bag = bagit.Bag( bag_folder )

print( "bagit is_valid() started at {}".format( datetime.datetime.now() ) )
is_bag_valid = bag.is_valid()
print( "bagit is_valid() completed at {}".format( datetime.datetime.now() ) )

if ( is_bag_valid == True ):
    print( "yay :)" )
else:
    print( "boo :(" )
#-- END check to see if valid --#

