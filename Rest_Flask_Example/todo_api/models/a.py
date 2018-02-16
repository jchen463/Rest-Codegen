class A(object):
   def __init__(self):
     self.b = 1
     self.c = 2
   def do_nothing(self):
     pass

   def serialize(self):
       return {
           'b': self.c,
           'c': self.b
       }