import concurrent.futures
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import moviepy.editor as mp
import streamlit as st
import os

def process_segment(segment_number, audio_file):
    # Step 1: Transcribe Audio
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='en-US')

    # Step 2: Translate Text to Hindi
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi').text

    # Step 3: Text to Hindi Audio
    tts = gTTS(text=translated_text, lang='hi')
    hindi_audio_file = f'hindi_audio_{segment_number}.mp3'
    tts.save(hindi_audio_file)
    return hindi_audio_file

# Streamlit web interface
st.title("Video Translation and Processing")
st.write("This tool processes a video by splitting it into segments, transcribing, translating to Hindi, and merging the segments back into a video.")

# Upload video file
input_video = st.file_uploader("Upload a video file", type=["mp4"])

# Segment duration input
segment_duration = st.number_input("Enter the segment duration (in seconds)", min_value=1, value=30)

if input_video:
    # Process the video
    st.write("Processing... This may take a while.")

    # Save the video file
    input_video_path = "input_video.mp4"  # Save in the current directory
    with open(input_video_path, "wb") as f:
        f.write(input_video.read())

    # Calculate num_segments based on segment_duration
    video = mp.VideoFileClip(input_video_path)
    total_duration = video.duration
    num_segments = int(total_duration / segment_duration) + 1

    # Process audio segments
    output_audio_files = []
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, total_duration)
        segment_video = video.subclip(start_time, end_time)
        segment_audio_file = f'segment_{i}.wav'
        segment_video.audio.write_audiofile(segment_audio_file)
        output_audio_files.append(segment_audio_file)

    # Step 2: Process Segments in Parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_segment, i, audio_file) for i, audio_file in enumerate(output_audio_files)]
        processed_audio_files = [future.result() for future in futures]

    # Step 3: Merge Processed Segments into a Single Video
    output_video_file = 'output_video.mp4'

    # Load the processed audio files and concatenate them
    final_audio = mp.concatenate_audioclips([mp.AudioFileClip(audio_file) for audio_file in processed_audio_files])

    # Set the processed audio as the audio for the input video
    video = mp.VideoFileClip(input_video_path)
    final_video = video.set_audio(final_audio)

    # Write the final video with merged audio to the output file
    final_video.write_videofile(output_video_file, codec='libx264', audio_codec='aac')

    # Clean up temporary files
    for i in range(num_segments):
        os.remove(f'segment_{i}.wav')
        os.remove(processed_audio_files[i])

    st.success('Process completed.')

    # Display the output video and audio files as download links
    # st.markdown('### Download Processed Output')
    # st.write("Download the processed output files:")
    # st.write(" - [Processed Video](output_video.mp4)")
    # st.write(" - [Processed Video](/download_file/output_video.mp4)")
    # for i, audio_file in enumerate(processed_audio_files):
    #     st.write(f" - [Processed Audio Segment {i + 1}](/{audio_file})")

    import base64


    def get_binary_file_downloader_html(bin_file, file_label='File'):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
            return href
        except Exception as e:
            return f"Error generating download link: {e}"


    # Display the output video and audio files as download links
    st.markdown('### Download Processed Output')
    st.write("Download the processed output files:")
    st.write(" - [Processed Video](/download_file/output_video.mp4)")

    # Add download link for processed video
    st.markdown(get_binary_file_downloader_html('output_video.mp4', 'Processed Video'), unsafe_allow_html=True)

    # Add download links for processed audio segments
    for i, audio_file in enumerate(processed_audio_files):
        st.markdown(get_binary_file_downloader_html(audio_file, f'Processed Audio Segment {i + 1}'),
                    unsafe_allow_html=True)

#
# hindi to english
# import concurrent.futures
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import moviepy.editor as mp
# import streamlit as st
# import os
#
# def process_segment(segment_number, audio_file):
#     # Step 1: Transcribe Audio
#     r = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = r.record(source)
#     text = r.recognize_google(audio_data, language='hi-IN')
#
#     # Step 2: Translate Text to Hindi
#     translator = Translator()
#     translated_text = translator.translate(text, src='hi', dest='en').text
#
#     # Step 3: Text to Hindi Audio
#     tts = gTTS(text=translated_text, lang='en')
#     hindi_audio_file = f'hindi_audio_{segment_number}.mp3'
#     tts.save(hindi_audio_file)
#     return hindi_audio_file
#
# # Streamlit web interface
# st.title("Video Translation and Processing")
# st.write("This tool processes a video by splitting it into segments, transcribing, translating to Hindi, and merging the segments back into a video.")
#
# # Upload video file
# input_video = st.file_uploader("Upload a video file", type=["mp4"])
#
# # Segment duration input
# segment_duration = st.number_input("Enter the segment duration (in seconds)", min_value=1, value=30)
#
# if input_video:
#     # Process the video
#     st.write("Processing... This may take a while.")
#
#     # Save the video file
#     input_video_path = "input_video.mp4"  # Save in the current directory
#     with open(input_video_path, "wb") as f:
#         f.write(input_video.read())
#
#     # Calculate num_segments based on segment_duration
#     video = mp.VideoFileClip(input_video_path)
#     total_duration = video.duration
#     num_segments = int(total_duration / segment_duration) + 1
#
#     # Process audio segments
#     output_audio_files = []
#     for i in range(num_segments):
#         start_time = i * segment_duration
#         end_time = min((i + 1) * segment_duration, total_duration)
#         segment_video = video.subclip(start_time, end_time)
#         segment_audio_file = f'segment_{i}.wav'
#         segment_video.audio.write_audiofile(segment_audio_file)
#         output_audio_files.append(segment_audio_file)
#
#     # Step 2: Process Segments in Parallel
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(process_segment, i, audio_file) for i, audio_file in enumerate(output_audio_files)]
#         processed_audio_files = [future.result() for future in futures]
#
#     # Step 3: Merge Processed Segments into a Single Video
#     output_video_file = 'output_video.mp4'
#
#     # Load the processed audio files and concatenate them
#     final_audio = mp.concatenate_audioclips([mp.AudioFileClip(audio_file) for audio_file in processed_audio_files])
#
#     # Set the processed audio as the audio for the input video
#     video = mp.VideoFileClip(input_video_path)
#     final_video = video.set_audio(final_audio)
#
#     # Write the final video with merged audio to the output file
#     final_video.write_videofile(output_video_file, codec='libx264', audio_codec='aac')
#
#     # Clean up temporary files
#     for i in range(num_segments):
#         os.remove(f'segment_{i}.wav')
#         os.remove(processed_audio_files[i])
#
#     st.success('Process completed.')
#
#     # Display the output video and audio files as download links
#     st.markdown('### Download Processed Output')
#     st.write("Download the processed output files:")
#     st.write(" - [Processed Video](output_video.mp4)")
#     for i, audio_file in enumerate(processed_audio_files):
#         st.write(f" - [Processed Audio Segment {i + 1}](/{audio_file})")