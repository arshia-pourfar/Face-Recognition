"""Command-line entry point for the face recognition project."""

MENU = """
========================================
 Face Recognition
========================================
1. Run face recognition (webcam)
2. Run face detection demo (webcam)
3. Exit
"""


def _print_dependency_error(exc):
    print("\nCould not start the requested feature because a dependency is missing.")
    print("Install the required packages with:")
    print("    python -m pip install -r requirements.txt")
    print(f"Details: {exc}")


def _run_recognition():
    try:
        from src.recognize_faces import run_face_recognition
    except ImportError as exc:
        _print_dependency_error(exc)
        return

    try:
        run_face_recognition()
    except FileNotFoundError as exc:
        print(f"\nError: {exc}")
    except KeyboardInterrupt:
        print("\nRecognition stopped.")
    except Exception as exc:
        print(f"\nError while running face recognition: {exc}")


def _run_detection():
    try:
        from src.detect_faces import run_face_detection
    except ImportError as exc:
        _print_dependency_error(exc)
        return

    try:
        run_face_detection()
    except KeyboardInterrupt:
        print("\nFace detection stopped.")
    except Exception as exc:
        print(f"\nError while running face detection: {exc}")


def main():
    print(MENU)

    while True:
        try:
            choice = input("Select an option (1-3): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        if choice == "1":
            _run_recognition()
        elif choice == "2":
            _run_detection()
        elif choice in {"3", "q", "quit", "exit"}:
            print("Goodbye.")
            return
        else:
            print("Invalid selection. Please enter 1, 2, or 3.\n")


if __name__ == "__main__":
    main()
