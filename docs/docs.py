__author__ = 'mark'
# docs.py
#
# Created by Mark Scrimshire on 2011-11-09.
# Copyright (c) 2011 HealthCa.mp. All rights reserved.

# Used to keep notes about the project

# Re-structure Account/UserProfile
# UserProfile is extension of User model
# Member Profile is optional but linked to User.

# Create stub Profile for each User entry

# working on /accounts/profile = accounts.account_settings
# Error loading a profile
# line 255 views.py:
# __init__() got an unexpected keyword argument 'user'

# form = AccountSettingsForm(user=request.user)
# need to populate account information using current user


# pulling data from User and merging in to form.

# next step is to address creating the Organization/Registry List
# Allow User to register Organization in Pending state
# Use Admin interface to set Organization to Approved or Removed.

# Need to get RegistryForm
# Validate information
# Set Linked Owner to User

# Set UserProfile Security Level to 2 (if level 1)


# Create a form instance with POST data.
# f = AuthorForm(request.POST)

# Create, but don't save the new author instance.
# new_author = f.save(commit=False)
# Modify the author in some way.
# new_author.some_field = 'some_value'

# Save the new instance.
# new_author.save()
# Now, save the many-to-many data for the form.
# f.save_m2m()



