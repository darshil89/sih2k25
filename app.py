import streamlit as st
import requests
import base64
from PIL import Image
import io
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="UFDR AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f8f9fa;
        color: #333;
        margin-right: 20%;
    }
    .message-content {
        flex: 1;
    }
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
    }
    .user-avatar {
        background-color: #007bff;
    }
    .assistant-avatar {
        background-color: #28a745;
    }
    .image-preview {
        max-width: 200px;
        max-height: 200px;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
    }
    .upload-section {
        border: 2px dashed #007bff;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def send_message_to_backend(message, report_id, image_data=None):
    """Send message to FastAPI backend"""
    try:
        url = f"http://localhost:8080/api/chat/{report_id}"
        payload = {
            "message": message,
            "report_id": report_id,
            "image_data": image_data
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"response": f"Error: {response.status_code}", "status": "error"}
    except Exception as e:
        return {"response": f"Connection error: {str(e)}", "status": "error"}

def save_uploaded_file(uploaded_file, report_id):
    """Save uploaded file to reports directory"""
    try:
        # Create reports directory if it doesn't exist
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_id}_{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(reports_dir, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path, filename
    except Exception as e:
        return None, str(e)

def chat_tab():
    """Chat interface tab"""
    st.title("💬 UFDR Chat Interface")
    st.markdown("Chat with your UFDR reports using AI assistance")
    
    # Sidebar for report selection and settings
    with st.sidebar:
        st.header("Chat Settings")
        report_id = st.text_input("Report ID", value="default-report", help="Enter the report ID to chat with")
        
        st.markdown("---")
        st.markdown("### Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="Upload an image to include in your message",
            key="chat_image_upload"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "image" in message:
                    st.image(message["image"], caption="Attached Image", width=200)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        user_message = {"role": "user", "content": prompt}
        if uploaded_file is not None:
            user_message["image"] = uploaded_file
        st.session_state.messages.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Attached Image", width=200)
        
        # Process image if uploaded
        image_data = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_data = encode_image_to_base64(image)
        
        # Send to backend and get response
        with st.spinner("Thinking..."):
            response = send_message_to_backend(prompt, report_id, image_data)
        
        # Add assistant response to chat history
        assistant_message = {"role": "assistant", "content": response["response"]}
        st.session_state.messages.append(assistant_message)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response["response"])
    
    # Clear chat button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()

def upload_tab():
    """Report upload tab"""
    st.title("📁 Upload UFDR Reports")
    st.markdown("Upload and manage your UFDR reports")
    
    # Upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload New Report")
    
    # Report ID input
    report_id = st.text_input(
        "Report ID", 
        value="", 
        help="Enter a unique identifier for this report",
        key="upload_report_id"
    )
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose UFDR report files",
        type=['pdf', 'docx', 'txt', 'xlsx', 'csv'],
        accept_multiple_files=True,
        help="Upload one or more UFDR report files"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process uploaded files
    if uploaded_files and report_id:
        st.markdown("### 📋 Upload Summary")
        
        success_count = 0
        error_count = 0
        
        for uploaded_file in uploaded_files:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"📄 {uploaded_file.name}")
                st.write(f"Size: {uploaded_file.size} bytes")
            
            with col2:
                if st.button(f"Upload", key=f"upload_{uploaded_file.name}"):
                    file_path, result = save_uploaded_file(uploaded_file, report_id)
                    
                    if file_path:
                        st.success(f"✅ Saved as: {result}")
                        success_count += 1
                    else:
                        st.error(f"❌ Error: {result}")
                        error_count += 1
        
        # Summary
        if success_count > 0 or error_count > 0:
            st.markdown("---")
            if success_count > 0:
                st.success(f"✅ Successfully uploaded {success_count} file(s)")
            if error_count > 0:
                st.error(f"❌ Failed to upload {error_count} file(s)")
    
    elif uploaded_files and not report_id:
        st.warning("⚠️ Please enter a Report ID before uploading files")
    
    # Display existing reports
    st.markdown("---")
    st.markdown("### 📚 Existing Reports")
    
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        report_files = os.listdir(reports_dir)
        if report_files:
            for file in report_files:
                file_path = os.path.join(reports_dir, file)
                file_size = os.path.getsize(file_path)
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"📄 {file}")
                
                with col2:
                    st.write(f"{file_size} bytes")
                
                with col3:
                    st.write(file_date.strftime("%Y-%m-%d"))
                
                with col4:
                    if st.button("🗑️", key=f"delete_{file}", help="Delete file"):
                        try:
                            os.remove(file_path)
                            st.success("File deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting file: {e}")
        else:
            st.info("No reports uploaded yet")
    else:
        st.info("No reports directory found")

def main():
    """Main application"""
    # Header
    st.markdown("# 🤖 UFDR AI Assistant")
    st.markdown("Intelligent analysis and chat interface for UFDR reports")
    
    # Create tabs
    tab1, tab2 = st.tabs(["💬 Chat Interface", "📁 Upload Reports"])
    
    with tab1:
        chat_tab()
    
    with tab2:
        upload_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("### 🔧 Backend Status")
    
    # Check backend connection
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        if response.status_code == 200:
            st.success("✅ Backend server is running")
        else:
            st.error("❌ Backend server returned an error")
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend server is not running. Please start the FastAPI server.")
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {str(e)}")

if __name__ == "__main__":
    main()
