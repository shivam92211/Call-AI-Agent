# Call AI Agent Project

This project sets up a telephony server using FastAPI, Twilio, and various AI services to handle and process phone calls. The project includes features for processing call transcripts, storing them locally in a JSON file, and (optionally) displaying them on a frontend.

## Demo

Watch a quick demo of the project here: [Telephony Agent Demo](https://youtu.be/JVMeyVwa3Yc?si=NJ8LcT0qLrCMR4BE)

## Getting Started

### 1. Clone This Repository

Open your terminal and run:

```bash
git clone https://github.com/shivam92211/Call-AI-Agent.git
cd Call-AI-Agent
```

### 2. Install Prerequisites

Make sure you have the following installed:

- **Docker**  
  Install from the [official Docker site](https://docs.docker.com/get-docker/).

- **Redis**  
  We will run Redis using Docker.

- **Poetry**  
  Install Poetry by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

### 3. Run Redis with Docker

Start a Redis container by running:

```bash
docker run -dp 6379:6379 -it redis/redis-stack:latest
```

This command runs Redis in a container, mapping port 6379 of the container to port 6379 on your machine.

### 4. Install Python Dependencies

With Poetry installed, run the following command to install all required packages:

```bash
poetry install
```

### 5. Set Up Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables. **Do not modify `BASE_URL`**; it is auto-generated via ngrok if not provided.

```dotenv
# OpenAI API Key for accessing OpenAI services (e.g., ChatGPT)
OPENAI_API_KEY=

# LLM model to be used (e.g., GPT-3.5, GPT-4)
LLM_MODEL=

# Twilio configuration: Account SID and Auth Token for telephony services
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=

# Deepgram API Key for speech-to-text functionality
DEEPGRAM_API_KEY=

# Eleven Labs configuration: API Key and Voice ID for voice synthesis
ELEVEN_LABS_API_KEY=
ELEVEN_LABS_VOICE_ID=

# Ngrok authentication token for exposing local servers (if using ngrok)
NGROK_AUTH_TOKEN=

# Base URL for the telephony server; can be auto-generated via ngrok if not provided
BASE_URL=

# Twilio phone numbers: destination and origin phone numbers
TO_PHONE_NUMBER=
FROM_PHONE_NUMBER=
```

### 6. Run the Server

Start the FastAPI server by executing:

```bash
poetry run uvicorn main:app --port 3000
```

Upon starting, you should see a log line similar to:

```
ba1-8a59-bc4c.ngrok-free.app" -> "http://127.0.0.1:3000"
2025-03-12 14:22:12.243 | INFO     | vocode.streaming.telephony.server.base:create_inbound_route:163 - Set up inbound call TwiML at https://329b-2405-201-1-af6-bc40-bba1-8a59-bc4c.ngrok-free.app/inbound_call
```

### 7. Configure Twilio Webhook

1. Log in to your [Twilio Account Dashboard](https://www.twilio.com/console).
2. Navigate to **Develop > Phone Numbers > Manage > Active Numbers**.
3. Select your active phone number.
4. In the **Voice Configuration** section, under "A call comes in", choose **Webhook**.
5. Paste the generated URL from your server (for example, `https://329b-2405-201-1-af6-bc40-bba1-8a59-bc4c.ngrok-free.app/inbound_call`).
6. Save your changes.

### 8. Making a Call

Call your configured Twilio phone number to test the telephony system. The system will answer the call, process the conversation using the ChatGPT agent, and store the call transcript in `transcripts.json`.

---

## Project Structure

- **main.py:** Sets up the FastAPI application, configures telephony server routes, and integrates with ngrok.
- **event_manager.py:** Handles events such as transcript completion and stores transcripts locally.
- **transcripts.json:** A JSON file where call transcripts are stored.
- **.env:** Environment configuration file.

---

## Troubleshooting

- **Docker/Redis Issues:** Ensure Docker is installed and running. Verify Redis is accessible on port 6379.
- **Environment Variables:** Double-check that all required variables in the `.env` file are set correctly.
- **Ngrok Issues:** If BASE_URL is not set, the ngrok tunnel should auto-generate a URL. Verify that the tunnel is active and reachable.
- **Twilio Webhook:** Confirm that the webhook URL in your Twilio configuration matches the generated URL from your server logs.

---

## License

Include your project's license details here.

---

This README should give you a clear roadmap from cloning the repository to configuring Twilio and running your telephony application. Enjoy building your project!

