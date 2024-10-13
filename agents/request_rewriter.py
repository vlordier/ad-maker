from langgraph import Agent


class RequestRewriterAgent(Agent):
    def __init__(self):
        super().__init__()

    def rewrite_request(self, user_input):
        # Transform user input into the expected format
        # Adjust ad duration and platform-specific details
        transformed_input = {
            "ad_theme": user_input.get("ad_theme", "Default Theme"),
            "platform": user_input.get("platform", "TikTok"),
            "ad_duration": min(max(user_input.get("ad_duration", 30), 0), 60),
        }
        return transformed_input
