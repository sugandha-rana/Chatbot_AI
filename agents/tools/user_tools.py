from langchain.agents import Tool
from service.llm_service import LLMService
from service.mock_data_service import MockDataService
import uuid

def invitee_incident_report_tool(query: str) -> str:
    """
    Invitee reports an incident (e.g., lost item, panic, injury) via chatbot.
    """

    # Step 1: Check if this is a lost item report or item description
    lost_keywords = ["lost", "missing", "can't find", "misplaced", "phone", "wallet", "keys", "bag", "jacket", "item"]
    is_lost_item = any(keyword in query.lower() for keyword in lost_keywords)
    
    # Also treat any item description as a lost item report
    if not is_lost_item and any(word in query.lower() for word in ["black", "red", "blue", "phone", "wallet", "keys", "bag", "jacket", "zone"]):
        is_lost_item = True
    
    if is_lost_item:
        # For lost items, first search the lost and found database
        mock_data_service = MockDataService()
        mock_data = mock_data_service.get_all_data()
        items = mock_data.get("lost_and_found", [])
        
        # Search for matching items based on the query
        matches = []
        query_lower = query.lower()
        
        for item in items:
            item_desc = item["description"].lower()
            # Check if any part of the query matches the item description
            query_words = [word for word in query_lower.split() if len(word) > 2]
            
            # More flexible matching
            if any(word in item_desc for word in query_words):
                matches.append(item)
            elif any(word in query_lower for word in item_desc.split()):
                matches.append(item)
            # Also check for color matches
            elif any(color in query_lower and color in item_desc for color in ["black", "red", "blue", "gold", "white"]):
                matches.append(item)
        
        if matches:
            # Found matching items
            result_text = "\n".join([
                f"- {item['description']} (found in {item['zone']})" 
                for item in matches
            ])
            
            prompt = f"""
            You are a helpful assistant at a public event.

            A user has reported losing an item: "{query}"

            Great news! We found matching items in our lost and found database:
            ---
            {result_text}
            ---

            Please tell the user they can collect their item from the help desk.
            Ask them to bring a valid ID for verification.
            Be friendly and helpful.
            """
        else:
            # No matches found, ask for more details and log the report
            incident_type = "Lost Item"
            location = "Unknown"
            description = query
            user_id = "user_001"
            report_id = f"REPORT-{uuid.uuid4().hex[:6].upper()}"

            # Log the report
            new_report = {
                "user_id": user_id,
                "incident_type": incident_type,
                "location": location,
                "description": description,
                "status": "Pending",
                "report_id": report_id
            }
            mock_data.setdefault("user_reports", []).append(new_report)

            prompt = f"""
            You are a helpful assistant at a public event.

            A user has reported losing an item: "{query}"

            Unfortunately, we don't have any matching items in our lost and found database.

            I've logged your report (ID: {report_id}) and we'll keep an eye out for your item.
            Please check with event staff or security, and we'll contact you if it turns up.

            Be supportive and helpful.
            """
    else:
        # For other incidents, log the report
        incident_type = "General Incident"
        location = "Unknown"
        description = query
        user_id = "user_001"
        report_id = f"REPORT-{uuid.uuid4().hex[:6].upper()}"

        # Step 2: Save to mock data
        mock_data_service = MockDataService()
        mock_data = mock_data_service.get_all_data()
        new_report = {
            "user_id": user_id,
            "incident_type": incident_type,
            "location": location,
            "description": description,
            "status": "Pending",
            "report_id": report_id
        }
        mock_data.setdefault("user_reports", []).append(new_report)

        prompt = f"""
        You are a helpful assistant at a public event.

        A user has submitted the following incident report via chat:
        ---
        Description: "{description}"
        Location: {location}
        Type: {incident_type}
        ---

        A report ID ({report_id}) has been generated.

        Please confirm to the user that their report has been logged and let them know that someone will attend to it shortly.
        """

    return LLMService().model.invoke(prompt)
def invitee_lost_and_found_tool(query: str) -> str:
    """
    Invitee searches lost & found items via chatbot.
    """

    mock_data_service = MockDataService()
    mock_data = mock_data_service.get_all_data()
    items = mock_data.get("lost_and_found", [])

    matches = [item for item in items if query.lower() in item["description"].lower()]

    if matches:
        # Format matches with clear instructions
        result_text = "\n".join([
            f"- {item['description']} (found in {item['zone']})" 
            for item in matches
        ])
        
        prompt = f"""
        You are an assistant helping event attendees search for lost items.

        The user searched for: "{query}"

        Great news! We found matching items in our lost and found:
        ---
        {result_text}
        ---

        Please tell the user they can collect their item from the help desk. 
        Ask them to bring a valid ID for verification.
        Be friendly and helpful.
        """
    else:
        prompt = f"""
        You are an assistant helping event attendees search for lost items.

        The user searched for: "{query}"

        Unfortunately, we don't have any matching items in our lost and found database.

        Please kindly let them know that their item hasn't been found yet, 
        but we'll keep their report on file in case it turns up later.
        Suggest they check with event staff or security.
        Be supportive and helpful.
        """

    return LLMService().model.invoke(prompt)
def get_user_tools():
    incident_tool = Tool(
        name="IncidentReportTool",
        func=invitee_incident_report_tool,
        description="Let users report incidents like lost items, injuries, or emergencies."
    )

    lost_found_tool = Tool(
        name="LostAndFoundTool",
        func=invitee_lost_and_found_tool,
        description="Allow users to check if their lost item has been found."
    )

    return [incident_tool, lost_found_tool]
