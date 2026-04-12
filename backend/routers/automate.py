from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/power-automate", tags=["automate"])

import datetime

@router.post("/run")
async def run_automate_flow():
    """
    Simplest possible Power Automate run endpoint.
    No database, no complex logic.
    """
    now = datetime.datetime.now().strftime("%I:%M:%S %p")
    print(f"Power Automate flow executed at {now}")
    return {
        "success": True,
        "message": "Power Automate flow executed successfully",
        "executed_at": now
    }
