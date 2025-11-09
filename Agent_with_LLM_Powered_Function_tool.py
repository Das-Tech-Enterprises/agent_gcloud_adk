from google.adk.tools import FunctionTool
from google.genai import types
from google import genai
from google.adk.models.lite.llm  import LiteLlm
import litellm

# Defining the necessary variables
AGENT_MODEL = LiteLlm(model="openai/gpt-4o-mini")
APP_NAME = "adk_course_app"
USER_ID = "user_1234" ## Dummy user ID
SESSION_ID = "support_session" ## Dummy session ID for session management


# Defining a simple FAQ knowledge base
FAQ_DATA = {
    "return policy": "Our return policy allows returns within 30 days of purchase with a valid receipt.",
    "support hours": "Our support team is available from 9 AM to 5 PM, Monday to Friday.",
    "contact": "You can reach our support team at support@dte.com"
}


# Defining the tool function
def lookup_faq(question: str) -> str:
    question = question.lower()
    for key in FAQ_DATA:
        if key in question:
            return FAQ_DATA[key]
    return "I'm sorry, I don't have an answer to that question."


# Wrap the tool function using FunctionTool
faq_tool = FunctionTool(func=lookup_faq)

# Creating the Agent
support_agent = LlmAgent(
    name="SupportAgent",
    descrption="An agent that answers customer queries based ona set of FAQs."
    instruction="Use the provided FAQ tool to answer customer questions effectively.",
    model=AGENT_MODEL,
    tools=[faq_tool]
)

# Setup the session service and runner
session_service = InMemorySessionService()
await session_service.create_session(app_name=APP_NAME, session_id=SESSION_ID, user_id=USER_ID)
runner = Runner(agent=support_agent, session_service=session_service, app_name=APP_NAME)

# Define and call the agent asynchronously




# Run the agent
await call_agent_async("What is your return policy?")