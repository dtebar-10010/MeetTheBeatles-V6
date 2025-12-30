import os
import sqlite3
import json
import re
from django.core.management.base import BaseCommand

class Command( BaseCommand ):
	help = 'Extract history data directly from SQLite database and clean content'
	
	def add_arguments( self, parser ):
		parser.add_argument( 'db_file', type = str, help = 'Path to the SQLite database file' )
		parser.add_argument( 'output_file', type = str, help = 'Path to the output JSON file' )
	
	def handle( self, *args, **options ):
		db_file = options[ 'db_file' ]
		output_file = options[ 'output_file' ]
		
		if not os.path.exists( db_file ):
			self.stdout.write( self.style.ERROR( f'Database file not found: {db_file}' ) )
			return
		
		self.stdout.write( self.style.SUCCESS( f'Connecting to database: {db_file}' ) )
		
		try:
			# Connect to the database
			conn = sqlite3.connect( db_file )
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor( )
			
			# Get table names
			cursor.execute( "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';" )
			tables = cursor.fetchall( )
			table_names = [ table[ 'name' ] for table in tables ]
			
			self.stdout.write( f'Tables in database: {", ".join( table_names )}' )
			
			# Find the history table
			history_table = None
			for table in table_names:
				if 'history' in table.lower( ):
					history_table = table
					break
			
			if not history_table:
				self.stdout.write( self.style.ERROR( 'No history table found in the database' ) )
				return
			
			self.stdout.write( f'Found history table: {history_table}' )
			
			# Get history table structure
			cursor.execute( f"PRAGMA table_info({history_table});" )
			columns = cursor.fetchall( )
			column_names = [ column[ 'name' ] for column in columns ]
			self.stdout.write( f'Columns in history table: {", ".join( column_names )}' )
			
			# Fetch history data
			cursor.execute( f"SELECT * FROM {history_table};" )
			history_rows = cursor.fetchall( )
			
			if not history_rows:
				self.stdout.write( self.style.WARNING( 'No history records found in the table' ) )
				return
			
			self.stdout.write( f'Found {len( history_rows )} history records' )
			
			# Convert to list of dictionaries and clean content
			history_data = [ ]
			for row in history_rows:
				row_dict = { column: row[ column ] for column in row.keys( ) }
				
				# Clean content field if it exists
				if 'content' in row_dict and row_dict[ 'content' ]:
					# Replace escaped characters with a single space
					content = row_dict[ 'content' ]
					# Replace \r\n sequences with a space
					content = re.sub( r'\\r\\n', ' ', content )
					# Replace other common escape sequences
					content = re.sub( r'\\[nt]', ' ', content )
					# Replace multiple spaces with a single space
					content = re.sub( r'\s+', ' ', content )
					row_dict[ 'content' ] = content
				
				history_data.append( row_dict )
			
			# Write to output file
			with open( output_file, 'w' ) as f:
				json.dump( history_data, f, indent = 2 )
			
			self.stdout.write( self.style.SUCCESS( f'Cleaned history data saved to: {output_file}' ) )
			
			# Create a separate preview file with full content for ALL records
			preview_file = f"{os.path.splitext( output_file )[ 0 ]}_preview.txt"
			with open( preview_file, 'w' ) as f:
				for i, record in enumerate( history_data ):  # Include all records
					f.write( f"=== Record {i + 1} ===\n" )
					for key, value in record.items( ):
						f.write( f"{key}: {value}\n" )
					f.write( "\n\n" )
			
			self.stdout.write( self.style.SUCCESS( f'Full preview of ALL {len( history_data )} records saved to: {preview_file}' ) )
			
			# Close connection
			conn.close( )
		
		except Exception as e:
			self.stdout.write( self.style.ERROR( f'Error: {str( e )}' ) )
