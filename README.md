# Reasoning over ML – Multi-Agent Chatbot

Welcome to **Reasoning over ML**, a delightful and powerful multi-agent conversational interface built for exploring and explaining machine learning models. Harness the combined intelligence of specialized AI agents—Analyst, Reasoning, and Reviewer—all wrapped in a sleek Gradio chat UI!

## 🚀 Key Features

- **Multi-Agent Conversation**: Seamless collaboration between AI agents to analyze, reason, and validate insights.
- **Gradio-Powered UI**: Interactive chat interface that displays messages and optional generated images.
- **Azure AI & Semantic Kernel**: Leverages Azure OpenAI, Semantic Kernel, and custom Jinja2 prompts for dynamic intelligence.
- **Code Interpretation**: Integrates a Code Interpreter tool for on-the-fly data analysis and visualization.
- **Extendable & Modular**: Easily plug new agents, strategies, and tools to customize workflows.

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/gbbai-o1-reasoning-over-ml.git
   cd gbbai-o1-reasoning-over-ml
   ```
2. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (example):
   ```bash
   export TEMPLATE_DIR_PROMPTS="path/to/templates"
   export TEMPLATE_REASONING_AGENT="reasoning.jinja"
   export TEMPLATE_ANALYST_AGENT="analyst.jinja"
   export TEMPLATE_REVIEWER_AGENT="reviewer.jinja"
   ```

## 🎯 Usage

### 1. Run the Gradio Chat UI (Notebook)

Open and run the `mas-ui.ipynb` notebook in Jupyter or VSCode:

1. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
2. Open `mas-ui.ipynb` and execute all cells.
3. Interact with the chatbot in your browser!

### 2. Command-Line Cleanup

To remove existing Azure agents before a fresh start, run:
```bash
python main.py
```
Follow the prompts to clean and interact via CLI.

## 📂 Project Structure

```
├── mas-ui.ipynb         # Gradio chat interface
├── main.py              # CLI entrypoint to clean agents
├── src/mas.py           # Orchestrator & agent definitions
├── src/agents/plugins   # Custom retrieval plugin
├── data/                # Example prediction data
├── model/               # Training, deployment, and environment config
├── infra/               # Azure infrastructure as code
└── requirements.txt     # Python dependencies
```

## 🤝 Contributing

We welcome contributions! Please review our [CONTRIBUTING.md](CONTRIBUTING.md) and follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-awesome-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to your branch (`git push origin feature/my-awesome-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the [MIT License](LICENSE.md). 

**Enjoy exploring ML reasoning with your AI agents!**

## TO-DO
- The Gradio UI has some issues and need to be fixed
- The interactions between the agents can be optimized
- Add a reasoning checkbox to activate the Reasoning Agent and needed