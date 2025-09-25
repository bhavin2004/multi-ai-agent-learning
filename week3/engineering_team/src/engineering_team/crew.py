from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from dotenv import load_dotenv
import os   
load_dotenv(override=True)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # System Architecture Team
    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['system_architect'],
            verbose=True,
        )

    @agent
    def requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_analyst'],
            verbose=True,
        )

    # Development Team
    @agent
    def data_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['data_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @agent
    def core_logic_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['core_logic_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @agent
    def api_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['api_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500, 
            max_retry_limit=3 
        )

    # Quality & Testing Team
    @agent
    def test_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['test_architect'],
            verbose=True,
        )

    @agent
    def unit_test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['unit_test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @agent
    def integration_test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['integration_test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500, 
            max_retry_limit=3 
        )

    # UI/UX Team
    @agent
    def ui_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_designer'],
            verbose=True,
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500, 
            max_retry_limit=3 
        )

    # Documentation & DevOps Team
    @agent
    def documentation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['documentation_engineer'],
            verbose=True,
        )

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'],
            verbose=True,
        )

    # Specialized Engineers
    @agent
    def security_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'],
            verbose=True,
        )

    @agent
    def performance_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_engineer'],
            verbose=True,
        )

    # Phase 1: Analysis and Architecture Tasks
    @task
    def requirements_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_analysis_task']
        )

    @task
    def system_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['system_architecture_task']
        )

    @task
    def test_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_strategy_task']
        )

    @task
    def ui_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['ui_design_task']
        )

    # Phase 2: Core Development Tasks
    @task
    def data_model_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_model_task']
        )

    @task
    def core_logic_task(self) -> Task:
        return Task(
            config=self.tasks_config['core_logic_task']
        )

    @task
    def api_interface_task(self) -> Task:
        return Task(
            config=self.tasks_config['api_interface_task']
        )

    @task
    def main_module_task(self) -> Task:
        return Task(
            config=self.tasks_config['main_module_task']
        )

    # Phase 3: Testing and Quality Assurance Tasks
    @task
    def unit_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['unit_testing_task']
        )

    @task
    def integration_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['integration_testing_task']
        )

    @task
    def security_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_review_task']
        )

    @task
    def performance_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_optimization_task']
        )

    # Phase 4: User Interface and Documentation Tasks
    @task
    def frontend_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_implementation_task']
        )

    @task
    def documentation_task(self) -> Task:
        return Task(
            config=self.tasks_config['documentation_task']
        )

    # Phase 5: Deployment and Operations Tasks
    @task
    def deployment_setup_task(self) -> Task:
        return Task(
            config=self.tasks_config['deployment_setup_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the comprehensive engineering team crew"""
        # ensure memory dir exists
        import os
        os.makedirs("./memory", exist_ok=True)

        # long-term memory (SQLite) - doesn't require OpenAI key
        long_term_mem = LongTermMemory(
            storage=LTMSQLiteStorage(db_path="./memory/long_term_memory_storage.db")
        )

        # try to initialize RAG-based short-term/entity memory, but fall back if embedder fails
        short_term_mem = None
        entity_mem = None
        try:
            short_term_storage = RAGStorage(
                embedder_config={"provider": "openai", "model_name": "text-embedding-3-small"},
                type="short_term",
                path="./memory/",
            )
            short_term_mem = ShortTermMemory(storage=short_term_storage)

            entity_storage = RAGStorage(
                embedder_config={"provider": "openai", "model_name": "text-embedding-3-small"},
                type="short_term",
                path="./memory/",
            )
            entity_mem = EntityMemory(storage=entity_storage)
        except Exception as e:
            print("Warning: RAGStorage initialization failed:", e)
            print("Short-term/entity RAG memory disabled. To enable set OPENAI_API_KEY and install required deps.")

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=True,
            max_rpm=10,
            long_term_memory=long_term_mem,
            short_term_memory=short_term_mem,
            entity_memory=entity_mem,
        )