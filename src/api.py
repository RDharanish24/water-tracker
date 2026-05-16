from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history
from datetime import datetime

app = FastAPI(title="Hydration Tracker API")
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int

@app.post("/log-intake") # Changed dot to hyphen for standard URL practice
async def log_water_intake(request: WaterIntakeRequest):
    try:
        # 1. Log the new intake to the database
        log_intake(request.user_id, request.intake_ml)
        
        # 2. Get history to calculate today's total for the AI
        history = get_intake_history(request.user_id)
        today = datetime.today().strftime("%Y-%m-%d")
        
        # Sum only today's records
        total_today = sum(record[0] for record in history if record[1] == today)
        
        # 3. Get AI Analysis (Passing the total so it knows the status)
        # Note: You might need to update your agent.analyze_intake method signature 
        # to accept 'total_ml' instead of just the single 'intake_ml'
        analysis = agent.analyze_intake(total_today)
        
        return {
            "status": "success",
            "user_id": request.user_id,
            "added_ml": request.intake_ml,
            "total_today_ml": total_today,
            "analysis": analysis
        }
    except Exception as e:
        # It's good to catch errors so the API doesn't just "die"
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    # Formatting history for a cleaner JSON response
    formatted_history = [{"ml": h[0], "date": h[1]} for h in history]
    return {"user_id": user_id, "history": formatted_history}