from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from agencia_noticias.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them


@CrewBase
class AgenciaNoticiasCrew():
	"""AgenciaNoticias crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def assistente(self) -> Agent:
		return Agent(
			config=self.agents_config['assistente'],
			verbose=True
		)

	@agent
	def revisor(self) -> Agent:
		return Agent(
			config=self.agents_config['revisor'],
			verbose=True
		)


	@task
	def preparar_email(self) -> Task:
		return Task(
			config=self.tasks_config['preparar_email'],
			agent=self.assistente()
		)

	@task
	def revisar_email(self) -> Task:
		return Task(
			config=self.tasks_config['revisar_email'],
			agent=self.revisor(),
			output_file='resposta.txt'
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