#!/usr/bin/env python3
"""
Camera Debug Helper - Direct Browser Test
"""

import webbrowser
import time

def open_camera_debug_page():
    """Open a direct camera test page in browser"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Debug Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .video-container {
            position: relative;
            width: 100%;
            max-width: 640px;
            margin: 20px auto;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
        }
        video {
            width: 100%;
            height: auto;
            display: block;
        }
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }
        button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .status {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
        }
        .error {
            border-left-color: #dc3545;
            background: #f8d7da;
            color: #721c24;
        }
        .success {
            border-left-color: #28a745;
            background: #d4edda;
            color: #155724;
        }
        .logs {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .debug-info {
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📷 Camera Debug Test</h1>
        <p>This page tests camera functionality directly without React.</p>
        
        <div class="video-container">
            <video id="video" autoplay muted playsinline></video>
        </div>
        
        <div class="controls">
            <button id="startBtn">Start Camera</button>
            <button id="stopBtn" disabled>Stop Camera</button>
            <button id="testBtn">Test Stream</button>
            <button id="clearBtn">Clear Logs</button>
        </div>
        
        <div id="status" class="status">Ready to test camera...</div>
        
        <div class="debug-info">
            <h3>🔍 Debug Information</h3>
            <div id="debugInfo">Click "Start Camera" to begin testing...</div>
        </div>
        
        <div class="logs">
            <div id="logs">Console output will appear here...</div>
        </div>
    </div>

    <script>
        let stream = null;
        const video = document.getElementById('video');
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const testBtn = document.getElementById('testBtn');
        const clearBtn = document.getElementById('clearBtn');
        const status = document.getElementById('status');
        const debugInfo = document.getElementById('debugInfo');
        const logs = document.getElementById('logs');

        function log(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = `[${timestamp}] ${message}\\n`;
            logs.textContent += logEntry;
            logs.scrollTop = logs.scrollHeight;
            console.log(message);
        }

        function updateStatus(message, type = 'info') {
            status.textContent = message;
            status.className = `status ${type}`;
        }

        function updateDebugInfo() {
            const info = {
                'Video Ready State': video.readyState,
                'Video Width': video.videoWidth,
                'Video Height': video.videoHeight,
                'Video Paused': video.paused,
                'Video Current Time': video.currentTime,
                'Video Duration': video.duration,
                'Stream Active': stream !== null,
                'Stream Tracks': stream ? stream.getTracks().length : 0,
                'User Agent': navigator.userAgent,
                'HTTPS': location.protocol === 'https:',
                'Localhost': location.hostname === 'localhost' || location.hostname === '127.0.0.1'
            };
            
            debugInfo.innerHTML = Object.entries(info)
                .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
                .join('<br>');
        }

        async function startCamera() {
            try {
                log('🎬 Starting camera...');
                updateStatus('Requesting camera access...', 'info');
                
                // Check for mediaDevices support
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    throw new Error('Camera API not supported in this browser');
                }
                
                log('✅ Camera API supported');
                
                // Try different configurations
                const configs = [
                    { video: { width: 640, height: 480 }, audio: false },
                    { video: { width: 320, height: 240 }, audio: false },
                    { video: true, audio: false }
                ];
                
                let configUsed = null;
                for (let i = 0; i < configs.length; i++) {
                    try {
                        log(`🎯 Trying config ${i + 1}: ${JSON.stringify(configs[i])}`);
                        stream = await navigator.mediaDevices.getUserMedia(configs[i]);
                        configUsed = i + 1;
                        log(`✅ Config ${configUsed} successful`);
                        break;
                    } catch (configError) {
                        log(`❌ Config ${i + 1} failed: ${configError.message}`);
                        if (i === configs.length - 1) {
                            throw configError;
                        }
                    }
                }
                
                if (!stream) {
                    throw new Error('Failed to get camera stream with any configuration');
                }
                
                log('✅ Camera stream obtained');
                
                // Get video tracks info
                const videoTracks = stream.getVideoTracks();
                if (videoTracks.length > 0) {
                    const track = videoTracks[0];
                    log(`📹 Video track: ${track.label}`);
                    log(`📹 Track enabled: ${track.enabled}`);
                    log(`📹 Track state: ${track.readyState}`);
                }
                
                // Set video source
                video.srcObject = stream;
                log('📺 Video source set');
                
                // Wait for video to load
                video.onloadedmetadata = () => {
                    log('🎥 Video metadata loaded');
                    log(`📐 Video dimensions: ${video.videoWidth}x${video.videoHeight}`);
                    updateDebugInfo();
                    
                    // Try to play
                    video.play().then(() => {
                        log('✅ Video playing successfully');
                        updateStatus('Camera working! Video is playing.', 'success');
                        startBtn.disabled = true;
                        stopBtn.disabled = false;
                        testBtn.disabled = false;
                        updateDebugInfo();
                    }).catch(playError => {
                        log(`❌ Video play error: ${playError.message}`);
                        updateStatus(`Video play error: ${playError.message}`, 'error');
                    });
                };
                
                video.onerror = (e) => {
                    log(`❌ Video error: ${e}`);
                    updateStatus('Video element error', 'error');
                };
                
                updateDebugInfo();
                
            } catch (error) {
                log(`❌ Camera error: ${error.message}`);
                updateStatus(`Camera error: ${error.message}`, 'error');
                
                // Provide specific help
                if (error.name === 'NotAllowedError') {
                    log('🔒 Permission denied - please allow camera access');
                } else if (error.name === 'NotFoundError') {
                    log('📷 No camera found - please connect a camera');
                } else if (error.name === 'NotReadableError') {
                    log('📷 Camera in use - close other apps using camera');
                }
            }
        }

        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
                video.srcObject = null;
                log('🛑 Camera stopped');
                updateStatus('Camera stopped', 'info');
                startBtn.disabled = false;
                stopBtn.disabled = true;
                testBtn.disabled = true;
                updateDebugInfo();
            }
        }

        function testStream() {
            if (!stream) {
                log('❌ No stream to test');
                return;
            }
            
            log('🔍 Testing stream quality...');
            
            // Create canvas for analysis
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;
            const ctx = canvas.getContext('2d');
            
            try {
                // Draw video frame
                ctx.drawImage(video, 0, 0);
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;
                
                // Analyze pixels
                let totalBrightness = 0;
                let nonBlackPixels = 0;
                
                for (let i = 0; i < data.length; i += 4) {
                    const r = data[i];
                    const g = data[i + 1];
                    const b = data[i + 2];
                    const brightness = (r + g + b) / 3;
                    totalBrightness += brightness;
                    
                    if (brightness > 10) {
                        nonBlackPixels++;
                    }
                }
                
                const avgBrightness = totalBrightness / (data.length / 4);
                const nonBlackRatio = nonBlackPixels / (data.length / 4);
                
                log(`📊 Average brightness: ${avgBrightness.toFixed(2)}`);
                log(`📊 Non-black pixels: ${(nonBlackRatio * 100).toFixed(1)}%`);
                
                if (nonBlackRatio > 0.1) {
                    log('✅ Stream has visual content');
                    updateStatus('Stream quality: Good - Visual content detected', 'success');
                } else {
                    log('⚠️ Stream appears to be black or empty');
                    updateStatus('Stream quality: Poor - No visual content detected', 'error');
                }
                
            } catch (error) {
                log(`❌ Stream analysis error: ${error.message}`);
            }
            
            updateDebugInfo();
        }

        function clearLogs() {
            logs.textContent = '';
            log('📝 Logs cleared');
        }

        // Event listeners
        startBtn.addEventListener('click', startCamera);
        stopBtn.addEventListener('click', stopCamera);
        testBtn.addEventListener('click', testStream);
        clearBtn.addEventListener('click', clearLogs);

        // Update debug info every second
        setInterval(updateDebugInfo, 1000);

        // Initial debug info
        updateDebugInfo();
        
        log('🚀 Camera debug page loaded');
        log('📍 Environment: ' + (location.protocol === 'https:' ? 'HTTPS' : 'HTTP'));
        log('🌐 Host: ' + location.hostname);
    </script>
</body>
</html>
    """
    
    # Save HTML file
    with open('camera_debug.html', 'w') as f:
        f.write(html_content)
    
    print("📷 Camera Debug Page Created!")
    print("=" * 50)
    print("📁 File: camera_debug.html")
    print("🌐 Opening in browser...")
    
    # Open in browser
    webbrowser.open('file://' + os.path.abspath('camera_debug.html'))
    
    print("\n🔧 Debug Instructions:")
    print("1. Click 'Start Camera' button")
    print("2. Allow camera permissions")
    print("3. Check if video appears")
    print("4. Click 'Test Stream' to analyze quality")
    print("5. Review debug information")
    
    print("\n📊 What to Look For:")
    print("✅ Video dimensions should be > 0")
    print("✅ Non-black pixels should be > 10%")
    print("✅ Average brightness should be > 20")
    print("✅ No error messages in console")
    
    print("\n🚨 If Still Not Working:")
    print("- Check browser camera permissions")
    print("- Try different browser (Chrome/Firefox)")
    print("- Check if camera is working in other apps")
    print("- Restart browser/computer")

if __name__ == "__main__":
    import os
    open_camera_debug_page()
