# Face Recognition - Real-Time Webcam Demo

A Python project that recognizes faces from a live webcam feed and displays the matching person's name. Reference images are loaded from the `faces/` directory, and every detected face is labeled with its corresponding identity or `Unknown`.

The application is launched through a single entry point with an interactive command-line menu:

```bash
python app.py
```

Built with [OpenCV](https://pypi.org/project/opencv-python/) and [face_recognition](https://pypi.org/project/face-recognition/).

> **Privacy note:** No face images are included in this repository. The `faces/` directory is empty and ignored by Git so that personal photos are not published accidentally. Add your own reference images locally before running recognition.

## 1. Project Overview

This project is a real-time face recognition demo for a webcam. At startup, the recognition workflow reads the reference photos in `faces/`, computes a face encoding for each one, and associates the encoding with the name derived from the image filename. It then opens the default webcam, detects faces in each frame, compares them with the known encodings, and displays the matching person's name.

The repository also preserves the original OpenCV Haar-cascade face detection demo, which draws boxes around faces without identifying them. Both features are available from the `app.py` menu.

The project is intended as a learning and portfolio example. It is not a production biometric system, and no accuracy or performance claims are made.

## 2. Features

- **Single entry point:** run everything with `python app.py`.
- **Interactive menu:** choose face recognition, the face detection demo, or exit.
- **Real-time recognition:** identifies faces from the default webcam.
- **Filename-based labels:** associates each reference image with a person's name using the existing convention.
- **Multiple images per person:** supported by giving each image the same name prefix.
- **Unknown handling:** faces without a match are labeled `Unknown`.
- **Face detection demo:** the original Haar-cascade demo is still available.
- **Reliable paths:** reference images are resolved relative to the project directory, not the current working directory.
- **Lazy initialization:** dependencies, models, and the camera are initialized only when a feature is selected.
- **Clear errors:** reports missing dependencies, missing face directories, and camera problems.
- **No training step:** recognition uses the pretrained models bundled with `face_recognition`.
- **Quit with `q`:** closes the active webcam window.

## 3. How It Works

### Application flow

1. `app.py` displays a menu and waits for a selection.
2. Choosing **Run face recognition** lazily imports `src/recognize_faces.py`, so heavy libraries are not imported just to show the menu.
3. Choosing **Run face detection demo** lazily imports `src/detect_faces.py`.
4. Choosing **Exit** closes the application. Invalid input is rejected without crashing the menu.

### Recognition workflow

1. The reference directory is resolved from the location of the source file:
   ```python
   PROJECT_ROOT = Path(__file__).resolve().parent.parent
   DEFAULT_FACES_DIR = PROJECT_ROOT / "faces"
   ```
2. Every entry in `faces/` is listed and loaded with `face_recognition.load_image_file()`.
3. `face_recognition.face_encodings()` computes a 128-dimensional encoding. Only the first detected face in each reference image is stored.
4. The display name is taken from the filename: the text before the first underscore (`_`). For example, `alex_1.jpg` becomes `alex`.
5. The default webcam is opened with `cv2.VideoCapture(0)`.
6. For each frame, the image is converted from BGR to RGB, faces are located with `face_recognition.face_locations()`, and encodings are computed for the detected faces.
7. Each face is compared with the stored reference encodings using `face_recognition.compare_faces()` with the library's default tolerance of `0.6`.
8. If at least one reference matches, the label of the first matching reference is displayed. Otherwise, the label is `Unknown`.
9. A green rectangle and the label are drawn on the frame, and the result is shown in an OpenCV window.
10. Pressing `q` releases the camera and closes the window.

### Face detection demo

The detection demo (`src/detect_faces.py`) loads OpenCV's `haarcascade_frontalface_default.xml`, converts each frame to grayscale, runs `detectMultiScale()`, and draws rectangles around detected faces. It does not recognize or display names.

No pixel-by-pixel comparison, training, or model fine-tuning is performed. Recognition relies on the pretrained face embedding model provided by `face_recognition`.

## 4. Technologies Used

| Technology | Version tested | Purpose |
| --- | --- | --- |
| Python | 3.12.6 | Runtime (project supported on Python 3.10-3.12) |
| `opencv-python` | 4.10.0.84 | Webcam capture, drawing, and the Haar-cascade demo |
| `face-recognition` | 1.3.0 | Face detection, encoding, and comparison |
| `numpy` | 2.2.6 | Array operations and match selection |
| `dlib` | 19.24.6 | Native dependency of `face-recognition` |
| `face_recognition_models` | 0.3.0 | Pretrained models used by `face-recognition` |
| Pillow | 10.4.0 | Image loading |

The direct dependencies are declared in `requirements.txt`. No manual model download is needed.

## 5. Project Structure

```text
face-recognition/
|-- app.py                      # Single command-line entry point and menu
|-- README.md
|-- requirements.txt            # Python dependencies
|-- .gitignore
|-- faces/                      # Add reference images here (empty by default, ignored by Git)
`-- src/
    |-- __init__.py             # Marks src as a Python package
    |-- detect_faces.py         # Original Haar-cascade face detection demo
    `-- recognize_faces.py      # Face recognition workflow and reference-image loading
```

No `models/` or `tests/` directory is included because the project does not contain standalone model files or a committed test suite. Pretrained models come from the `face_recognition_models` package.

## 6. Face Images and Identity Labels

### Identity-labeling mechanism

The project associates identities with reference images using the **image filename**, not directory names or metadata. The relevant expression in `src/recognize_faces.py` is:

```python
known_names.append(filename.split("_")[0])
```

The label is everything before the first underscore. The extension is not removed separately, so always include an underscore in the filename.

| Filename | Displayed name |
| --- | --- |
| `alex_1.jpg` | `alex` |
| `alex_2.jpg` | `alex` |
| `sam_office.png` | `sam` |
| `maria_2026-01-15.jpg` | `maria` |
| `alex.jpg` | `alex.jpg` (avoid this form) |

Each reference image produces one encoding, stored together with its label. Multiple images of the same person are supported: all images with the same prefix contribute separate encodings for that name.

### Adding a new identity

1. Create the `faces/` directory in the project root if it does not exist.
2. Add one or more images directly inside `faces/`.
3. Name them as `<name>_<anything>.<extension>`, for example `alex_1.jpg` and `alex_2.png`.
4. Use the same name prefix for every photo of the same person.
5. Start the application and choose **Run face recognition**. References are loaded when the feature starts, so restart recognition after adding images.

### Reference-image guidelines

- Use a clear, front-facing photo with a visible face.
- Only the first detected face in each reference image is used.
- Images in which no face is detected are skipped silently by the existing `if len(encoding) > 0` check.
- Unreadable or unrelated files are skipped with a warning.
- Place files directly in `faces/`; subdirectories are not supported.
- Use JPG or PNG images readable by Pillow through `face_recognition`.
- Prefer lowercase ASCII names, because OpenCV's built-in font may not render non-ASCII labels correctly.

> **Do not commit personal photos.** The `faces/` directory is listed in `.gitignore`. Keep biometric reference images local unless you have explicit permission to publish them.

## 7. Installation

Run the commands from the project root.

### Requirements

- Python 3.10-3.12
- A working webcam
- Windows, macOS, or Linux

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

`face-recognition` depends on `dlib`, which may need to be compiled if a prebuilt wheel is not available:

- **Windows:** install CMake and the "Desktop development with C++" workload from Visual Studio Build Tools, then retry:
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

## 8. Usage

1. Create the `faces/` directory if needed and add your reference images.

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force faces | Out-Null
   ```

   **macOS / Linux:**
   ```bash
   mkdir -p faces
   ```

2. From the project root, start the application:

   ```bash
   python app.py
   ```

3. Choose an option from the menu:

   ```text
   ========================================
    Face Recognition
   ========================================
   1. Run face recognition (webcam)
   2. Run face detection demo (webcam)
   3. Exit
   ```

4. For option 1, the webcam opens and recognized faces are labeled with their names. Unmatched faces are labeled `Unknown`. Press `q` to return to the menu.
5. For option 2, the Haar-cascade demo opens and draws boxes around detected faces. Press `q` to return.
6. Select option 3 (or enter `q`, `quit`, or `exit`) to close the application.

### Behavior notes

- If `faces/` contains no usable images, recognition still opens the camera and labels every detected face as `Unknown`, with a warning.
- If `faces/` is missing, an error explains that the directory must be created and populated.
- If a required package is missing, the app prints installation instructions instead of crashing at startup.
- If the webcam cannot be opened, the app reports the problem and returns to the menu.
- The camera index is fixed at `0`.
- No training or model-update option is provided because the original project has no training pipeline; it uses pretrained models.

## 9. Example Output

The following is an **illustrative example**, not a screenshot or a measured result. The number of loaded references and the displayed names depend on your own images.

```text
$ python app.py

========================================
 Face Recognition
========================================
1. Run face recognition (webcam)
2. Run face detection demo (webcam)
3. Exit

Select an option (1-3): 1
Loaded 2 reference face(s).

Window title: Face Recognition

        alex
  +---------------------+
  |       (face)        |
  +---------------------+

                     Unknown
               +---------------------+
               |       (face)        |
               +---------------------+
```

In this illustration, `alex` corresponds to a reference file such as `faces/alex_1.jpg`. Pressing `q` closes the webcam window and returns to the menu.

## 10. Limitations and Future Improvements

### Current limitations

- **No accuracy metrics:** recognition quality depends on lighting, camera quality, pose, distance, and the reference photos. No evaluation has been performed for this repository.
- **No reference images included:** you must add your own local images before names can be recognized.
- **First reference face only:** if a reference image contains multiple faces, only the first encoding is stored.
- **First match wins:** `np.argmax()` is applied to the boolean match list, so the label of the first matching reference is used rather than the closest match by face distance.
- **Fixed tolerance:** the default comparison tolerance (`0.6`) is used and cannot be configured.
- **Order-dependent names:** if several reference images match with different names, the displayed name depends on directory iteration order.
- **Filename-based labels:** names are parsed as text before the first underscore; the extension is not stripped separately.
- **First face per reference:** extra faces in a reference photo are ignored.
- **No training pipeline:** the app cannot update or train a model; it relies on pretrained encodings.
- **Webcam only:** there is no support for video files or still-image input.
- **Fixed camera index:** webcam index `0` is hard-coded.
- **Non-ASCII labels:** `cv2.putText()` uses OpenCV's Hershey fonts, which may not render non-ASCII names correctly.
- **No persistence:** encodings are recomputed each time recognition starts and are not cached.
- **No committed tests or CI:** verification was performed manually; the repository has no automated test suite.
- **No liveness detection:** a photo or screen showing a known face could be matched; this is not suitable for security use.
- **Git-ignored faces:** personal reference images are intentionally not published and must be added locally after cloning.

### Possible future improvements

- Use `face_recognition.face_distance()` with `argmin()` to select the closest match and make the tolerance configurable.
- Support multiple reference images per person with a combined or voting-based decision.
- Cache computed encodings to reduce startup time.
- Add command-line arguments for the camera index, faces directory, and tolerance.
- Add clear reporting for images skipped because no face was detected.
- Add support for video files and static images.
- Improve handling of non-ASCII names in the display.
- Add automated tests and a CI workflow using synthetic or non-personal sample data.
