import uuid
from datetime import datetime, timezone
def create_request(action_type, requester, payload):
    return {"approval_id":str(uuid.uuid4()),"action_type":action_type,"requester":requester,"payload":payload,"state":"pending_approval","created_at":datetime.now(timezone.utc).isoformat()}
