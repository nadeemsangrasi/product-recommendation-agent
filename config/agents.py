from agents import Agent,Runner,OpenAIChatCompletionsModel,RunConfig,function_tool,AsyncOpenAI
from config.tools import initialize_tools
import os
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")
def initialize_agents():
    try:
        external_client:AsyncOpenAI=AsyncOpenAI(
            api_key=gemini_api_key,
            base_url='https://generativelanguage.googleapis.com/v1beta/'
        )
        model:OpenAIChatCompletionsModel=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=external_client)
        config:RunConfig = RunConfig(
            model=model,
            model_provider=external_client,
            tracing_disabled=True
        )

        tool_get_walmart_product_data = initialize_tools()['get_real_time_product_data_from_walmart']
        tool_get_amazon_product_data = initialize_tools()['get_real_time_product_data_from_amazon']
        query_Interpreter_Agent:Agent =Agent(
            name="Query Interpreter Agent",
         instructions="""Whenever you receive a product query, parse and refine it into the following format:

                            **Product:** <full product name>

                            **Brand:** <brand>

                            **Model:** <model>

                            **Size:** <size>

                            **Color:** <color>

                            **Material:** <key material or feature>

                            **Price:** <price range>

                            **Retailers:** Amazon, Walmart

                            If any information is missing in the user’s query, fill it in with reasonable defaults or assumptions.""",
            model=model
            )
        real_Time_Market_Scraper_Agent:Agent=Agent(
            name="Real-Time Market Scraper Agent",
            instructions="Get the latest product data from both the Walmart API and the Amazon Product Advertising API "
        "in real time, and update the repository so it always reflects current availability, pricing, "
        "and product details.",
            tools=[tool_get_walmart_product_data,tool_get_amazon_product_data]
        )
        product_Recommendation_Agent:Agent = Agent(
            name="product Recommendation Agent",
            instructions="Receive structured product criteria and the scraped results from Walmart and Amazon. "
        "Analyze the data to identify the most relevant and affordable option(s) that match the user’s needs. "
        "If exact matches are not found, recommend the closest alternatives. "
        "Provide a clear recommendation with product name, price, retailer, availability, and any useful notes "
        "(e.g., color or size variations, better-rated versions). "
        "Include a short conclusion explaining your recommendation logic.",
            model=model
            )
        return {
            'query_Interpreter_Agent':query_Interpreter_Agent,
            'real_Time_Market_Scraper_Agent':real_Time_Market_Scraper_Agent,
            'product_Recommendation_Agent':product_Recommendation_Agent,
            'config':config
        }
        
    except Exception as e:
        raise
