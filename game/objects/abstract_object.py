from abc import abstractclassmethod


class GameObject:
   @abstractclassmethod
   def move(self):
      pass

   @abstractclassmethod
   def draw(self):
      pass

