import os
from removebgvideo import RemoveBGVideoClient

client = RemoveBGVideoClient(api_key=os.environ["REMOVEBGVIDEO_API_KEY"])

job = client.create_job(
    video_url="https://cdn.example.com/input.mp4",
    model="original",
    bg_type="green",
    output_format="webm",
)

result = client.wait_for_completion(job["id"])
print("Output URL:", result.get("output_url"))
