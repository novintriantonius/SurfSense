import ast
import sys

def check_syntax(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source, filename=file_path)
        print(f"Syntax OK: {file_path}")
        return True
    except SyntaxError as e:
        print(f"Syntax Error in {file_path}:")
        print(f"  Line {e.lineno}, Col {e.offset}: {e.text}")
        print(f"  {e.msg}")
        return False
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

check_syntax("surfsense_backend/app/tasks/connector_indexers/local_folder_indexer.py")
