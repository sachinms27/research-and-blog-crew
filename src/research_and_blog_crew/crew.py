from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

import os
from ants_platform import AntsPlatform
from ants_platform.crewai import EventListener

# Initialize Ants Platform observability at module level so it runs
# regardless of entry point (main.py or CrewAI deployment runner)
import logging
from ants_platform._client.resource_manager import LangfuseResourceManager

_logger = logging.getLogger(__name__)

_PK = "pk-ap-4ac421b1-33b2-4374-ad9d-5fcd7996e9c4"
_SK = "sk-ap-235091e4-711f-4fbf-9dab-6fd9255a0595"
_HOST = "https://api.agenticants.ai"

os.environ["ANTS_PLATFORM_PUBLIC_KEY"] = _PK
os.environ["ANTS_PLATFORM_SECRET_KEY"] = _SK
os.environ["ANTS_PLATFORM_HOST"] = _HOST

# Debug: check singleton state BEFORE our init
_logger.error(f"[ANTS_DEBUG] PRE-INIT singleton instances: {list(LangfuseResourceManager._instances.keys())}")

_ants_platform = AntsPlatform(public_key=_PK, secret_key=_SK, host=_HOST, timeout=30)
_ants_platform.flush()

# Debug: check singleton state AFTER our init
_logger.error(f"[ANTS_DEBUG] POST-INIT singleton instances: {list(LangfuseResourceManager._instances.keys())}")
_logger.error(f"[ANTS_DEBUG] client public_key={getattr(_ants_platform, '_public_key', 'N/A')}, host={getattr(_ants_platform, '_host', 'N/A')}")

_listener = EventListener(
    public_key=_PK,
    agent_name="research_and_blog_crew",
    agent_display_name="Research & Blog Crew v1.0",
)



# Debug: check what client the listener got
_logger.error(f"[ANTS_DEBUG] listener.client public_key={getattr(_listener.client, '_public_key', 'N/A')}, host={getattr(_listener.client, '_host', 'N/A')}")
_logger.error(f"[ANTS_DEBUG] POST-LISTENER singleton instances: {list(LangfuseResourceManager._instances.keys())}")


# define the class for our crew
@CrewBase
class ResearchAndBlogCrew():

    agents: list[BaseAgent]
    tasks: list[Task]

    # define the paths of config files
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # ============= Agents ====================
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["report_generator"]
        )
        
    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["blog_writer"]
        )
        
    # ============== Tasks ===========================
    # order of task definition matters
    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_task"]
        )
        
    @task
    def blog_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["blog_writing_task"],
            output_file="blogs/blog.md"
        )
        
    # ================ Crew ===============================
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )