import sys
sys.path.insert(0, '.')

# Test that the server module can be imported without errors
from flask_server import app

print("Flask server with error handlers loaded successfully!")

# List all routes
print("\nRegistered routes:")
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"  {methods:8} {rule.rule}")
