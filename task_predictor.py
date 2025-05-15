import requests

class TaskPredictor:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3:8b"  # or "qwen2.5-coder:7b"

    def predict(self, event_text):
        prompt = f"Given the calendar event: '{event_text}', suggest a task. Options: Prepare slides, Send birthday wishes, No action needed, Schedule follow-up, Review documents, Send follow-up email. Task:"
        response = requests.post(
            self.api_url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        return response.json()["response"].strip()

# Example usage:
# predictor = TaskPredictor()
# print(predictor.predict("Meeting with client at 2 PM"))