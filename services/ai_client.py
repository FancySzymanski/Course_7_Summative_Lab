import ollama

class OllamaChatClient:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        self.history.append({"role": "user", "content": prompt.strip()})

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)
            content = self._extract_content(response)
        except Exception as error:
            self.history.pop()   # remove the failed user message
            raise RuntimeError(f"AI service request failed: {error}") from error

        self.history.append({"role": "assistant", "content": content})
        return content

    @staticmethod
    def _extract_content(response):
        """Handle both dict-style and object-style responses."""
        if isinstance(response, dict):
            message = response.get("message")
        else:
            message = getattr(response, "message", None)

        if isinstance(message, dict):
            content = message.get("content")
        else:
            content = getattr(message, "content", None)

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Service returned no usable assistant content.")
        return content

    def reset(self):
        self.history = []

    def message_count(self):
        return len(self.history)

    def get_transcript(self):
        return [message.copy() for message in self.history]