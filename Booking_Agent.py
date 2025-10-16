import streamlit as st
from groq import Groq
from fastmcp import Client
from datetime import datetime, timedelta
import asyncio
import json

# Initialize clients
groq_client = Groq(api_key="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")
MCP_SERVER_URL = "http://localhost:8000/mcp"  # Your running MCP server URL

# Fixed system prompt for booking agent
SYSTEM_PROMPT = """
You are a professional booking agent for appointment scheduling and reservations. 
Your role is to confirm bookings, provide friendly responses, and handle any issues politely.
Always respond in a friendly, professional manner.
Output in a structured format: 
- Greeting and confirmation
- Booking details summary
- Next steps
Use the following JSON for key details if confirming: {"status": "confirmed", "booking_id": "unique_id", "date": "YYYY-MM-DD", "time": "HH:MM", "service": "service_name"}
"""

async def process_booking_with_mcp(user_inputs):
    """Call MCP server to book appointment."""
    async with Client(MCP_SERVER_URL) as mcp_client:
        try:
            result = await mcp_client.call_tool("book_appointment", user_inputs)
            return result.content[0].text  # MCP response (e.g., success message with booking ID)
        except Exception as e:
            return f"Booking error: {str(e)}"

def get_ai_response(booking_result):
    """Use Groq to generate a polished response based on MCP result."""
    user_prompt = f"""
    User booking processed with result: {booking_result}
    
    Generate a friendly confirmation message.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

# Streamlit App
st.set_page_config(
    page_title="Professional Booking Agent",
    page_icon="📅",
    layout="wide"
)

# Custom CSS for modern professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTitle { font-family: 'Arial', sans-serif; font-weight: bold; color: #2c3e50; }
    .stTextInput > label { font-weight: bold; color: #34495e; }
    .stSelectbox > label { font-weight: bold; color: #34495e; }
    .stDateInput > label { font-weight: bold; color: #34495e; }
    .stButton > button { background-color: #3498db; color: white; border-radius: 8px; font-weight: bold; }
    .stButton > button:hover { background-color: #2980b9; }
    .response-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📅 Professional Appointment Booking")
st.markdown("Schedule your reservation with our AI-powered booking agent. Fill in the details below to get started.")

# Sidebar for instructions
with st.sidebar:
    st.header("How to Book")
    st.markdown("""
    - Select a service
    - Choose a date (next 30 days)
    - Pick a time slot
    - Provide your contact info
    - Submit for instant confirmation via Google Calendar & Email
    """)
    st.info(f"Backend MCP Server: {MCP_SERVER_URL}")

# Main form
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Booking Details")
    service = st.selectbox("Select Service", ["Consultation", "Meeting", "Workshop", "Custom Reservation"])
    
    # Date input (next 30 days, starting from current date: Oct 16, 2025)
    min_date = datetime(2025, 10, 16)
    max_date = min_date + timedelta(days=30)
    selected_date = st.date_input("Preferred Date", min_value=min_date, max_value=max_date, value=min_date + timedelta(days=1))
    
    # Time slots
    time_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"]
    selected_time = st.selectbox("Preferred Time", time_slots)

with col2:
    st.subheader("Contact Information")
    name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email", type="email")

# Submit button
if st.button("Book Appointment", type="primary"):
    if name and email:
        user_inputs = {
            'name': name,
            'email': email,
            'service': service,
            'date': selected_date.strftime("%Y-%m-%d"),
            'time': selected_time
        }
        
        with st.spinner("Processing your booking with MCP Server..."):
            # Call MCP asynchronously
            mcp_result = asyncio.run(process_booking_with_mcp(user_inputs))
            
            # Get polished AI response
            ai_response = get_ai_response(mcp_result)
        
        # Display response in a styled box
        st.markdown('<div class="response-box">', unsafe_allow_html=True)
        st.markdown(f"**Booking Response:**\n\n{ai_response}\n\n**MCP Details:** {mcp_result}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Optional: Parse for success
        if "successfully" in mcp_result.lower():
            st.success("✅ Booking confirmed! Check your email and Google Calendar.")
    else:
        st.warning("Please fill in all fields.")

# Footer
st.markdown("---")
st.markdown("*Powered by Groq AI, FastMCP, Google Calendar & Gmail*")