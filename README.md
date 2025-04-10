# 🛍️ Product Recommendation Agent

An intelligent agentic system that interprets user queries, fetches real-time product data from Amazon and Walmart, and recommends the best-matching products with a clean Chainlit UI interface.

---

## 🚀 Features

- 🧠 **Query Interpreter Agent**: Parses and enhances user queries into structured product search formats.
- 🔎 **Real-Time Market Scraper Agent**: Fetches live product data from Amazon and Walmart using respective APIs.
- 🎯 **Product Recommendation Agent**: Analyzes and aggregates data to recommend the best product options to the user.
- 💬 **Chainlit UI**: Interactive chat interface to interact with the agent system.
- ⚡ Built using OpenAI Agent SDK + Chainlit

---

## 🧱 Tech Stack

- 🐍 Python 3.10+
- 🤖 [OpenAI Agent SDK](https://openai.github.io/openai-agents-python/)
- 🔗 [Chainlit](https://docs.chainlit.io/)
- 🌐 Amazon & Walmart APIs
- 🧪 Async Programming (`asyncio`)
- 📦 Modular Multi-Agent Architecture

---

## 📁 Project Structure

```

├── src/
│   ├── config/
│   │   ├── agents.py
│   │   └── tools.py
│   └── main.py
├── .env
└── README.md

```

---

## 💻 Chainlit Command

```bash
#!/bin/bash
echo "Starting Product Recommendation Agentic System Chainlit UI on port 8080..."
source .venv/bin/activate
chainlit run src/main.py
```

Run this command to launch the Chainlit interface.

---

## ✅ Usage

1. Clone the repo:

```bash
git clone https://github.com/your-username/product_recommendation_agent.git
cd product_recommendation_agent
```

2. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Add your `.env` with API keys for Amazon, Walmart, and OpenAI or Gemini models.

4. Run via Chainlit:

```bash
chainlit run src/product_recommendation_agent/main.py
```

---

---

## 📦 Dependencies

- `openai agent sdk`
- `chainlit`
- `asyncio`
- `openai-agents`
- `requests`
- `python-dotenv`

---

## 🧠 Future Additions

- Integration with more platforms (eBay, Flipkart)
- Image scraping and preview
- Filtering options in UI (price sliders, brands)
- User feedback to improve future recommendations

---

## 👨‍💻 Author

**Nadeem Khan**  
Fullstack Developer & Agentic Systems Enthusiast  
[LinkedIn](linkedin.com/in/nadeem-khan-a083702b9/) • [GitHub](https://github.com/nadeemsangrasi) • [Portfolio](https://nadeemkhan.vercel.app)

---
