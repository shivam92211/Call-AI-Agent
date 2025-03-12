# main.py

import os
import sys
from loguru import logger
from pyngrok import ngrok
from fastapi import FastAPI
from dotenv import load_dotenv
from events_manager import EventsManager
from prompt_loader import get_system_prompt
from speller_agent import SpellerAgentFactory
from vocode.logging import configure_pretty_logging
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizerConfig


load_dotenv()
configure_pretty_logging()
app = FastAPI(docs_url=None)
config_manager = RedisConfigManager()


BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth is not None:
        ngrok.set_auth_token(ngrok_auth)
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 3000

    # Open a ngrok tunnel to the dev server
    BASE_URL = ngrok.connect(port).public_url.replace("https://", "")
    logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))

if not BASE_URL:
    raise ValueError("BASE_URL must be set in environment if not using pyngrok")



telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,

    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",

            agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(text="Hello there, what's your name?"),
                prompt_preamble=get_system_prompt(),
                generate_responses=True,
                num_check_human_present_times=1,
                goodbye_phrases=["bye", "goodbye", "good bye", "goodbye!", "Please stay on the line", "this call lasted"],
                end_conversation_on_goodbye=True,
                send_filler_audio=True,
                allowed_idle_time_seconds=30,
                interrupt_sensitivity="high",
            ),

            twilio_config=TwilioConfig(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            ),

            synthesizer_config=ElevenLabsSynthesizerConfig.from_telephone_output_device(
                api_key=os.environ["ELEVEN_LABS_API_KEY"],
                voice_id=os.environ["ELEVEN_LABS_VOICE_ID"],
                experimental_websocket=True
            ),

        )
    ],
    events_manager=EventsManager(),
    agent_factory=SpellerAgentFactory(),
)

app.include_router(telephony_server.get_router())
