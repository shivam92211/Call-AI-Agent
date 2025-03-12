import os

from dotenv import load_dotenv

from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import TwilioConfig

load_dotenv()

from speller_agent import SpellerAgentConfig

from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizerConfig
from vocode.streaming.synthesizer.eleven_labs_synthesizer import AudioEncoding

BASE_URL = os.environ["BASE_URL"]


async def main():
    config_manager = RedisConfigManager()

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        to_phone=os.environ["TO_PHONE_NUMBER"],
        from_phone=os.environ["FROM_PHONE_NUMBER"],
        config_manager=config_manager,
        agent_config=ChatGPTAgentConfig(
            initial_message=BaseMessage(text="What up"),
            prompt_preamble="Have a pleasant conversation about life",
            generate_responses=True,
            num_check_human_present_times=1,
            goodbye_phrases=["bye", "goodbye", "good bye", "goodbye!", "Please stay on the line", "this call lasted"],
            end_conversation_on_goodbye=True,
            send_filler_audio=True,
            allowed_idle_time_seconds=30,
            interrupt_sensitivity="high",
        ),
        telephony_config=TwilioConfig(
            account_sid=os.environ["TWILIO_ACCOUNT_SID"],
            auth_token=os.environ["TWILIO_AUTH_TOKEN"],
        ),
        synthesizer_config=ElevenLabsSynthesizerConfig.from_telephone_output_device(
                api_key=os.environ["ELEVEN_LABS_API_KEY"],
                voice_id=os.environ["ELEVEN_LABS_VOICE_ID"],
                experimental_websocket=True
        ),
    )

    input("Press enter to start call...")
    await outbound_call.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
