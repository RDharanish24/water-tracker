import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite", # 'latest' is best for free tier
    api_key=GEMINI_API_KEY,
    temperature=0.5
)

class WaterIntakeAgent:
    def __init__(self):
        self.history=[]

    def analyze_intake(self,intake_ml):

        prompt=f"""
                you are an hydration assistant , the user has consumed {intake_ml} of water today.
                provide a hydration status and suggest if they need to drink more water
                """
        response=llm.invoke([HumanMessage(content=prompt)])
        return response.content
    

if __name__=="__main__":
    agent=WaterIntakeAgent()
    intake=1500
    feedback=agent.analyze_intake(intake)
    print(feedback)