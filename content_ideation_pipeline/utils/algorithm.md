# Step 1: Ingestion (The Trigger)

email_parser.py uses *imaplib* or *google-api-python-client*.

- **Action**: Connect to [Gmail], search for TO [paragon.automations+ideas@gmail.com.]

- **Extraction**: [Regex] out the Instagram [URL] from the body, capture the sender’s email, and any "user notes" included in the text.

------------------------------------------------------------------------------------------------------------

# Step 2: Content Retrieval
download_service.py takes over.

- **Action**: Use *yt_dlp* with your instagram_cookies.txt to download the audio as an .mp3.

- **Metadata**: Extract the author, caption, and hashtags from the yt_dlp info dict.

# Step 3: Audio Transcription
transcript_service.py sends the file to Groq.

------------------------------------------------------------------------------------------------------------

- **Action**: Send the local .mp3 to the Groq Whisper-large-v3 endpoint.

- **Output**: Returns a raw text transcript of the Reel.

------------------------------------------------------------------------------------------------------------

# Step 4: AI Marketing Analysis
marketing_analysis.py processes the transcript + metadata.

- **Prompting**: Feed the transcript and caption to an LLM.

- **Logic**: Generate the Visual Hook, Auditory Hook, and a Summary specifically tuned for marketing ideation.

------------------------------------------------------------------------------------------------------------

# Step 5: Task Finalization
clickup_service.py hits the ClickUp API.

- **Action**: Create a task in the specified List.

- **Formatting**: Use Markdown to populate the description with the beautiful breakdown of the video analysis, including the original URL and sender info.