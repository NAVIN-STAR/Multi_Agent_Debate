from app.core.domain.models.turn_context import (
    DebateState,
    Speaker,
    TurnContext,
)


class DebateStateFactory:

    @staticmethod
    def create(
        *,
        topic: str = "Science is good.",
        current_speaker: Speaker = Speaker.OPTIMIST,
        max_rounds: int = 2,
        round_number: int = 1,
        verdict: str | None = None,
    ) -> DebateState:

        turn_context = TurnContext(
            topic=topic,
            round_number=round_number,
        )

        return {
            "turn_context": turn_context,
            "current_speaker": current_speaker,
            "max_rounds": max_rounds,
            "verdict": verdict,
        }