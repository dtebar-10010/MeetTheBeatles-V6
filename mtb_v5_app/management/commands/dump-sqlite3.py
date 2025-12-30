import os
import sqlite3
import json
from django.core.management.base import BaseCommand

class Command( BaseCommand ):
	help = 'Dump SQLite database contents to a JSON file'
	
	def add_arguments( self, parser ):
		parser.add_argument( 'db_file', type = str, help = 'Path to the SQLite database file' )
		parser.add_argument( 'output_file', type = str, help = 'Path to the output JSON file' )
	
	def handle( self, *args, **options ):
		db_file = options[ 'db_file' ]
		output_file = options[ 'output_file' ]
		
		if not os.path.exists( db_file ):
			self.stdout.write( self.style.ERROR( f'Database file not found: {db_file}' ) )
			return
		
		self.stdout.write( self.style.SUCCESS( f'Dumping database: {db_file}' ) )
		
		# Connect to the database
		conn = sqlite3.connect( db_file )
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor( )
		
		# Get table names
		cursor.execute( "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';" )
		tables = cursor.fetchall( )
		table_names = [ table[ 'name' ] for table in tables ]
		
		# Initialize result dictionary
		result = { }
		
		# Iterate through tables
		for table_name in table_names:
			self.stdout.write( f'Processing table: {table_name}' )
			
			# Get column names
			cursor.execute( f"PRAGMA table_info({table_name});" )
			columns_info = cursor.fetchall( )
			column_names = [ column[ 'name' ] for column in columns_info ]
			
			# Get table data
			cursor.execute( f"SELECT * FROM {table_name};" )
			rows = cursor.fetchall( )
			
			# Format as list of dictionaries
			table_data = [ ]
			for row in rows:
				row_dict = { column: row[ column ] for column in row.keys( ) }
				table_data.append( row_dict )
			
			# Add to result
			result[ table_name ] = {
			'columns': column_names,
			'data'   : table_data
			}
		
		# Write to file
		with open( output_file, 'w' ) as f:
			json.dump( result, f, indent = 2 )
		
		self.stdout.write( self.style.SUCCESS( f'Database dump completed: {output_file}' ) )
