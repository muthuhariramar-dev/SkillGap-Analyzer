import React, { useRef, useEffect, useState } from 'react';
import { FaExclamationTriangle } from 'react-icons/fa';
const CameraMonitor = ({ onViolation, isActive }) => {
    const videoRef = useRef(null);
    const [isModelLoaded, setIsModelLoaded] = useState(false);
    const [initializationError, setInitializationError] = useState(null);
    const faceapiRef = useRef(null);
    const streamRef = useRef(null);

    // Load models
    useEffect(() => {
        const loadModels = async () => {
            try {
                const faceapi = await import('../vendor/face-api.min.js');
                faceapiRef.current = faceapi;
                const MODEL_URL = '/models';
                // Only load tinyFaceDetector as it's the only one used and available
                await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);

                setIsModelLoaded(true);
                console.log("FaceAPI models loaded");
            } catch (err) {
                console.error("Error loading FaceAPI models:", err);
                setInitializationError("Failed to load AI models");
            }
        };
        loadModels();
    }, []);

    // Start video stream
    useEffect(() => {
        if (!isActive) return;

        const startVideo = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
                streamRef.current = stream;
            } catch (err) {
                console.error("Error accessing camera:", err);
                onViolation('CAMERA_ACCESS_DENIED');
            }
        };

        startVideo();

        return () => {
            if (streamRef.current) {
                streamRef.current.getTracks().forEach(track => track.stop());
            }
        };
    }, [isActive, onViolation]);

    // Detection loop
    useEffect(() => {
        if (!isModelLoaded || !isActive || !videoRef.current) return;

        let intervalId;
        let violationCount = 0;
        const MAX_VIOLATIONS = 3; // Trigger immediate action after 3 consecutive failures (approx 3-6 sec)

        const startDetection = () => {
            intervalId = setInterval(async () => {
                if (videoRef.current && videoRef.current.readyState === 4) { // HAVE_ENOUGH_DATA
                    try {
                        // Optimization: Ensure video data is ready
                        if (videoRef.current.readyState !== 4) return;

                        const detections = await faceapiRef.current.detectAllFaces(
                            videoRef.current,
                            new faceapiRef.current.TinyFaceDetectorOptions({
                                inputSize: 224, // Optimized resolution
                                scoreThreshold: 0.1 // Increased sensitivity
                            })
                        );

                        // Draw detections for debugging/feedback (optional)
                        // const displaySize = { width: videoRef.current.videoWidth, height: videoRef.current.videoHeight };
                        // faceapi.matchDimensions(canvasRef.current, displaySize);
                        // const resizedDetections = faceapi.resizeResults(detections, displaySize);
                        // canvasRef.current.getContext('2d').clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
                        // faceapi.draw.drawDetections(canvasRef.current, resizedDetections);

                        if (detections.length === 0) {
                            violationCount++;
                            console.warn(`No face detected! (${violationCount})`);
                            if (violationCount >= MAX_VIOLATIONS) {
                                onViolation('FACE_NOT_VISIBLE');
                                violationCount = 0; // Reset or debounce
                            }
                        } else if (detections.length > 1) {
                            violationCount++;
                            console.warn(`Multiple faces detected! (${violationCount})`);
                            if (violationCount >= MAX_VIOLATIONS) {
                                onViolation('MULTIPLE_FACES_DETECTED');
                                violationCount = 0;
                            }
                        } else {
                            // Face detected correctly
                            violationCount = Math.max(0, violationCount - 1); // Decay violation count
                        }
                    } catch (err) {
                        console.error("Detection error:", err);
                    }
                }
            }, 2000); // Check every 2 seconds
        };

        const videoElement = videoRef.current;
        if (!videoElement) return;

        // Ensure video is playing before starting detection
        videoElement.addEventListener('play', startDetection);

        return () => {
            clearInterval(intervalId);
            if (videoElement) {
                videoElement.removeEventListener('play', startDetection);
            }
        };
    }, [isModelLoaded, isActive, onViolation]);

    return (
        <div className="camera-monitor" style={{ position: 'relative', width: '100%', height: '100%', background: '#000' }}>
            <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
            {/* <canvas ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0 }} /> */}
            {initializationError && (
                <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,0.8)', color: 'red' }}>
                    <FaExclamationTriangle /> {initializationError}
                </div>
            )}
            {!isModelLoaded && !initializationError && (
                <div style={{ position: 'absolute', bottom: 10, left: 10, color: 'white', fontSize: '12px' }}>
                    Loading AI Models...
                </div>
            )}
        </div>
    );
};

export default CameraMonitor;
