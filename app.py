import gradio as gr
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Debug: Print environment variables (excluding sensitive data)
print("Environment variables available:", [k for k in os.environ.keys()])
print("OPENAI_API_KEY present:", "OPENAI_API_KEY" in os.environ)
print("PORT value:", os.environ.get("PORT"))

async def process_task(task):
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            
        print("Initializing ChatOpenAI...")
        llm = ChatOpenAI(model="gpt-4")
        print("Creating Agent...")
        agent = Agent(
            task=task,
            llm=llm,
        )
        print("Running task:", task)
        result = await agent.run()
        return result
    except Exception as e:
        print("Error occurred:", str(e))
        return f"Error: {str(e)}"

def run_task(task):
    return asyncio.run(process_task(task))

# Create Gradio interface
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

# Launch with server name and port for Railway
if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 7860))
        print(f"Starting server on port {port}...")
        iface.launch(server_name="0.0.0.0", server_port=port, show_error=True)
    except Exception as e:
        print("Failed to start server:", str(e))
        raise 