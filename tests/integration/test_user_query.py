import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.events.request_input import RequestInput
from google.genai import types

from app.agent import root_agent

async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(user_id="test_user", app_name="app")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="app")

    message = types.Content(
        role="user", parts=[types.Part.from_text(text="Build a Lost & Found web application for a university campus.")]
    )

    print("--- Invoking workflow ---")
    async for event in runner.run_async(
        new_message=message,
        user_id="test_user",
        session_id=session.id,
    ):
        if isinstance(event, RequestInput):
            print(f"Workflow paused at RequestInput: {event.interrupt_id} - {event.message}")
            if event.interrupt_id == "approval":
                print("--- Resuming with 'approve' ---")
                async for res_event in runner.run_async(
                    user_id="test_user",
                    session_id=session.id,
                    resume_inputs={"approval": "approve"}
                ):
                    if res_event.content:
                        for part in res_event.content.parts:
                            if part.text:
                                print(f"Resumed Content: {part.text}")
                    if res_event.output:
                        print(f"Resumed Output: {res_event.output}")
        else:
            if event.content:
                for part in event.content.parts:
                    if part.text:
                        print(f"Content: {part.text}")
            if event.output:
                print(f"Output: {event.output}")

if __name__ == "__main__":
    asyncio.run(main())
