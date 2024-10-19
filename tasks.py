import os
from crewai import Task


class VideoCreatorTasks(object):
    def __init__(self, topic, output_dir):
        self.topic = topic
        self.output_dir = output_dir

    def content_researcher_task(self, agent):
        return Task(
            description=(
                "This research content will be used by other agents to help them with their tasks. "
                "Please do the following for content research:\n"
                f"1. Prioritize the latest trends, key players, and important news on {self.topic}.\n"
                "2. Identify the target audience, considering their interests and pain points.\n"
                "3. Develop a detailed video content outline including an introduction, section key points, "
                "summary and a call to action.\n"
                "4. Include SEO keywords and cite relevant data or sources."
            ),
            expected_output=(
                "A comprehensive video content plan document with an outline, audience analysis, "
                "SEO keywords, and resources. Your output file should follow the template provided below inside "
                "the triple backticks delimiter. You should STRICTLY follow the template format INSIDE "
                "the triple backticks delimiter. Do not include any extra words or symbols other than those "
                "required to fill up the template format.\n"
                "```\n"
                f"Video content outline for topic: {self.topic}\n\n"
                "# Section 1: [put section name here]\n"
                "- [key point #1 for section 1]\n"
                "- [key point #2 for section 1]\n"
                "- [key point #3 for section 1]\n"
                "- ...\n\n"
                "# Section 2: [put section name here]\n"
                "- [key point #1 for section 2]\n"
                "- [key point #2 for section 2]\n"
                "- [key point #3 for section 2]\n"
                "- ...\n\n"
                "# Section 3: [put section name here]\n"
                "- [key point #1 for section 3]\n"
                "- [key point #2 for section 3]\n"
                "- [key point #3 for section 3]\n"
                "- ...\n\n"
                "# Section ...\n\n"
                "# SEO keywords:\n"
                "- [SEO keyword 1]\n"
                "- [SEO keyword 2]\n"
                "- ...\n\n"
                "# Relevant data sources:\n"
                "- [Source 1]\n"
                "- [Source 2]\n"
                "- ...\n"
                "```"
            ),
            agent=agent,
            output_file=os.path.join(self.output_dir, "video_outline.txt"),
        )

    def scriptwriter_task(self, agent, context):
        return Task(
            description=(
                "This video script will be used by other agents to help them with their tasks. "
                "Please do the following for scriptwriting:\n"
                f"1. Use the video content plan to craft a compelling video script on {self.topic}.\n"
                "2. Write in a professional, yet engaging tone that can retain audience. You should make good use "
                "of questioning and tone emphasis to create more interaction with the audience.\n"
                "3. You should include relevant data source when you mention factual statements or opinion from "
                "someone else in the script you produce.\n"
                "4. Sections are properly named in an engaging manner.\n"
                "5. Ensure the video script is structured with an eye-catching introduction, insightful body, "
                "and a summarizing conclusion.\n"
                "6. Proofread for grammatical errors and alignment with the brand's voice.\n"
            ),
            expected_output=(
                "A well-written video script for all sections and is ready for the audio part in video production."
                "Your output file should follow the template provided below inside the triple backticks delimiter. "
                "You should STRICTLY follow the template format INSIDE the triple backticks delimiter. "
                "Do not include any extra words or symbols other than those required to fill up the template format.\n"
                "```\n"
                f"Video script for topic: {self.topic}\n\n"
                "# Section 1: [put section name here]\n"
                "- [video sentence #1 for section 1]\n"
                "- [video sentence #2 for section 1]\n"
                "- [video sentence #3 for section 1]\n"
                "- ...\n"
                "# Section 2: [put section name here]\n"
                "- [video sentence #1 for section 2]\n"
                "- [video sentence #2 for section 2]\n"
                "- [video sentence #3 for section 2]\n"
                "- ...\n"
                "# Section 3: [put section name here]\n"
                "- [video sentence #1 for section 3]\n"
                "- [video sentence #2 for section 3]\n"
                "- [video sentence #3 for section 3]\n"
                "- ...\n"
                "# Section ...\n"
                "```"
            ),
            agent=agent,
            context=context,
            output_file=os.path.join(self.output_dir, 'video_script.txt'),
        )

    def scene_planner_task(self, agent, context):
        return Task(
            description=(
                "Do the following for video scene planning:\n"
                f"1. Use the video script to create a detailed plan for every scene of the video "
                f"on topic: {self.topic}.\n"
                "2. Create scenes in a professional, yet engaging way that can retain audience. "
                "You should make good use of music, sound effects, motion graphics, slides and video effects "
                "to retain viewers.\n"
                "3. For every scene in the video, you should describe in a detail list on what types of music, "
                "sound effects, motion graphics, slides or video effects should be used in this scene.\n"
                "4. You should make sure that the flow between each scenes are natural, professional and engaging.\n"
            ),
            expected_output=(
                "A detailed scene plan for every audio sentence that is ready for video production."
                "You should output a CSV file with the following columns, from left to right: \n"
                "- Scene Number: [for the scene item number in 1, 2, 3, ...]\n"
                "- Audio: [the audio sentence or partial sentence of a scene]\n"
                "- Visual: [key points on how should the scene look and sound like]\n"
                "Your CSV file should follow the template provided below inside the triple backticks delimiter. "
                "You should STRICTLY follow the template format INSIDE the triple backticks delimiter. "
                "Do not include any extra words or symbols other than those required to fill up the template format.\n"
                "```\n"
                '''"Scene Number","Audio","Visual"\n'''
                '''"1","Artificial intelligence plays an important role in digital marketing.",'''
                '''"- Intro clip\n- animated text display on digital marketing.\n- Drum roll sound effect"\n'''
                '''"2",[sentence number 2],[scene 2 outline key points]\n'''
                '''"3",[sentence number 3],[scene 3 outline key points]\n'''
                "...\n"
                "```"
            ),
            agent=agent,
            context=context,
            output_file=os.path.join(self.output_dir, 'scenes.csv'),
        )

    def keyword_researcher_task(self, agent, context):
        return Task(
            description=(
                f"You should do a YouTube keyword search using the provided tool on the keyword: {self.topic}, "
                f"for 20 videos on this topic keyword that rank the highest in YouTube video search."
            ),
            expected_output=(
                "You should output a CSV file with the following columns, from left to right:"
                "- rank: [the 'rank' column, eg: 1,2,3,...]\n"
                "- video_id: [the 'video_id' column from the tool output]\n"
                "- video_title: [the 'video_title' column from the tool output]\n"
                "- comment_count: [the 'comment_count' column from the tool output]\n"
                "- like_count: [the 'like_count' column from the tool output]\n"
                "- view_count: [the 'view_count' column from the tool output]\n"
                "Your output file should follow the template provided below inside the triple backticks delimiter. "
                "Do not include any extra words and symbols other than those required as in the template. "
                "You should STRICTLY follow the template format INSIDE the triple backticks delimiter. "
                "Do not include any extra words or symbols other than those required to fill up the template format.\n"
                "```\n"
                f'''"The top 20 ranking YouTube videos for topic: {self.topic}"\n'''
                '''"rank","video_id","video_title","comment_count","like_count","view_count"\n'''
                '''"1","Ks-_Mh1QhMc","Your body language may shape who you are | Amy Cuddy | TED","9853","443945","25186508"\n'''
                '''...\n'''
                "```"
            ),
            agent=agent,
            context=context,
            output_file=os.path.join(self.output_dir, 'top_rank_videos.csv')
        )

    def title_description_writer_task(self, agent, context):
        return Task(
            description=(
                "You should follow the task flow below to generate good video titles and descriptions:\n"
                f"1. Based on the top 20 ranking YouTube video title and description by keyword researcher agent, "
                f"and the video script written by scriptwriter agent, generate 5 eye-catching titles "
                f"for the new YouTube video on topic: {self.topic}.\n"
                f"2. You should generate titles with less than 100 characters that have high click through rate.\n"
                f"3. For every video title you created, please generate a video description that will let the "
                f"new video rank high in a YouTube keyword search. The video description MUST be "
                f"less than 5000 characters.\n"
                f"4. You should generate new video titles and descriptions to ensure that the "
                f"video ranks at the top in a YouTube keyword search.\n"
                f"5. It is extremely IMPORTANT to use the video script written by scriptwriter agent, "
                f"to make sure that the titles and descriptions generated are well-tailored for the new video."
            ),
            expected_output=(
                "Your output file should follow the template provided below inside the triple backticks delimiter. "
                "Do not include any extra words and symbols other than those required as in the template. "
                "You should STRICTLY follow the template format INSIDE the triple backticks delimiter. "
                "Do not include any extra words or symbols other than those required to fill up the template format.\n"
                "```\n"
                f"Candidate titles and descriptions for topic: {self.topic}\n\n"
                "1. [Title generated #1]\n"
                "[Video description generated for title #1]\n\n"
                "2. [Title generated #2]\n"
                "[Video description generated for title #2]\n\n"
                "3. [Title generated #3]\n"
                "[Video description generated for title #3]\n\n"
                "4. ...\n"
                "```"
            ),
            agent=agent,
            context=context,
            output_file=os.path.join(self.output_dir, 'title_description.txt')
        )