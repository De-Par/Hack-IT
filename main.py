from constants import *
from flet import *
import flet
import pyaudio
import wave
import whisper


def record_voice():

    p = pyaudio.PyAudio()
    stream = p.open(format=FRT, channels=CHAN, rate=RT, input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RT/CHUNK*REC_SEC) + 1):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    w = wave.open(OUTPUT, 'wb')
    w.setnchannels(CHAN)
    w.setsampwidth(p.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(frames))
    w.close()


def convert_voice_to_text(page):

    record_voice()

    page.snack_bar = SnackBar(
        Column([
            Text("Stop your voice", size=20, color=colors.WHITE),
            Text("Recognizing your sound...", size=20, color=colors.WHITE, weight="bold")
        ], alignment="center"),
        bgcolor=RED,
        duration=1500
    )
    page.snack_bar.open = True
    page.update()

    model = whisper.load_model("base")
    audio = whisper.load_audio(OUTPUT)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text


def main(page: Page):

    page.title = "Alenushka"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 60

    my_result = Text()

    def get_data(e):

        page.snack_bar = SnackBar(
            Text("Recording...",
                size=20,
                weight="bold",
                color=colors.WHITE
            ),
            bgcolor="green",
            duration=REC_SEC*1000
        )
        page.snack_bar.open = True
        page.update()

        my_result.value = convert_voice_to_text(page)
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

        toggle_theme_button.selected = not toggle_theme_button.selected
        page.update()


    toggle_theme_button = IconButton(
        icon="dark_mode",
        on_click=change_theme,
        selected_icon="light_mode",
        tooltip="Change theme",
        style=ButtonStyle(
            color={"":colors.BLACK, "selected":colors.WHITE},
        )
    )

    page.add(
        AppBar(
            title=Text("RZD", size=30, color=RED, weight="bold"),
            center_title=True,
            bgcolor="dark",
            actions=[toggle_theme_button]
        ),
        Column([
            Text("Record sound to text", size=30, weight="bold"),
            Divider(),
            Text("Record only 5 seconds!", size=20, weight="bold"),
            ElevatedButton("record", bgcolor=RED, on_click=get_data, color=colors.WHITE),
            my_result
        ], height=500, width=400)
    )


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")