import cv2
import numpy as np

# ---------------------------
# MediaPipe Setup (Graceful Fallback)
# ---------------------------
mp_face_mesh = None
mp_drawing = None
HAS_MEDIAPIPE = False

try:
    import mediapipe as mp
    if hasattr(mp, 'solutions'):
        mp_face_mesh = mp.solutions.face_mesh
        mp_drawing = mp.solutions.drawing_utils
        HAS_MEDIAPIPE = True
    else:
        print("MediaPipe 'solutions' module not found. Face mesh overlay will be disabled.")
except Exception as e:
    print(f"Failed to initialize MediaPipe: {e}. Face mesh overlay will be disabled.")


# ---------------------------
# Face Detection (Haar Cascades)
# ---------------------------

def detect_faces(image):
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    return faces


# ---------------------------
# Face Mesh Detection
# ---------------------------

def get_landmarks(image):
    if not HAS_MEDIAPIPE or mp_face_mesh is None:
        return None

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    try:
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5
        ) as face_mesh:
            results = face_mesh.process(rgb)
        return results
    except Exception as e:
        print(f"Error processing face landmarks: {e}")
        return None


# ---------------------------
# Draw Face Mesh
# ---------------------------

def draw_face_mesh(image, results):
    output = image.copy()
    if not HAS_MEDIAPIPE or mp_drawing is None or results is None:
        return output

    try:
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=output,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION
                )
    except Exception as e:
        print(f"Error drawing face mesh: {e}")
        
    return output


# ---------------------------
# Redness Detection
# ---------------------------

def redness_score(image):
    b, g, r = cv2.split(image)
    redness = np.mean(r) - np.mean(g)
    return round(max(redness, 0), 2)


# ---------------------------
# Acne Estimation
# ---------------------------

def acne_estimate(image):
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(
        hsv,
        lower_red,
        upper_red
    )

    spots = cv2.countNonZero(mask)
    return int(spots)


# ---------------------------
# Skin Health Score
# ---------------------------

def calculate_skin_score(
    acne_score,
    redness_score_value
):
    score = 100
    score -= acne_score * 0.01
    score -= redness_score_value * 0.2
    score = max(0, round(score))
    return score


# ---------------------------
# Heatmap Generation
# ---------------------------

def generate_heatmap(image):
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    heatmap = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    return heatmap


# ---------------------------
# Complete Analysis
# ---------------------------

def analyze_skin(image):
    faces = detect_faces(image)
    landmarks = get_landmarks(image)
    redness = redness_score(image)
    acne = acne_estimate(image)
    skin_score = calculate_skin_score(
        acne,
        redness
    )
    heatmap = generate_heatmap(image)

    return {
        "faces": faces,
        "landmarks": landmarks,
        "redness": redness,
        "acne": acne,
        "skin_score": skin_score,
        "heatmap": heatmap
    }