from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Page( models.Model ):
   name = models.CharField( max_length = 255 )
   phase = models.IntegerField( )

   class Meta:
      verbose_name_plural = "Page"

   def __str__( self ):
      return f"Page: {self.name} (Phase: {self.phase})"

class Media( models.Model ):
   title = models.CharField( max_length = 255 )
   phase = models.CharField(max_length = 2  )
   path = models.CharField( max_length = 255 )
   page = models.ForeignKey( Page, on_delete = models.CASCADE )
   type = models.CharField( max_length = 255, choices = [
      ('image', 'Poster'),
      ('video', 'Video'),
   ] )

   class Meta:
      verbose_name_plural = "Media"

   def __str__( self ):
      return f"Media: {self.title}"

   def poster_path( self ):
      if self.type == 'video':
         return self.path.replace( '.mp4', '.jpg' )
      return None

class History( models.Model ):
   content = CKEditor5Field( config_name = 'default' )
   
   phase = models.CharField(max_length = 2  )
   page = models.ForeignKey( Page, on_delete = models.CASCADE )

   class Meta:
      verbose_name_plural = "History"

   def __str__( self ):
      return f"History: (Page {self.page.name})"
