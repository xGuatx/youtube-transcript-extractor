import os
import yt_dlp
import whisper

def download_youtube_audio(url, output_path="audio.mp3"):
    """Download YouTube video and extract audio only."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # Extract audio only
        'audioformat': 'mp3',
        'outtmpl': output_path,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path

def transcribe_audio(file_path, model_size="small"):
    """Transcribe audio to text with Whisper."""
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result["text"]

def main():
    url = input("Enter YouTube video URL: ")

    if "youtube.com" not in url and "youtu.be" not in url:
        print("The provided URL is not a YouTube video.")
        return

    print("Downloading...")
    audio_path = download_youtube_audio(url)

    print("Transcribing...")
    transcription = transcribe_audio(audio_path)

    print("\n--- Transcription ---\n")
    print(transcription)

    # Save text to file
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)

    print("\nTranscription saved to 'transcription.txt'.")

if __name__ == "__main__":
    main()

