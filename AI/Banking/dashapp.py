from dash import Dash, dcc, callback, Output, Input, no_update
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import TavilySearchResults
from dotenv import find_dotenv, load_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)   # change to use Groq
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # https://platform.openai.com/api-keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # https://app.tavily.com/sign-in

search_tool = TavilySearchResults()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal="""Uncover the latest news and trends about the bank selected by the user in the task section.""",
  backstory="""You work at a leading banking think tank. 
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
)
writer = Agent(
  role='Banking Content Strategist',
  goal='Craft compelling content from news on the selected bank.',
  backstory="""You are a famous Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives. You avoid complex words so it doesn't sound like you're an AI.""",
  verbose=True,
  allow_delegation=True,
)


app = Dash()
app.layout = [
    dcc.Markdown("# Multi AI Agent System - Bank Analysis"),
    dcc.Markdown("Choose the bank you would like your AIs to research and write a blog post on"),
    dcc.Dropdown(["JPMORGAN CHASE", "BANK OF AMERICA", "WELLS FARGO"], id="topic", value=None, clearable=False),
    dcc.Markdown(children="", id="answer-placeholder")
]

@callback(
  Output("answer-placeholder", "children"),
  Input("topic", "value"),
)
def activate_agent(bank_chosen):
    if bank_chosen is None:
        return no_update
    else:
        task1 = Task(
            description=f"""Conduct a comprehensive analysis of the latest news about {bank_chosen}.
            Identify key trends, investments, loans, acquisitions, or holdings. Research how macroeconomic 
            factors, such as interest rates, might impact the bank's performance.""",
            expected_output="Full analysis report in bullet points",
            agent=researcher
        )

        task2 = Task(
            description=f"""Using the insights provided, develop an engaging blog
            post that highlights the latest concerns and projections of {bank_chosen}.
            Support your arguments with key financial metrics.""",
            expected_output="Full blog post in the form of 4 paragraphs",
            agent=writer
        )

        # Instantiate your crew with a sequential process
        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            verbose=True,
            # full_output=True,
            process=Process.sequential  # https://docs.crewai.com/core-concepts/Processes/#assigning-processes-to-a-crew
        )

        # Get your crew to work!
        result = crew.kickoff()
        return result.raw


if __name__ == '__main__':
    app.run_server(debug=False)
