from youtubesearchpython import VideosSearch

video = VideosSearch("i really want to stay at your house", limit=1)

result: list = video.result().get("result")
component: dict = result.__getitem__(0)
link: str = component.get("link")

print(link)
