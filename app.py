import gradio as gr
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def process_task(task):
    try:
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4"),
        )
        result = await agent.run()
        return result
    except Exception as e:
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
    port = int(os.environ.get("PORT", 7860))
    iface.launch(server_name="0.0.0.0", server_port=port) 