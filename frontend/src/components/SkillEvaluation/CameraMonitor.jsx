import React, { useRef, useEffect, useState, useCallback } from 'react';

/**
 * CameraMonitor – Strict AI proctoring using face-api.js.
 * Monitors for: No face (3s), Multiple faces, Covered camera, and Stream stops.
 */
const CameraMonitor = ({ onViolation, active = true }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const streamRef = useRef(null);
    const intervalRef = useRef(null);
    const [status, setStatus] = useState('initializing');
    const [faceDetected, setFaceDetected] = useState(true);
    const modelsLoaded = useRef(false);
    const noFaceFrames = useRef(0);

    // ── Load face-api models ──
    const loadModels = useCallback(async () => {
        try {
            const faceapi = await import('../../vendor/face-api.min.js');
            const MODEL_URL = '/models';
            // Only load tinyFaceDetector as it's the only one used and available
            await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);

            modelsLoaded.current = true;
            return faceapi;
        } catch (err) {
            console.error('[CameraMonitor] models failed:', err);
            return null;
        }
    }, []);

    // ── Start webcam ──
    const startCamera = useCallback(async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 320, height: 240, facingMode: 'user' },
                audio: false,
            });
            streamRef.current = stream;
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                await videoRef.current.play();
            }

            // Monitor track health
            stream.getVideoTracks()[0].onended = () => {
                onViolation('Camera stream stopped unexpectedly');
            };

            setStatus('active');
        } catch (err) {
            console.error('[CameraMonitor] access error:', err);
            setStatus('error');
            // PART 1: Immediate termination if camera denied/fails
            onViolation('Camera access is required for this assessment.');
        }
    }, [onViolation]);

    // ── Black frame detection (Camera Covered) ──
    const checkOcclusion = useCallback(() => {
        if (!videoRef.current || !canvasRef.current) return false;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        if (!ctx) return false;

        ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        let totalBrightness = 0;
        for (let i = 0; i < data.length; i += 4) {
            totalBrightness += (data[i] + data[i + 1] + data[i + 2]) / 3;
        }
        const avgBrightness = totalBrightness / (data.length / 4);

        // If average brightness is extremely low, camera is likely covered
        return avgBrightness < 10;
    }, []);

    // ── Detection loop ──
    const startDetection = useCallback(async (faceapi) => {
        if (!faceapi || !modelsLoaded.current) return;

        intervalRef.current = setInterval(async () => {
            if (!videoRef.current || videoRef.current.paused || videoRef.current.ended) return;

            try {
                // Check if covered
                if (checkOcclusion()) {
                    onViolation('Assessment terminated: Camera hidden or covered.');
                    return;
                }

                // Optimization: Ensure video data is ready
                if (videoRef.current.readyState !== 4) return;

                const detections = await faceapi.detectAllFaces(
                    videoRef.current,
                    new faceapi.TinyFaceDetectorOptions({
                        inputSize: 224, // Increased from 160 for better resolution
                        scoreThreshold: 0.1 // Lowered from 0.4 for higher sensitivity
                    })
                );

                if (detections.length === 0) {
                    noFaceFrames.current += 1;
                    setFaceDetected(false);
                    console.warn(`[CameraMonitor] No face detected. Frame: ${noFaceFrames.current}`);
                    // PART 2: Terminate if face not visible for ~3 seconds (interval is 600ms, 5 frames)
                    if (noFaceFrames.current >= 5) {
                        onViolation('Assessment terminated: Face not detected for more than 3 seconds.');
                    }
                } else if (detections.length > 1) {
                    console.warn(`[CameraMonitor] Multiple faces detected: ${detections.length}`);
                    // PART 2: Terminate immediately if multiple faces
                    onViolation('Assessment terminated: Multiple faces detected.');
                } else {
                    noFaceFrames.current = 0;
                    setFaceDetected(true);
                }

                // Check track status
                const track = streamRef.current?.getVideoTracks()[0];
                if (!track || !track.enabled || track.readyState !== 'live') {
                    onViolation('Assessment terminated: Camera stream became inactive.');
                }

            } catch (err) {
                console.error('Detection loop error:', err);
            }
        }, 600);
    }, [onViolation, checkOcclusion]);

    // ── Lifecycle ──
    useEffect(() => {
        if (!active) return;
        let mounted = true;

        (async () => {
            const faceapi = await loadModels();
            if (!mounted) return;

            if (!faceapi) {
                setStatus('error-models');
                // We still want to see the camera feed even if AI fails, 
                // but we should report the issue.
            }

            await startCamera();

            if (mounted && faceapi && streamRef.current) {
                startDetection(faceapi);
            }
        })();

        return () => {
            mounted = false;
            if (intervalRef.current) clearInterval(intervalRef.current);
            if (streamRef.current) {
                streamRef.current.getTracks().forEach((t) => t.stop());
            }
        };
    }, [active, loadModels, startCamera, startDetection]);

    return (
        <div className="camera-section">
            <h4 className="sidebar-label">📷 LIVE PROCTORING</h4>
            <video ref={videoRef} className="camera-feed" muted playsInline />
            <canvas ref={canvasRef} width="40" height="30" style={{ display: 'none' }} />
            <div className="camera-status">
                <span className={`camera-dot ${faceDetected ? '' : 'warning'}`} />
                {status === 'initializing' && 'Initializing AI Proctoring…'}
                {status === 'active' && (faceDetected || noFaceFrames.current < 2 ? 'AI Monitoring Active' : '⚠ Face missing!')}
                {status === 'error' && 'Camera access denied'}
                {status === 'error-models' && 'AI Model load failure'}
            </div>
        </div>
    );
};

export default CameraMonitor;
