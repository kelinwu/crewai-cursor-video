import os
import pandas as pd

from crewai_tools import BaseTool
from googleapiclient.discovery import build


class YoutubeKeywordSearchTool(BaseTool):
    name: str = "Keyword Search on YouTube"
    description: str = (
        "Search for videos on YouTube using the YouTube Data API to return a list of a specific number of videos, "
        "based on the provided keyword query. The argument 'query' takes the provided keyword as an input, "
        "and the argument 'max_result' takes the number of video results to return as an input."
    )

    def _run(self, query: str, max_results: int = 20) -> str:
        youtube = build(serviceName='youtube', version='v3', developerKey=os.getenv("YOUTUBE_API_KEY"))
        search_request = youtube.search().list(
            part="snippet",
            maxResults=max_results,
            q=query,
            type="video"
        )
        search_response = search_request.execute()
        search_items = search_response.get("items", [])

        result_list = [["rank", "video_id", "video_title"]]
        for idx, item in enumerate(search_items):
            result_list.append([
                idx + 1,
                item['id']['videoId'],
                item['snippet']['title']
            ])

        result_df = pd.DataFrame(result_list[1:], columns=result_list[0])

        vid_request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(map(str, list(result_df['video_id'])))
        )
        vid_response = vid_request.execute()
        vid_items = vid_response.get("items", [])

        vid_list = [["video_id", "comment_count", "like_count", "view_count"]]
        for item in vid_items:
            vid_list.append([
                item['id'],
                int(item['statistics']['commentCount']),
                int(item['statistics']['likeCount']),
                int(item['statistics']['viewCount'])
            ])

        vid_df = pd.DataFrame(vid_list[1:], columns=vid_list[0])
        # merge both df
        full_result_df = pd.merge(result_df, vid_df, on='video_id')
        full_result_csv = full_result_df.to_csv(index=False)
        return full_result_csv