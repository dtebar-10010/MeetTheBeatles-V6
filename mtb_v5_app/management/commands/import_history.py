import os
import sqlite3
from django.core.management.base import BaseCommand
from mtb_v5_app.models import Page, History

class Command(BaseCommand):
	help = 'Import history data from old database file'
	
	def handle(self, *args, **options):
		old_db_path = 'db.sqlite3.new'  # Path to your old database
		
		if not os.path.exists(old_db_path):
			self.stdout.write(self.style.ERROR(f'Old database file not found: {old_db_path}'))
			return
		
		self.stdout.write(self.style.SUCCESS('Starting history data import from old database'))
		
		# Connect to the old database
		conn = sqlite3.connect(old_db_path)
		conn.row_factory = sqlite3.Row  # This allows accessing columns by name
		cursor = conn.cursor()
		
		# Get table names to verify the database structure
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = cursor.fetchall()
		table_names = [t['name'] for t in tables]
		self.stdout.write(f"Tables in old database: {', '.join(table_names)}")
		
		# Check if History table exists
		history_table_name = None
		for table in table_names:
			if 'history' in table.lower():
				history_table_name = table
				break
		
		if not history_table_name:
			self.stdout.write(self.style.ERROR('History table not found in the old database'))
			return
		
		self.stdout.write(f"Found history table: {history_table_name}")
		
		# Get column names in the history table
		cursor.execute(f"PRAGMA table_info({history_table_name});")
		columns = cursor.fetchall()
		column_names = [col['name'] for col in columns]
		self.stdout.write(f"Columns in history table: {', '.join(column_names)}")
		
		# Import History data
		try:
			cursor.execute(f"SELECT * FROM {history_table_name};")
			history_items = cursor.fetchall()
			self.stdout.write(f"Found {len(history_items)} history items to import")
			
			# Check if the related Page objects exist
			for history_data in history_items:
				page_id = history_data['page_id']
				
				# Check if the page exists, create it if needed
				if not Page.objects.filter(id=page_id).exists():
					self.stdout.write(f"Creating placeholder Page with ID {page_id}")
					# Create a placeholder page
					Page.objects.create(
					id=page_id,
					name=f"Placeholder Page {page_id}",
					phase="01"  # Default phase
					)
				
				# Create the history record
				history = History.objects.create(
				content=history_data['content'] if 'content' in history_data else '',
				phase=history_data['phase'] if 'phase' in history_data else '01',
				page_id=page_id
				)
				self.stdout.write(f"Imported history item: {history.id} for page {page_id}")
		
		except sqlite3.OperationalError as e:
			self.stdout.write(self.style.ERROR(f"Error importing history: {str(e)}"))
			# Get more details about the error
			self.stdout.write(f"The error occurred while trying to access table: {history_table_name}")
			self.stdout.write(f"Available columns: {', '.join(column_names)}")
			self.stdout.write(f"Model requires: id, content, phase, page_id")
		
		conn.close()
		self.stdout.write(self.style.SUCCESS('History data import completed!'))
