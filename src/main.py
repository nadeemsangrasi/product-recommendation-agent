import chainlit as cl
from agents import Runner
from config.agents import initialize_agents
import sys
from typing import Optional,Dict

@cl.oauth_callback
def handle_oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    # Optionally modify or enrich the default_user using raw_user_data.
    return default_user


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Running Shoes",
            message="Men's Nike Air Zoom Pegasus 39 running shoes, size 10, under $100.",
            icon="/public/shoes.svg",
        ),
        cl.Starter(
            label="Smartphone",
            message="Best Android smartphone under $500.",
            icon="/public/phone.svg",
        ),
        cl.Starter(
            label="Laptop",
            message="Lightweight laptop for programming under $1000.",
            icon="/public/laptop.svg",
        ),
    ]

async def run_workflow(raw_query, agents_config):
    try:
        query_agent= agents_config['query_Interpreter_Agent']
        scraper_agent=agents_config['real_Time_Market_Scraper_Agent']
        recommendation_agent=agents_config['product_Recommendation_Agent']
        config = agents_config["config"]

        await cl.Message(content=f"""
## 🔍 Interpretation Phase

Parsing and structuring your query: **{raw_query}**
""").send()
        interpret_result = await Runner.run(
            starting_agent=query_agent,
            input=f"Format this query into structured criteria:\n{raw_query}",
            run_config=config
        )
        criteria = interpret_result.final_output

        await cl.Message(content=f"""
## 📋 Criteria:
```
{criteria}
```
""").send()

        await cl.Message(content=f"""
## 📦 Scraping Phase

Fetching product data from Walmart and Amazon...
""").send()
        scrape_result = await Runner.run(
            starting_agent=scraper_agent,
            input=criteria,
            run_config=config
        )
        scraped_data = scrape_result.final_output

        await cl.Message(content=f"""
## 🧾 Scraped Data:
```
{scraped_data}
```
""").send()

        await cl.Message(content="""
## 🧠 Recommendation Phase

Analyzing data to recommend the best product...
""").send()
        recommend_result = await Runner.run(
            starting_agent=recommendation_agent,
            input=f"Based on these criteria and data, recommend the best product:\n{criteria}\n{scraped_data}",
            run_config=config
        )
        recommendation_text = recommend_result.final_output

        await cl.Message(content=f"""
## 🎯 Your Product Recommendation

{recommendation_text}
""").send()
        return True

    except Exception as e:
        await cl.Message(content=f"❌ Error during workflow: {str(e)}").send()
        return False

@cl.on_chat_start
async def on_chat_start():
    agents = initialize_agents()
    cl.user_session.set("agents_config", agents)
    await cl.Message(content="""
# 🛍️ Welcome to the Product Recommendation Agent!

This AI-powered tool recommends products from Amazon and Walmart based on your detailed query.

## How it works:

1. **🔍 Interpretation Phase**: Our Query Interpreter Agent structures your product query.
2. **📦 Scraping Phase**: Our Product Scraper Agent fetches live data from Amazon and Walmart.
3. **🎯 Recommendation Phase**: Our Product Recommendation Agent analyzes and suggests the best options.

**To get started, simply type a product query in the format:**
"Men's Nike Air Zoom Pegasus 39 running shoes, size 10, under $100"""
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    raw_query = message.content.strip()
    if not raw_query:
        await cl.Message(content="⚠️ Please enter a valid product query.").send()
        return

    agents_config = cl.user_session.get("agents_config")
    if not agents_config:
        await cl.Message(content="❌ Session expired. Please refresh to restart.").send()
        return

    await cl.Message(content="""
## 🚀 Starting Product Recommendation

Please wait while we process your query and find the best product options...
""").send()
    await run_workflow(raw_query, agents_config)
