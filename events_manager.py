# # event_manager.py

# import os
# import typing
# import json
# from vocode.streaming.models.events import Event, EventType
# from vocode.streaming.models.transcript import TranscriptCompleteEvent
# from vocode.streaming.utils import events_manager

# class EventsManager(events_manager.EventsManager):

#     def __init__(self):
#         super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

#     async def handle_event(self, event: Event):
#         if event.type == EventType.TRANSCRIPT_COMPLETE:
#             transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
#             transcript_text = transcript_complete_event.transcript.to_string()

#             # Prepare the transcript data
#             data = {
#                 "conversation_id": transcript_complete_event.conversation_id,
#                 "user_id": 1,  # demo user id
#                 "transcript": transcript_text
#             }

#             # Instead of sending via webhook, store the transcript in a JSON file
#             self.store_transcript_to_file(data)
#             print("Transcript stored successfully.")

#     def store_transcript_to_file(self, data: dict, filename="transcripts.json"):
#         transcripts = []
#         # If the file exists, load existing transcripts
#         if os.path.exists(filename):
#             try:
#                 with open(filename, "r") as file:
#                     transcripts = json.load(file)
#             except json.JSONDecodeError:
#                 transcripts = []
#         # Append the new transcript and write back
#         transcripts.append(data)
#         with open(filename, "w") as file:
#             json.dump(transcripts, file, indent=2)




# event_manager.py

import os
import typing
import json
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from vocode.streaming.utils import events_manager

class EventsManager(events_manager.EventsManager):

    def __init__(self):
        super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

    async def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT_COMPLETE:
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            transcript_text = transcript_complete_event.transcript.to_string()

            # Prepare the transcript data
            data = {
                "conversation_id": transcript_complete_event.conversation_id,
                "user_id": 1,  # demo user id
                "transcript": transcript_text
            }

            # Instead of sending via webhook, store the transcript in a JSON file
            self.store_transcript_to_file(data)
            print("Transcript stored successfully.")

    def store_transcript_to_file(self, data: dict, filename="transcripts.json"):
        transcripts = {}
        # If the file exists, load the existing dictionary of transcripts
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    transcripts = json.load(file)
            except json.JSONDecodeError:
                transcripts = {}
        # Use the conversation_id as the key
        transcripts[data["conversation_id"]] = data
        # Write the updated dictionary back to the file
        with open(filename, "w") as file:
            json.dump(transcripts, file, indent=2)
