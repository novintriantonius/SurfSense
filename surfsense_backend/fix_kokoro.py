import re

with open('pyproject.toml', 'r') as f:
    content = f.read()

# Make kokoro an optional dependency or remove the exact version constraint if it's breaking python 3.14 build
content = re.sub(r'\s*"kokoro>=0\.9\.4",\n', '\n', content)

with open('pyproject.toml', 'w') as f:
    f.write(content)
print("Removed kokoro requirement temporarily to run tests")
