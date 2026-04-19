import os
from removebgvideo import RemoveBGVideoClient

client = RemoveBGVideoClient(api_key=os.environ["REMOVEBGVIDEO_API_KEY"])

# 1) Upload local file to /v1/uploads
upload = client.upload("./input.mp4")
video_url = upload["video_url"]

# 2) Create processing job on /v1/jobs
job = client.create_job(
    video_url=video_url,
    model="pro",
    text_prompt="person wearing red jacket",
    bg_type="transparent",
    output_format="webm",
)

# 3) Poll status until completed
result = client.wait_for_completion(job["id"])
print("Output URL:", result.get("output_url"))
