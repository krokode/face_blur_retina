import torch
from retinaface import RetinaFace


def set_default_tensor_type():
    """
    Sets the default tensor type based on CUDA availability.
    """
    if torch.cuda.is_available():
        print("CUDA is available. Setting default tensor type to CUDA FloatTensor.")
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    else:
        torch.set_default_tensor_type('torch.FloatTensor')
        print("CUDA is not available. Using CPU.")


def get_face_coordinates(image_path):
    """
    Detects faces in an image and returns their coordinates.

    Args:
        image_path (str): The path to the image file.

    Returns:
        list: A list of dictionaries containing face coordinates.
    """
    set_default_tensor_type()
    try:
        # Detect faces in the image
        faces = RetinaFace.detect_faces(image_path)

        # Extract coordinates for each detected face
        face_coords = []
        for key in faces.keys():
            face = faces[key]
            coords = face['facial_area']
            face_coords.append({
                'x1': coords[0],
                'y1': coords[1],
                'x2': coords[2],
                'y2': coords[3]
            })

        return face_coords

    except Exception as e:
        print(f"Error detecting faces: {e}")
        return []
