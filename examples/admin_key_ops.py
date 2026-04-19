import os
from removebgvideo import RemoveBGVideoAdminClient

admin = RemoveBGVideoAdminClient(admin_token=os.environ["REMOVEBGVIDEO_ADMIN_TOKEN"])

created = admin.create_key(client_id="acme-prod", note="Production integration")
print("New key:", created["api_key"])
print("Fingerprint:", created["key_fingerprint"])

summary = admin.list_keys()
print("Key count:", len(summary.get("items", [])))
