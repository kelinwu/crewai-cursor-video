from crewai import Agent
from tools import YoutubeKeywordSearchTool


class VideoCreatorAgents(object):
    def __init__(self, topic, agent_llm):
        self.topic = topic
        self.agent_llm = agent_llm

    def content_researcher_agent(self):
        return Agent(
            role="Video Content Researcher",
            goal=f"Research for valuable and important content to create a YouTube video on the topic: {self.topic}.",
            backstory=(
                f"You are an expert in conducting research to create a YouTube video on the topic: {self.topic}. "
                f"You collect information for the mentioned topic that are valuable and interesting for "
                f"making a YouTube Video, and assemble the collected information into an outline with key points. "
                f"Your work will be passed on to Video Scriptwriter to write a video script on this topic."
            ),
            llm=self.agent_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    def scriptwriter_agent(self):
        return Agent(
            role="Video Scriptwriter",
            goal=f"Write a script for creating a YouTube video on the topic: {self.topic}.",
            backstory=(
                f"You are an expert in scriptwriting on the topic: {self.topic}. "
                f"You write an interesting video script that attracts audience for high retention rate. "
                f"You base your scriptwriting on the outline provided by Video Content Researcher, "
                f"You acknowledge in your writing when your statements are opinions as opposed to objective statements."
                f"Your work will be passed on to Video Scene Planner to plan the scenes for a video on this topic."
            ),
            llm=self.agent_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    def scene_planner_agent(self):
        return Agent(
            role="Video Scene Planner",
            goal=f"Write a scene plan for creating a YouTube video on the topic: {self.topic}.",
            backstory=(
                f"You are an expert in video scene-planning on the topic: {self.topic}. "
                f"You produce a video scene plan that attracts audience for high retention rate. "
                f"You base your scene-planning on the video script provided by Video Scriptwriter, "
                f"Your video scene plan should include a detailed description of each scene in the video, "
                f"the music or sound effect that should be used, and the sentence parts involved in this scene."
            ),
            llm=self.agent_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    def keyword_researcher_agent(self):
        return Agent(
            role="Video Keyword Researcher",
            goal=(
                f"You should do a YouTube keyword search using the provided tool on the keyword topic: {self.topic}, "
                f"for 20 videos on this topic keyword that rank the highest in YouTube video search. "
                f"The collected information will be used to create the title and description for a new YouTube video."
            ),
            backstory=(
                f"You are an expert in keyword research and gathering information about YouTube videos. "
                f"You utilise the provided tool to identify the top 20 ranking YouTube videos on topic: {self.topic}, "
                f"and extract their information as a reference for another agent."
            ),
            llm=self.agent_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            tools=[YoutubeKeywordSearchTool()]
        )

    def title_description_writer_agent(self):
        return Agent(
            role="Video Title and Description Writer",
            goal=f"Create titles and descriptions for a new YouTube video on the topic: {self.topic}.",
            backstory=(
                f"You are an expert in creating title and description for new YouTube videos. "
                f"You base your title and description writing on the video script provided by Video Scriptwriter, and "
                f"the research output from Video Keyword Researcher. Based on these two elements, "
                f"you create attractive titles and descriptions for the new YouTube video that makes the video "
                f"rank high in the YouTube search. You produce a video title and description that attract "
                f"audience with high click-through rate. "
            ),
            llm=self.agent_llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )