import json
import anthropic
from datetime import datetime, timedelta
from langgraph.graph import StateGraph
from typing import Dict, Optional, List
from langchain_core.runnables import RunnableLambda

# Claude API Setup
anthropic_client = anthropic.Anthropic(api_key="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")

# Function to interact with Claude
def call_claude(prompt: str):
    response = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()

# Mock function tools
def create_meeting(arg: Dict):
    return {
        "status": "success",
        "meeting_id": "abc123",
        "summary": f"Meeting '{arg['summary']}' scheduled on {arg['start_time']}."
    }

def get_meetings(arg: Dict):
    return [{
        "id": "event123",
        "summary": "Project Sync",
        "start": {"dateTime": "2025-03-15T06:00:00Z", "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": "2025-03-15T07:00:00Z", "timeZone": "Asia/Kolkata"},
        "attendees": [{"email": "sujanmoi787@gmail.com"}],
        "htmlLink": "https://calendar.google.com/event?eid=event123"
    }]

def delete_meeting(event_id: str):
    return {"status": "success", "message": f"Meeting with ID {event_id} deleted."}

# State structure
class AgentState(Dict):
    query: str
    action: Optional[str]
    meeting_data: Optional[Dict]
    meetings: Optional[List[Dict]]
    delete_id: Optional[str]
    summary: Optional[str]

# Step 1: Determine Intent
def determine_intent(state: AgentState):
    query = state["query"]
    prompt = f"Determine the intent of this query: '{query}'. Reply with 'create', 'fetch', 'delete', or 'calculate'."
    action = call_claude(prompt)
    return {"action": action.lower()}  # Example: "create", "fetch", "delete", "calculate"

# Step 2: Handle Meeting Creation
def handle_create_meeting(state: AgentState):
    query = state["query"]
    prompt = f"Extract structured meeting details (JSON) from this query: '{query}'. Format: {{'summary': str, 'start_time': str, 'end_time': str, 'attendees': list}}"
    meeting_data = json.loads(call_claude(prompt))  # Ensure Claude returns valid JSON
    result = create_meeting(meeting_data)
    return {"meeting_data": meeting_data, "summary": result["summary"]}

# Step 3: Handle Fetching Meetings
def handle_get_meetings(state: AgentState):
    query = state["query"]
    prompt = f"Extract date range (JSON) from this query: '{query}'. Format: {{'start_time': str, 'end_time': str}}"
    time_range = json.loads(call_claude(prompt))
    meetings = get_meetings(time_range)

    if not meetings:
        return {"meetings": [], "summary": "No meetings found for the requested date/time."}

    summary_list = [f"- **{m['summary']}** from {m['start']['dateTime']} to {m['end']['dateTime']} [Meeting Link]({m['htmlLink']})"
                    for m in meetings]
    return {"meetings": meetings, "summary": "\n".join(summary_list)}

# Step 4: Handle Deleting Meetings
def handle_delete_meeting(state: AgentState):
    query = state["query"]
    prompt = f"Extract the event ID from this query: '{query}'"
    event_id = call_claude(prompt)
    result = delete_meeting(event_id)
    return {"delete_id": event_id, "summary": result["message"]}

# Step 5: Calculate Meeting Hours
def handle_calculate_meeting_time(state: AgentState):
    query = state["query"]
    prompt = f"Extract the date (JSON) from this query: '{query}'. Format: {{'start_time': str, 'end_time': str}}"
    time_range = json.loads(call_claude(prompt))
    meetings = get_meetings(time_range)

    total_minutes = sum(
        (datetime.fromisoformat(m["end"]["dateTime"][:-1]) - datetime.fromisoformat(m["start"]["dateTime"][:-1])).total_seconds() / 60
        for m in meetings
    )
    total_hours = total_minutes / 60
    return {"summary": f"You have spent {total_hours:.2f} hours in meetings."}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("determine_intent", determine_intent)
workflow.add_node("handle_create_meeting", handle_create_meeting)
workflow.add_node("handle_get_meetings", handle_get_meetings)
workflow.add_node("handle_delete_meeting", handle_delete_meeting)
workflow.add_node("handle_calculate_meeting_time", handle_calculate_meeting_time)

# Define Conditional Edges
workflow.set_entry_point("determine_intent")
workflow.add_conditional_edges(
    "determine_intent",
    {
        "create": handle_create_meeting,  # Use function reference, not string
        "fetch": handle_get_meetings,
        "delete": handle_delete_meeting,
        "calculate": handle_calculate_meeting_time
    },
    lambda state: state["action"]  # No need for RunnableLambda here
)

# Compile the Graph
app = workflow.compile()

# Example Queries
queries = [
    "Create a meeting tomorrow at 2am for 1 hour with attendees sujanmoi@gmail.com and brayan@gmail.com.",
    # "Give me the list of all meetings today.",
    # "Check my calendar tomorrow from 2pm to 3pm and delete any meetings.",
    # "How many hours did I spend in meetings yesterday?"
]

for query in queries:
    result = app.invoke({"query": query})
    print(f"Query: {query}")
    print(f"Response:\n{result['summary']}\n")
