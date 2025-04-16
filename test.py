import cv2
from pyzbar.pyzbar import decode

# Initialize the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If the frame is read correctly, ret is True
    if not ret:
        break

    # Decode the QR codes in the frame
    detected_barcodes = decode(frame)
    
    for barcode in detected_barcodes:
        # Get the data from the barcode
        barcode_data = barcode.data.decode('utf-8')
        
        # Draw a rectangle around the detected barcode
        rect_points = barcode.polygon
        if len(rect_points) == 4:
            pts = [tuple(point) for point in rect_points]
            cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Put the decoded data on the frame
        cv2.putText(frame, barcode_data, (barcode.rect[0], barcode.rect[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    # Display the frame with the detected QR codes
    cv2.imshow('QR Code Scanner', frame)

    # Exit the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
