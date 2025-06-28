import redis
import pickle
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6380, db=0)

# Test the connection
if r.ping():
    print("Connected to Redis!")

# Get all keys
keys = r.keys('*')
print("Keys in Redis:")
for key in keys:
    print(f"Key: {key}")

    try:
        # Try to decode the value as UTF-8 text anish
        value = r.get(key)
        try:
            # Try parsing as JSON
            decoded = json.loads(value)
            print(f"Value (JSON): {json.dumps(decoded, indent=2)}")
        except (json.JSONDecodeError, TypeError):
            try:
                # Try unpickling (Celery stores pickled results)
                decoded = pickle.loads(value)
                print(f"Value (Pickled): {decoded}")
            except Exception:
                print(f"Value (Raw Bytes): {value}")
    except Exception as e:
        print(f"Error retrieving key {key}: {e}")
