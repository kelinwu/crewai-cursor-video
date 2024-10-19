import os
from crewai import Crew, Process
import agentops
from agents import VideoCreatorAgents
from tasks import VideoCreatorTasks
from langchain_openai import ChatOpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def main_run(topic):
    # initialise agentops for monitoring
    agentops.init(os.getenv('AGENTOPS_API_KEY'))

    # create output folder for run
    run_date = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.now())
    run_dir = os.path.join('./runs', f'{run_date}')
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    # Initialise llm
    llm = ChatOpenAI(
        model='gpt-4o-mini',
        api_key=os.getenv('OPENAI_API_KEY')
    )

    agents = VideoCreatorAgents(topic=topic, agent_llm=llm)
    content_research_agent = agents.content_researcher_agent()
    scriptwriting_agent = agents.scriptwriter_agent()
    scene_planning_agent = agents.scene_planner_agent()
    keyword_research_agent = agents.keyword_researcher_agent()
    title_description_writing_agent = agents.title_description_writer_agent()

    tasks = VideoCreatorTasks(topic=topic, output_dir=run_dir)
    content_research_task = tasks.content_researcher_task(agent=content_research_agent)
    scriptwriting_task = tasks.scriptwriter_task(agent=scriptwriting_agent, context=[content_research_task])
    scene_planning_task = tasks.scene_planner_task(agent=scene_planning_agent, context=[scriptwriting_task])
    keyword_research_task = tasks.keyword_researcher_task(agent=keyword_research_agent, context=[scriptwriting_task])
    title_description_writing_task = tasks.title_description_writer_task(
        agent=title_description_writing_agent, context=[scriptwriting_task, keyword_research_task]
    )

    crew = Crew(
        agents=[
            content_research_agent, scriptwriting_agent, scene_planning_agent, keyword_research_agent,
            title_description_writing_agent
        ],
        tasks=[
            content_research_task, scriptwriting_task, scene_planning_task, keyword_research_task,
            title_description_writing_task
        ],
        process=Process.sequential,     # Process.hierarchical <-- use this to try out hierarchical setup
        # manager_llm=llm,  # uncomment to try out hierarchical setup
        output_log_file=os.path.join(run_dir, 'crewlog.txt'),
        verbose=True,
    )
    crew.kickoff()

    # complete agentops session
    agentops.end_session("Success")


if __name__ == "__main__":
    # run crew
    main_run(topic="calculate the monthly savings of a person who earns $70k a year in toronto over 25 years career with raises and compare and contrast people who invest and don't invest")