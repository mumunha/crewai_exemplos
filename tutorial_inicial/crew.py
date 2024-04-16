from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from agencia_noticias.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import ScrapeWebsiteTool

# from langchain_community.tools import DuckDuckGoSearchRun
# scrape_tool = DuckDuckGoSearchRun()

from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SerperDevTool
scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

@CrewBase
class AgenciaNoticiasCrew():
	"""AgenciaNoticias crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[
				scrape_tool,
				search_tool,
							],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)
	
	@agent
	def translator(self) -> Agent:
		return Agent(
			config=self.agents_config['translator'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			# output_file='report.md'
		)
	
	@task
	def translate_task(self) -> Task:
		return Task(
			config=self.tasks_config['translate_task'],
			agent=self.translator(),
			output_file='report_ptbr.md'
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the AgenciaNoticias crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)