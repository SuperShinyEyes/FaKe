#from django.test import TestCase

# Create your tests here.
import os

print __file__

print os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print os.path.dirname(os.path.abspath(__file__))
print os.path.abspath(__file__)
