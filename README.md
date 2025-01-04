# 🎓 BitsGPT 2.0

BitsGPT is a chatbot designed for the students of BPHC. It uses an agentic framework to provide accurate and reliable responses to a variety of queries related to campus life, academics, and placements. This rewrite improves modularity, accuracy, and performance.

## Features

- **Query Classification**: Automatically detects query intent (campus queries, course-related, PS/placement-related, etc.).
- **Tool-Based Query Handling**: Uses dedicated tools for data retrieval based on query intent.
- **Reliable and Modular Design**: Built with LangGraph and Langchain for agentic capabilities.

---

## Getting Started

Follow these steps to set up BitsGPT locally:

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for dependency management

---

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/crux-bphc/bitsgpt-rewrite.git
   cd bitsgpt
   ```

2. **Install Dependencies**:
   Use Poetry to install all required packages.

   ```bash
   poetry install
   ```

3. **Activate the Poetry Shell**:
   Start a Poetry-managed virtual environment.

   ```bash
   poetry shell
   ```

4. **Run the Application**:
   Run langgraph dev to start the server. This will open langgraph studio in your browser.
   ```bash
   langgraph dev
   ```

---

### Configuration

Create a `.env` file in the project root with the following entries:

```env
GROQ_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT="bitsgpt-rewrite"
```

Replace the keys with the appropriate values.

---

## Contributing

We welcome contributions to make BitsGPT better! Feel free to submit issues or pull requests.
