import os
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from mtb_v5_app.models import Media, Page

class Command( BaseCommand ):
 help = 'Populate the Media table with data from the /media folder'

 def handle( self, *args, **kwargs ):
  media_root = os.path.join( os.getcwd( ), 'media' )
  phases = [ '01', '02', '03', '04', '05' ]

  self.stdout.write( self.style.SUCCESS( 'Starting to populate Media table' ) )

  # Ensure Page object with pk=0 exists
  try:
   page = Page.objects.get( pk = 0 )
  except ObjectDoesNotExist:
   page = Page.objects.create( pk = 0, name = 'home', phase = 0 )  # Adjust fields as necessary
   self.stdout.write( self.style.SUCCESS( 'Created default Page object with pk=0' ) )

  for phase in phases:
   phase_path = os.path.join( media_root, phase )
   if os.path.isdir( phase_path ):
    self.stdout.write( self.style.SUCCESS( f'Processing phase: {phase}' ) )
    for file_name in os.listdir( phase_path ):
     file_path = os.path.join( phase_path, file_name )
     if os.path.isfile( file_path ):
      title, ext = os.path.splitext( file_name )
      media_type = 'image' if ext.lower( ) == '.jpg' else 'video' if ext.lower( ) == '.mp4' else None
      if media_type:
       Media.objects.create( title = title, phase = phase, path = title,  # Only the filename without extension
        page = page, type = media_type )
       self.stdout.write( self.style.SUCCESS( f'Successfully added {title} to Media table' ) )
      else:
       self.stdout.write( self.style.WARNING( f'Skipped file with unsupported extension: {file_name}' ) )
   else:
    self.stdout.write( self.style.WARNING( f'Phase directory does not exist: {phase_path}' ) )

  self.stdout.write( self.style.SUCCESS( 'Finished populating Media table' ) )
