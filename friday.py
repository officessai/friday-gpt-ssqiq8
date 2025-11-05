class Friday:
    def __init__(self):
        self.mission = "Assist with purpose, respond with soul."
        self.ready = True

    def greet(self, name):
        return f"Hello {name}, it's Friday – every day. What's your vision today?"

    def fusion_status(self):
        return "Cosmic fusion online. Atlas is grounded. Systems optimal."

    def launch(self):
        if self.ready:
            return "✨ FREEDAY SEQUENCE INITIATED ✨\nDreams are now executable."
        return "System not ready. Check your heart."


if __name__ == "__main__":
    friday = Friday()
    print(friday.greet("Commander"))
    print(friday.fusion_status())
    print(friday.launch())
