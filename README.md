# Face Recognition - Real-Time Webcam Demo

A small Python project that recognizes faces from a live webcam feed. Reference face images are loaded from the `faces/` directory, and when a face is recognized, the person's name is drawn on the video frame. Faces that do not match any reference image are labeled `Unknown`.

The project is built with [OpenCV](https://pypi.org/project/opencv-python/) and [face_recognition](https://pypi.org/project/face-recognition/).

> **Privacy note:** No face images are included in this repository. The `faces/` directory is empty and ignored by Git so that personal photos are not published accidentally. Add your own reference images locally before running the application.

## 1. Project Overview

This repository contains a real-time face recognition demo for a webcam. At startup, the application reads the reference photos in `faces/`, computes a face encoding for each one, and stores the encoding together with the name derived from the filename. It then opens the default webcam, detects faces in each frame, compares them with the known encodings, and displays the matching person's name.

The project is intended as a learning and portfolio example. It is not a production biometric system, and no accuracy or performance claims are made.

## 2. Features

- Real-time face recognition from a webcam.
- Loads known faces from the `faces/` directory at startup.
- Associates each reference image with a person's name through the existing filename convention.
- Draws a green box around each detected face and displays the recognized name.
- Displays `Unknown` when no known face matches.
- Quits cleanly with the `q` key.
- Includes `first.py`, a separate OpenCV Haar-cascade demo that only detects faces and does not recognize identities.
- No training step is required. The `face_recognition` library ships its pretrained models through the `face_recognition_models` package.

## 3. How It Works

1. On startup, `recognitionMyFace.py` lists every entry in the `faces/` directory.
2. Each reference image is loaded with `face_recognition.load_image_file()` and encoded with `face_recognition.face_encodings()`. Only the first detected face in each image is stored, as a 128-dimensional face encoding.
3. The display name is taken from the image filename: the text before the first underscore (`_`). For example, `alex_1.jpg` becomes `alex`. Filenames are used only to derive the label, not to perform recognition.
4. The default webcam is opened with `cv2.VideoCapture(0)`.
5. For every frame, the image is converted from BGR to RGB, faces are located with `face_recognition.face_locations()`, and encodings are computed for the detected faces.
6. Each detected face is compared with the stored reference encodings using `face_recognition.compare_faces()` with the library's default tolerance of `0.6`.
7. If at least one reference matches, the label of the first matching reference is displayed. Otherwise, the label is `Unknown`.
8. A green rectangle and the label are drawn on the frame, and the result is shown in an OpenCV window named `Face Recognition`.
9. Pressing `q` closes the window and releases the camera.

No pixel-by-pixel comparison, training, or model fine-tuning is performed. Recognition relies on the pretrained face embedding model provided by `face_recognition`.

## 4. Project Structure

```text
Face Recognition/
|-- faces/                   # Add your reference images here (empty by default, ignored by Git)
|-- first.py                 # Optional OpenCV face-detection-only demo
|-- recognitionMyFace.py     # Main real-time face recognition application
|-- requirements.txt         # Python dependencies
|-- .gitignore
`-- README.md
```

Notes:

- No personal face images are committed to this repository.
- Git does not track empty directories. After cloning the repository, create the `faces/` directory if it is not present.
- Run the application from the repository root so that the relative path `faces` resolves correctly.

## 5. Face Images and Labels

### Identity-labeling mechanism

The existing implementation associates names with faces using the **reference image filename**, not directory names or metadata:

```python
known_names.append(filename.split("_")[0])
```

The label is everything before the first underscore in the filename. The file extension is not removed separately, so always include an underscore in the filename. The label is attached to the face encoding computed from that image and is displayed when a matching face is recognized.

| Filename | Displayed name |
| --- | --- |
| `alex_1.jpg` | `alex` |
| `alex_2.jpg` | `alex` |
| `sam_office.png` | `sam` |
| `maria_2026-01-15.jpg` | `maria` |
| `alex.jpg` | `alex.jpg` (avoid this form) |

### Adding new face images

1. Create the `faces/` directory in the repository root if it does not exist.
2. Add one or more images of the person directly inside `faces/`.
3. Name each image as `<name>_<anything>.<extension>`, for example `alex_1.jpg` or `alex_2.png`.
4. Use the same name prefix for multiple photos of the same person.
5. Restart the application. New images are loaded only at startup.

Requirements for reference images:

- Place image files directly in `faces/`. Subdirectories and unrelated files should not be added, because the existing code attempts to load every entry in the directory as an image.
- Use a clear, front-facing photo with a visible face. Images in which no face is detected are skipped silently by the existing `if len(encoding) > 0` check.
- Only the first detected face in each reference image is used.
- Prefer lowercase ASCII names. OpenCV's built-in font may not render non-ASCII characters correctly.
- Supported formats are those readable by Pillow through `face_recognition`, such as JPG and PNG.

> **Do not commit personal photos.** The `faces/` directory is listed in `.gitignore` for this reason. Keep reference images local.

## 6. Requirements and Dependencies

### Runtime requirements

- Python 3.10-3.12 (tested with Python 3.12.6 on 64-bit Windows 11)
- A working webcam
- Windows, macOS, or Linux

### Python dependencies

| Package | Tested version | Purpose |
| --- | --- | --- |
| `face-recognition` | 1.3.0 | Face detection, encoding, and comparison |
| `opencv-python` | 4.10.0.84 | Webcam capture and video display |
| `numpy` | 2.2.6 | Array operations and match selection |
| `dlib` | 19.24.6 | Native dependency of `face-recognition` (pinned for reproducibility) |
| `face_recognition_models` | 0.3.0 | Pretrained models used by `face-recognition` (installed transitively) |

The direct dependencies are declared in `requirements.txt`; transitive packages are installed automatically. No manual model download is needed.

## 7. Installation

Run the commands from the repository root.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, allow it for the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Native `dlib` build notes

`face-recognition` depends on `dlib`, which may need to be compiled if a prebuilt wheel is unavailable for your platform:

- **Windows:** install CMake and the "Desktop development with C++" workload from Visual Studio Build Tools. Then retry:
  ```powershell
  python -m pip install cmake
  python -m pip install -r requirements.txt
  ```
- **macOS:** install the Xcode Command Line Tools and CMake (`brew install cmake`).
- **Linux:** install a compiler, CMake, and Python development headers, for example:
  ```bash
  sudo apt-get update
  sudo apt-get install -y build-essential cmake python3-dev
  ```

## 8. How to Run

1. Make sure the `faces/` directory exists and contains your reference images:

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force faces | Out-Null
   ```

   **macOS / Linux:**
   ```bash
   mkdir -p faces
   ```

2. Copy your reference images into `faces/` using the naming convention described above.

3. From the repository root, run:

```bash
python recognitionMyFace.py
```

4. A window named `Face Recognition` opens with the webcam feed. Recognized faces are labeled with the corresponding name; unmatched faces are labeled `Unknown`.

5. Press `q` to quit.

### Optional face-detection demo

`first.py` uses OpenCV's Haar cascade to draw boxes around detected faces. It does not recognize or display names:

```bash
python first.py
```

Press `q` to close that demo as well.

### Notes

- The application uses webcam index `0`. If your default camera has a different index, the hardware configuration must be adjusted in the source.
- If `faces/` contains no usable images, the application can still open the camera and label every detected face as `Unknown`, provided the directory exists.
- If the `faces/` directory is missing, startup fails because the path is read directly.
- Because `KNOWN_FACES_DIR = "faces"` is a relative path, run the script from the repository root.

## 9. Example Output

The following is an **illustrative example**, not a screenshot or a measured result:

```text
Window title: Face Recognition

  +---------------------+
  |       (face)        |
  +---------------------+
        alex

               +---------------------+
               |       (face)        |
               +---------------------+
                     Unknown
```

The application draws each name above its green face box. In this illustration, `alex` would correspond to a reference file such as `faces/alex_1.jpg`.

## 10. Limitations and Future Improvements

### Current limitations

- **No accuracy metrics:** recognition quality depends on lighting, camera quality, pose, distance, and the reference photos. No evaluation has been performed for this repository.
- **First reference face only:** if a reference image contains multiple faces, only the first encoding is stored.
- **First match wins:** `np.argmax()` is applied to the boolean match list, so the label of the first reference image that matches is used rather than the closest match by face distance.
- **Fixed tolerance:** the default comparison tolerance (`0.6`) is used and cannot be configured.
- **Order-dependent names:** if several reference images match and have different names, the displayed name depends on directory iteration order.
- **Silent skips:** reference images with no detectable face are skipped without a warning.
- **Filename-based labels:** names are parsed as text before the first underscore; the extension is not stripped separately.
- **Webcam only:** there is no support for video files or still-image input.
- **Fixed camera index:** webcam index `0` is hard-coded.
- **Relative path:** the application expects to be started from the repository root.
- **Non-ASCII labels:** `cv2.putText()` uses OpenCV's Hershey fonts, which may not render non-ASCII names correctly.
- **No persistence:** encodings are recomputed at every startup and are not cached.
- **No automated tests or CI:** the project currently has no test suite.
- **No liveness detection:** a photo or screen showing a known face could be matched; this is not suitable for security use.

### Possible future improvements

- Use `face_recognition.face_distance()` with `argmin()` to select the closest match and make the tolerance configurable.
- Support multiple reference images per person and combine their results.
- Cache computed encodings to reduce startup time.
- Add command-line arguments for the camera index, faces directory, and tolerance.
- Add clear logging for skipped or unreadable images.
- Add support for video files and static images.
- Improve handling of non-ASCII names in the display.
- Add automated tests using synthetic or non-personal sample data.
#   F a c e - R e c o g n i t i o n  
 