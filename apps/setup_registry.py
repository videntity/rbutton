#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Mark Scrimshire on 2011-11-09.
Copyright (c) 2011 HealthCa.mp. All rights reserved.
"""

import unittest


class untitled(unittest.TestCase):
	def setUp(self):
		pass

    
if __name__ == '__main__':
	unittest.main()       
	
	
	
	
#	System Outline
#       
#   Add Organization
#       Must be logged in (ie. have a user account)
#  Search for Organization Record      
# Create Organization record
# Edit Organization
# Remove Organization (By Owner)
#                   
# Admin: Approve 
# Admin: Remove

# apps.registry(Status : 'done', Folder : 'apps/registry')        
# apps.registry(Status : 'done', File : '__init__.py') 
# apps.registry(Status : 'done', File : 'admin.py')
# apps.registry(File : 'auth.py')
# apps.registry(Status : 'done', File : 'models.py')                                                        
# apps.registry(Status : 'done', File : 'forms.py') 
# apps.registry(Status : 'done', File : 'views.py')
# apps.registry(Status : 'done', File : 'urls.py')

# apps.registry( Feature : 'Organization' , Model : 'Organization', View : {'List', 'Search', 'Edit', 'Delete'})
# apps.registry( Model : 'Organization', View : {'AdminList', 'AdminEdit', 'AdminApprove', 'AdminDelete'})

# template.registry( File: 'registry/registry_view.html')
# template.registry( File: 'registry/registry_settings.html')