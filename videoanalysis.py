import cv2

def detect_faces_video(video_path):
    # Load the pre-trained face detection model from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the video file using the FFMPEG backend
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces and show the number next to each box
        for i, (x, y, w, h) in enumerate(faces, 1):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Person {i}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Display the frame with detected faces
        cv2.imshow('Detected Faces', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace 'path/to/your/video.mp4' with the actual path of your video
    video_path = r"F:\Blurred_Pedestrians__Turin_Italy.mp4"
    detect_faces_video(video_path)
