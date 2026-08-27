# This Makefile contains helper commands for the Moody Manuals Project

extractcompanynames:
	uv run src/company_name_extraction.py

syncdataup:
	rsync -r ./data "${REMOTE_DATA_CONN_STRING}"

syncdatadown:	
	rsync -r "${REMOTE_DATA_CONN_STRING}" ./data
