import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class WaterIntakeAgent:
    def __init__(self):
        # Attach the LLM to the instance using 'self'
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite", 
            api_key=GEMINI_API_KEY,
            temperature=0.5
        )
        self.history = []

    def analyze_intake(self, intake_ml):
        prompt = f"""
                 You are a hydration assistant. The user has consumed {intake_ml}ml of water today.
                 Provide a hydration status and suggest if they need to drink more water.
                 """
        
        # Now 'self.llm' exists and can be called
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        raw_content = response.content
        
        if isinstance(raw_content, list):
            return raw_content[0].get('text', 'No analysis available.')
        
        return raw_content

if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Feedback: {feedback}")