# Customer AI Agent

A Streamlit-powered chat interface that uses Langflow API to provide automated customer service responses. This AI agent can handle queries about orders, shipping, returns, and general customer service inquiries.
![image](https://github.com/user-attachments/assets/6ccd3a5b-8ad0-402c-8f0e-48b6c18d4ea8)

## Flow
![image](https://github.com/user-attachments/assets/79f27e28-7fb0-42d8-93c4-a3d9cd815ec5)
![image](https://github.com/user-attachments/assets/5e1ad7ea-981f-4453-a114-6ef5f05e8214)
![image](https://github.com/user-attachments/assets/03f75bf1-6e1c-4ec3-9c24-5afc6560bdc0)

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/kstubhieeee/customer-ai-agent.git
```

```
cd customer-ai-agent
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
BASE_API_URL="https://api.langflow.astra.datastax.com"
LANGFLOW_ID="your-langflow-id"
FLOW_ID="your-flow-id"
APPLICATION_TOKEN="your-application-token"
```

### Running the Application

Launch the application using:

```bash
streamlit run main.py
```

The chat interface will be available at `http://localhost:8501`

## 💡 Usage Examples

The AI agent can handle various customer service queries:

- "What are your shipping times?"
- "What's your return policy?"

## 🔧 Technical Details

### Project Structure

```
customer-ai-agent/
├── main.py              # Main application code
├── requirements.txt     # Dependencies
├── .env                # Environment variables (not tracked)
└── README.md           # Documentation
```

### Dependencies

- `streamlit`: Web interface
- `python-dotenv`: Environment variable management
- `requests`: API communication

## 🐛 Error Handling

The application handles various scenarios:

- API timeouts
- Authentication failures
- Missing environment variables
- Network issues
- Invalid responses

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Langflow](https://langflow.org/)
- DataStax Astra DB integration

---

⭐ Star this repository if you find it helpful!
