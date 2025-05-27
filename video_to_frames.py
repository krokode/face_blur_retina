import os
import subprocess
import sys


def extract_frames(input_video, output_directory):
    """
    Extracts frames from a video file and saves them as JPEG images.

    Args:
        input_video (str): The path to the input video file.
        output_directory (str): The path to the directory where frames will be saved.
    """
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Construct the ffmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            input_video,
            "-qscale:v",
            "2",
            os.path.join(output_directory, "frame_%06d.jpg")
        ]

        # Execute the ffmpeg command
        subprocess.run(ffmpeg_command, check=True, capture_output=True)

        print(
            f"Frames extracted from '{input_video}' to '{output_directory}'.")

    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure it is installed and in your system's PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during frame extraction:")
        print(e.stderr.decode())
        sys.exit(1)
    except OSError as e:
        print(f"Error creating directory '{output_directory}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            f"Usage: python {sys.argv[0]} <input_video_file> <output_directory>")
        sys.exit(1)

    input_video_file = sys.argv[1]
    output_dir = sys.argv[2]

    extract_frames(input_video_file, output_dir)
