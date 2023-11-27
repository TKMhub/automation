from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

def detect_silence(audio_segment, min_silence_len=500, silence_thresh=-50):
    # 非無音部分を検出
    nonsilent_parts = detect_nonsilent(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    return nonsilent_parts

def cut_video(clip, nonsilent_parts):
    # カットする部分を集める
    clips = []
    for start, end in nonsilent_parts:
        start_time = start / 1000.0  # PyDubはミリ秒単位で時間を扱うため、秒単位に変換
        end_time = end / 1000.0
        if start_time < clip.duration and end_time <= clip.duration:
            subclip = clip.subclip(start_time, end_time)
            clips.append(subclip)

    # クリップを結合
    if clips:
        final_clip = concatenate_videoclips(clips)
        return final_clip
    else:
        return None

def process_video(video_path):
    # ビデオを読み込む
    clip = VideoFileClip(video_path)
    # 音声がない部分を検出
    audio_segment = AudioSegment.from_file(video_path, format="mp4")
    silence_ranges = detect_silence(audio_segment)
    # カットする部分を決定
    cut_ranges = silence_ranges
    # カット
    final_clip = cut_video(clip, silence_ranges)
    # 結果を保存
    if final_clip is not None:
        output_path = os.path.splitext(video_path)[0] + '_cut.mp4'
        # 音声のビットレートを調整し、適切なコーデックを指定
        final_clip.write_videofile(output_path, audio_codec='aac', audio_bitrate='192k', preset='slow', ffmpeg_params=['-crf', '18'])

# ディレクトリ内の全動画ファイルに対して処理を実行
directory = "/Users/tkm/Documents/autoCutMovie"
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if filename.endswith(".mp4") and os.path.isfile(file_path):
        process_video(file_path)