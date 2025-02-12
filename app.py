import gradio as gr
import os
import sys
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# Debug: Print environment variables and system info
logger.info("Python version: %s", sys.version)
logger.info("Environment variables available: %s", [k for k in os.environ.keys()])
logger.info("OPENAI_API_KEY present: %s", "OPENAI_API_KEY" in os.environ)
logger.info("PORT value: %s", os.environ.get("PORT"))

async def process_task(task):
    try:
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OpenAI API key not found")
            return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            
        logger.info("Initializing ChatOpenAI...")
        llm = ChatOpenAI(model="gpt-4")
        logger.info("Creating Agent...")
        agent = Agent(
            task=task,
            llm=llm,
        )
        logger.info("Running task: %s", task)
        result = await agent.run()
        return result
    except Exception as e:
        logger.exception("Error in process_task")
        return f"Error: {str(e)}"

def run_task(task):
    try:
        return asyncio.run(process_task(task))
    except Exception as e:
        logger.exception("Error in run_task")
        return f"Error in run_task: {str(e)}"

# Create Gradio interface
try:
    iface = gr.Interface(
        fn=run_task,
        inputs=gr.Textbox(lines=2, placeholder="Enter your browser automation task here..."),
        outputs="text",
        title="Browser-Use Web Interface",
        description="Enter a task to automate in your browser. The AI will execute it and return the results.",
        examples=[
            ["Go to Reddit, search for 'browser-use', and return the title of the first post."],
            ["Search for 'machine learning' on Google and return the first 3 results."]
        ]
    )
except Exception as e:
    logger.exception("Error creating Gradio interface")
    raise

# Launch with server name and port for Railway
if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 7860))
        logger.info("Starting server on port %s...", port)
        # Start with minimal options to ensure quick startup
        iface.launch(
            server_name="0.0.0.0",
            server_port=port,
            show_error=True
        )
    except Exception as e:
        logger.exception("Failed to start server")
        raise 