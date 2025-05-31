import os
import sys
import ffmpeg
import shutil


def extract_frames_with_ffmpeg_library(input_video, output_directory):
    """
    Extracts frames from a video file and saves them as JPEG images using ffmpeg-python.

    Args:
        input_video (str): The path to the input video file.
        output_directory (str): The path to the directory where frames will be saved.
    """
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Construct the output path for frames
        output_frame_path = os.path.join(output_directory, "frame_%06d.jpg")

        # Use ffmpeg-python to extract frames
        (
            ffmpeg
            .input(input_video)
            .output(output_frame_path, qscale=2)  # -qscale:v 2
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )

        print(
            f"Frames extracted from '{input_video}' to '{output_directory}'.")

    except ffmpeg.Error as e:
        print(f"Error during frame extraction:")
        # ffmpeg-python's Error object has stdout and stderr attributes
        if e.stdout:
            print(f"STDOUT: {e.stdout.decode('utf8')}")
        if e.stderr:
            print(f"STDERR: {e.stderr.decode('utf8')}")
        sys.exit(1)
    except FileNotFoundError:
        # This typically means the 'ffmpeg' executable itself wasn't found by the library
        print("Error: ffmpeg executable not found. Please ensure it is installed and in your system's PATH.")
        sys.exit(1)
    except OSError as e:
        print(f"Error creating directory '{output_directory}': {e}")
        sys.exit(1)


def rebuild_video_from_blurred_frames_with_ffmpeg_library(BLURRED_FRAMES_DIR, output_video, FPS=30):
    """
    Rebuilds a video from blurred frames stored in a specified directory using ffmpeg-python.

    Args:
        BLURRED_FRAMES_DIR (str): Directory containing the blurred frames.
        FPS (int): Frames per second for the output video.
        OUTPUT_VIDEO (str): The name of the output video file.
    """
    try:
        (
            ffmpeg
            .input(os.path.join(BLURRED_FRAMES_DIR, 'frame_%06d.jpg'), framerate=FPS)
            .output(output_video, c='libx264', crf=18, preset='fast')
            .run(overwrite_output=True)  # overwrite_output is equivalent to -y
        )
        print(f"Blurred Video rebuilt and saved to: {output_video}")
    except ffmpeg.Error as e:
        print(f"Error rebuilding video: {e.stderr.decode('utf8')}")
        raise


def remove_directory(directory):
    """
    Removes a directory and all its contents recursively.

    Args:
        directory (str): The path to the directory to be removed.
    """
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            print(
                f"Directory '{directory}' and its contents removed successfully.")
        except OSError as e:
            print(
                f"Error: Could not remove directory '{directory}'. Reason: {e}")
    else:
        print(f"Directory '{directory}' does not exist.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            f"Usage: python {sys.argv[0]} <input_video_file> <output_directory>")
        sys.exit(1)

    input_video_file = sys.argv[1]
    output_dir = sys.argv[2]

    # extract_frames_with_ffmpeg_library(input_video_file, output_dir)

    # Example usage of rebuilding video from blurred frames
    # rebuild_video_from_blurred_frames_with_ffmpeg_library(
    #     output_dir, "output_blurred_video.mp4", FPS=30)

    # Example usage of removing a directory
    # remove_directory(output_dir)
