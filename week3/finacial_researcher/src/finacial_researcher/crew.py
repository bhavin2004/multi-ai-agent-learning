from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerplyWebSearchTool


@CrewBase
class FinacialResearcher():
    """Financial Research crew for comprehensive company analysis and investment recommendations"""

    @agent
    def senior_equity_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_equity_researcher'],
            verbose=True,
            tools=[SerplyWebSearchTool()]
        )

    @agent
    def quantitative_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['quantitative_analyst'],
            verbose=True,
            tools=[SerplyWebSearchTool()]
        )

    @agent
    def market_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['market_strategist'],
            verbose=True,
            tools=[SerplyWebSearchTool()]
        )

    @agent
    def esg_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['esg_analyst'],
            verbose=True,
            tools=[SerplyWebSearchTool()]
        )

    @agent
    def credit_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['credit_analyst'],
            verbose=True,
            tools=[SerplyWebSearchTool()]
        )

    @agent
    def sector_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['sector_specialist'],
            verbose=True,
            tools=[SerplyWebSearchTool()]
        )

    @agent
    def portfolio_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['portfolio_manager'],
            verbose=True
        )

    @task
    def fundamental_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['fundamental_analysis_task']
        )

    @task
    def quantitative_risk_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['quantitative_risk_analysis_task']
        )

    @task
    def macroeconomic_market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['macroeconomic_market_analysis_task']
        )

    @task
    def esg_sustainability_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['esg_sustainability_analysis_task']
        )

    @task
    def credit_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['credit_analysis_task']
        )

    @task
    def sector_competitive_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['sector_competitive_analysis_task']
        )

    @task
    def portfolio_investment_decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['portfolio_investment_decision_task'],
            output_file='output/investment_recommendation.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Financial Research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
