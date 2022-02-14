import json
from typing import Dict, List, Any, Optional


def parse_modal_view(data: Dict, fields=List[str]) -> Dict:
    view_payload_path: tuple = ('view', 'state', 'values')

    def get_payload() -> Dict:
        payload: Optional[Dict] = None
        for field in view_payload_path:
            payload = data[field]

        return payload

    payload = get_payload()
    for block_id, action_info in payload.items():
        pass
    