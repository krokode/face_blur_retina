from vid_ffmpeg_to_frames_and_back import *
# from video_to_frames import *
from face_coords import *
import json
from PIL import Image, ImageDraw, ImageFilter


def map_face(input_video, output_directory, bboxes_file, blured_frame_dir):
    """
    Main function to extract frames from a video and detect faces in each frame.

    Args:
       input_video (str): The path to the input video file.
       output_directory (str): The path to the directory where frames will be saved.
    """
    # Extract frames from the video
    # extract_frames(input_video, output_directory)
    extract_frames_with_ffmpeg_library(input_video, output_directory)

    frame_faces = {}

    # Process each frame to detect faces
    with open(bboxes_file, "w", encoding='utf-8') as f:
        for frame_file in sorted(os.listdir(output_directory)):
            if frame_file.endswith('.jpg'):
                frame_path = os.path.join(output_directory, frame_file)
                face_coords = get_face_coordinates(frame_path)
                frame_faces[frame_file] = face_coords
                apply_blur_to_image(
                    frame_path, blured_frame_dir, frame_file, face_coords)
        json.dump(frame_faces, f, indent=4, ensure_ascii=False, default=int)


def apply_blur_to_image(frame_path, BLURRED_FRAMES_DIR, file, coordinates):
    """
    Opens an image, draws red rectangles around specified face coordinates,
    applies a Gaussian blur to the face regions, and saves the modified image.

    Args:
        frame_path (str): The full path to the input image file.
        coordinates (list): A list of lists, where each inner list contains
                            dictionaries with 'x1', 'y1', 'x2', 'y2' keys
                            defining bounding box coordinates for faces.
        file (str): The filename for the output blurred image (e.g., "frame_001.jpg").
        BLURRED_FRAMES_DIR (str): The directory where the blurred image will be saved.
    """
    img = Image.open(frame_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    for box in coordinates:
        x1, y1, x2, y2 = int(box['x1']), int(
            box['y1']), int(box['x2']), int(box['y2'])

        # Draw rectangle around the face (red outline)
        # This is purely for visualization of the detected face boundaries
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        # Apply Gaussian blur to the face region
        # First, crop the specific region of the image
        face_region = img.crop((x1, y1, x2, y2))
        # Then, apply the blur filter to the cropped region
        blurred_face_region = face_region.filter(
            ImageFilter.GaussianBlur(20))
        # Finally, paste the blurred region back onto the original image
        img.paste(blurred_face_region, (x1, y1))

    # Ensure the output directory exists
    os.makedirs(BLURRED_FRAMES_DIR, exist_ok=True)

    # Save the modified image
    output_path = os.path.join(BLURRED_FRAMES_DIR, file)
    img.save(output_path)
    print(f"Blurred image saved to: {output_path}")


def blur_from_bboxes(bboxes_file, output_dir, BLURRED_FRAMES_DIR):
    """
    Applies blur to images based on bounding boxes specified in a JSON file.
    Args:
        bboxes_file (str): The path to the bounding boxes JSON file.
        output_dir (str): The directory containing the original frames.
        BLURRED_FRAMES_DIR (str): The directory where blurred frames will be saved.
    """
    for frame_file, coordinates in open_bboxes_file_per_frame(bboxes_file):
        frame_path = os.path.join(output_dir, frame_file)
        apply_blur_to_image(frame_path, BLURRED_FRAMES_DIR, frame_file,
                            coordinates)


def open_bboxes_file_per_frame(bboxes_file):
    """
    Opens the bounding boxes file and yields data per frame.

    Args:
        bboxes_file (str): The path to the bounding boxes JSON file.

    Yields:
        tuple: A tuple containing:
               - The filename of the frame (str).
               - A list of dictionaries, where each dictionary represents
                 a face bounding box with 'x1', 'y1', 'x2', 'y2' keys.
    """
    with open(bboxes_file, "r", encoding='utf-8') as f:
        bboxes_data = json.load(f)
        for frame_filename, face_bbox_list in bboxes_data.items():
            # face_bbox_list is already a list of dictionaries,
            # so we yield it directly.
            yield frame_filename, face_bbox_list


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(
            f"Usage: python {sys.argv[0]} <input_video_file> <output_directory>")
        sys.exit(1)

    input_video_file = sys.argv[1]
    # Extract the file name without extension
    input_file_name = input_video_file.split("/")[-1].split(".")[0]
    bboxes_file = f"{input_file_name}_bboxes.json"

    output_dir = sys.argv[2]
    BLURRED_FRAMES_DIR = f"blur_{output_dir}"

    OUTPUT_VIDEO = f"{input_file_name}_blurfaces.mp4"

    map_face(input_video_file, output_dir, bboxes_file,
             BLURRED_FRAMES_DIR)
    # blur_from_bboxes(bboxes_file, output_dir, BLURRED_FRAMES_DIR)
    # rebuild_video_from_blurred_frames(
    #     BLURRED_FRAMES_DIR, output_video=OUTPUT_VIDEO)
    rebuild_video_from_blurred_frames_with_ffmpeg_library(
        BLURRED_FRAMES_DIR, OUTPUT_VIDEO, FPS=30)
    # Clean up directories
    remove_directory(BLURRED_FRAMES_DIR)
    remove_directory(output_dir)
