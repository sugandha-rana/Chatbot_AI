from langchain.agents import Tool
from service.llm_service import LLMService
from service.mock_data_service import MockDataService

def responder_doc_search_tool(query: str) -> str:
    """
    Searches event documents relevant to responders (SOPs, safety guidelines).
    """

    mock_data_service = MockDataService()
    mock_data = mock_data_service.get_all_data()
    documents = mock_data.get("documents", [])

    # More flexible document search
    query_lower = query.lower()
    matching_docs = []
    
    for doc in documents:
        doc_title = doc.get("title", "").lower()
        doc_desc = doc.get("description", "").lower()
        
        # Check if query matches title or description
        if any(word in doc_title for word in query_lower.split() if len(word) > 2):
            matching_docs.append(doc)
        elif any(word in doc_desc for word in query_lower.split() if len(word) > 2):
            matching_docs.append(doc)
        # Also check for specific document types
        elif any(doc_type in query_lower for doc_type in ["emergency", "protocol", "sop", "guideline", "map", "faq"]) and any(doc_type in doc_title for doc_type in ["emergency", "protocol", "sop", "guideline", "map", "faq"]):
            matching_docs.append(doc)
    
    if matching_docs:
        # Format found documents
        result_text = "\n\n".join([
            f"📄 {doc['title']}\n📝 {doc['description']}\n🔗 {doc.get('url', 'No URL available')}"
            for doc in matching_docs
        ])
        
        prompt = f"""
        You are a safety responder assistant.

        The responder searched for: "{query}"

        Found relevant documents:
        ---
        {result_text}
        ---

        Please provide a clear, actionable summary of the relevant information for the responder.
        Focus on practical steps and procedures they can follow immediately.
        """
    else:
        prompt = f"""
        You are a safety responder assistant.

        The responder searched for: "{query}"

        No specific documents found matching your query.

        Please suggest checking with the command center or referring to general safety protocols.
        Be helpful and provide alternative resources if available.
        """

    return LLMService().model.invoke(prompt)

def responder_dispatch_tool(query: str) -> str:
    """
    Simulates a responder dispatch operation (e.g., sending help to a zone).
    """

    mock_data_service = MockDataService()
    mock_data = mock_data_service.get_all_data()
    incidents = mock_data.get("incidents", [])
    alerts = mock_data.get("alerts", [])
    users = mock_data.get("users", [])

    # Check if there are active incidents in the mentioned location
    location_lower = query.lower()
    active_incidents = []
    active_alerts = []
    
    # Search for incidents in the location
    for incident in incidents:
        incident_desc = incident.get("description", "").lower()
        if location_lower in incident_desc or any(word in incident_desc for word in location_lower.split()):
            active_incidents.append(incident)
    
    # Search for alerts in the location
    for alert in alerts:
        alert_desc = alert.get("description", "").lower()
        if location_lower in alert_desc or any(word in alert_desc for word in location_lower.split()):
            active_alerts.append(alert)
    
    # Check for responders in the area
    responders_in_area = [user for user in users if user.get("user_role") == "responder_security" and location_lower in user.get("user_zone", "").lower()]
    
    if active_incidents or active_alerts:
        # There are active issues in the area
        incident_text = ""
        if active_incidents:
            incident_text = "\n".join([f"- {inc['incident_type']}: {inc['description']}" for inc in active_incidents])
        
        alert_text = ""
        if active_alerts:
            alert_text = "\n".join([f"- {alert['alert_type']}: {alert['description']}" for alert in active_alerts])
        
        responder_text = ""
        if responders_in_area:
            responder_text = f"\nResponders available in area: {len(responders_in_area)}"
        
        prompt = f"""
        You are a responder dispatch agent.

        Dispatch requested to: "{query}"

        ACTIVE ISSUES IN AREA:
        {incident_text}
        {alert_text}
        {responder_text}

        Please provide dispatch instructions, ETA, and any specific protocols to follow.
        Be professional and provide clear action steps.
        """
    else:
        # No active issues, but still provide dispatch info
        prompt = f"""
        You are a responder dispatch agent.

        Dispatch requested to: "{query}"

        No active incidents or alerts reported in this area.

        Confirm that the responder team has been notified and provide standard dispatch procedures.
        Include ETA and any relevant safety protocols.
        """

    return LLMService().model.invoke(prompt)
def get_responder_tools():
    doc_search_tool = Tool(
        name="DocSearchTool",
        func=responder_doc_search_tool,
        description="Search responder-related documents like SOPs or safety instructions."
    )

    dispatch_tool = Tool(
        name="DispatchTool",
        func=responder_dispatch_tool,
        description="Dispatch help to a specific zone or handle responder alerts."
    )

    return [doc_search_tool, dispatch_tool]
