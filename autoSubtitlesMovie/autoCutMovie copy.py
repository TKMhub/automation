from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import speech_recognition as sr
import os

# 音声をテキストに変換する関数
def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        # 音声認識が失敗した場合のエラーハンドリング
        print(f"音声認識に失敗しました: {e}")
        return None

# 字幕を生成して動画に追加する関数
def add_subtitles(video_path, text, subtitle_style):
    # 動画を読み込む
    clip = VideoFileClip(video_path)
    # 字幕クリップを生成する
    subtitle_clip = TextClip(text, **subtitle_style).set_position('bottom').set_duration(clip.duration)
    # 字幕を動画に合成する
    video = CompositeVideoClip([clip, subtitle_clip])
    # 結果を保存
    output_path = os.path.splitext(video_path)[0] + '_subtitled.mp4'
    video.write_videofile(output_path)

def process_video_with_subtitles(video_path, subtitle_style):
    # ビデオの音声を抽出
    audio_path = os.path.splitext(video_path)[0] + '.wav'
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    # 音声をテキストに変換
    text = speech_to_text(audio_path)
    if text:
        # 字幕を動画に追加
        add_subtitles(video_path, text, subtitle_style)

# 字幕のスタイル設定（例）
subtitle_style = {
    'fontsize': 24,
    'color': 'white'
}

# ディレクトリ内の全動画ファイルに対して処理を実行
directory = "/path/to/your/videos"
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if filename.endswith(".mp4") and os.path.isfile(file_path):
        process_video_with_subtitles(file_path, subtitle_style)
