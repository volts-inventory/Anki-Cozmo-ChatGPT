import chatgpt
import pyttsx4
import pycozmo
from pydub import AudioSegment


class Callisto():

    def __init__(self):
        self.engine = pyttsx4.init("nsss")
        self.engine.setProperty('rate',150)
        self.filename = "speech.wav"
        self.cli = pycozmo.connect()
        self.cli.set_volume(10000)
    
    def cozmo_speak(self, text):
        self.engine.save_to_file(text, self.filename)
        self.engine.runAndWait()
        sound = AudioSegment.from_file(self.filename)
        sound = sound.set_frame_rate(22050)                
        sound = sound.set_channels(1)
        sound.export(self.filename, format="wav")

        # A 22 kHz, 16-bit, mono file is required.
        self.cli.play_audio(self.filename)
        self.cli.wait_for(pycozmo.event.EvtAudioCompleted)

    def cozmo_ask_gpt(self, question):
        resp = chatgpt.get_response(question, "asker")
        self.cozmo_speak(resp)

    def get_state(self):
        def on_robot_state(_ , pkt: pycozmo.protocol_encoder.RobotState):
            self.state = pkt
            print(pkt)
        self.cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state, one_shot=True)

    def run(self):
        pass
