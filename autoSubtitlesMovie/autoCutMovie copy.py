from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import speech_recognition as sr
import os

# 音声ファイルからテキストへの変換を行う関数
def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        # 音声認識の失敗をキャッチし、エラーメッセージを表示
        print(f"音声認識に失敗しました: {e}")
        return None

# 動画ファイルに字幕を追加する関数
def add_subtitles(video_path, text, subtitle_style):
    clip = VideoFileClip(video_path)
    # 字幕のスタイルを設定し、動画に適用
    subtitle_clip = TextClip(text, fontsize=subtitle_style['fontsize'], color=subtitle_style['color'], size=clip.size).set_position('bottom').set_duration(clip.duration)
    video = CompositeVideoClip([clip, subtitle_clip])
    # 字幕付きの動画を新しいファイルとして保存
    output_path = os.path.splitext(video_path)[0] + '_subtitled.mp4'
    video.write_videofile(output_path)

# 動画ファイルに音声から生成した字幕を追加するプロセスを実行する関数
def process_video_with_subtitles(video_path, subtitle_style):
    audio_path = os.path.splitext(video_path)[0] + '.wav'
    try:
        video = VideoFileClip(video_path)
        # 動画から音声を抽出し、一時的なファイルとして保存
        video.audio.write_audiofile(audio_path)
        # 音声をテキストに変換
        text = speech_to_text(audio_path)
        if text:
            # 字幕を動画に追加
            add_subtitles(video_path, text, subtitle_style)
    except Exception as e:
        # エラー処理
        print(f"エラーが発生しました: {e}")

# 字幕のスタイル設定
subtitle_style = {
    'fontsize': 24,
    'color': 'white'
}

# 指定されたディレクトリ内の全ての動画ファイルに対して処理を実行
directory = "/path/to/your/videos"
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    # MP4ファイルのみを処理
    if filename.endswith(".mp4") and os.path.isfile(file_path):
        process_video_with_subtitles(file_path, subtitle_style)
