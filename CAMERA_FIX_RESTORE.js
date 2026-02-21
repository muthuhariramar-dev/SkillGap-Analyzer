// Enhanced Camera Implementation - Replace the corrupted startCameraMonitoring function

const startCameraMonitoring = async () => {
  try {
    console.log('📷 Starting enhanced camera monitoring...');
    
    // Check if mediaDevices is available
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('Camera API not supported in this browser');
    }
    
    // Check available devices first
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    console.log('📹 Found ' + videoDevices.length + ' video devices');
    
    if (videoDevices.length === 0) {
      throw new Error('No camera devices found');
    }
    
    // Try multiple camera configurations with enhanced error handling
    const cameraConfigs = [
      {
        video: {
          width: { ideal: 640, max: 1280 },
          height: { ideal: 480, max: 720 },
          facingMode: 'user'
        },
        audio: false
      },
      {
        video: {
          width: { ideal: 320, max: 640 },
          height: { ideal: 240, max: 480 }
        },
        audio: false
      },
      {
        video: true,
        audio: false
      }
    ];
    
    let stream = null;
    let configUsed = null;
    
    // Try each configuration until one works
    for (let i = 0; i < cameraConfigs.length; i++) {
      try {
        console.log(`🎬 Trying camera config ${i + 1}:`, cameraConfigs[i]);
        stream = await navigator.mediaDevices.getUserMedia(cameraConfigs[i]);
        configUsed = i + 1;
        console.log(`✅ Camera config ${configUsed} successful`);
        break;
      } catch (configError) {
        console.warn(`❌ Camera config ${i + 1} failed:`, configError);
        if (i === cameraConfigs.length - 1) {
          throw configError;
        }
      }
    }
    
    if (!stream) {
      throw new Error('Failed to get camera stream with any configuration');
    }
    
    console.log('✅ Camera stream obtained');
    console.log(`📺 Using camera configuration: ${configUsed}`);
    
    // Get video tracks for debugging
    const videoTracks = stream.getVideoTracks();
    if (videoTracks.length > 0) {
      const track = videoTracks[0];
      console.log('🎥 Video track info:', {
        label: track.label,
        enabled: track.enabled,
        muted: track.muted,
        readyState: track.readyState,
        settings: track.getSettings()
      });
    }
    
    streamRef.current = stream;
    
    // Enhanced video element setup with multiple fallback strategies
    if (videoRef.current) {
      const video = videoRef.current;
      
      console.log('📺 Setting up video element...');
      
      // Strategy 1: Direct stream assignment with immediate play
      try {
        // Set stream directly
        video.srcObject = stream;
        
        // Force video to load
        video.load();
        
        // Set video attributes
        video.autoplay = true;
        video.muted = true;
        video.playsInline = true;
        video.controls = false;
        
        console.log('📺 Stream assigned to video element');
        
        // Strategy 2: Wait for metadata and force play
        const waitForMetadata = () => {
          return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
              reject(new Error('Metadata timeout'));
            }, 5000);
            
            video.onloadedmetadata = () => {
              clearTimeout(timeout);
              console.log('🎥 Video metadata loaded');
              console.log('📐 Video dimensions:', {
                videoWidth: video.videoWidth,
                videoHeight: video.videoHeight,
                readyState: video.readyState
              });
              
              // Force play immediately
              video.play().then(() => {
                console.log('✅ Video playing successfully');
                resolve();
              }).catch(playError => {
                console.error('❌ Video play error:', playError);
                
                // Strategy 3: Try muted play
                video.muted = true;
                video.play().then(() => {
                  console.log('✅ Video playing with muted audio');
                  resolve();
                }).catch(mutedError => {
                  console.error('❌ Even muted play failed:', mutedError);
                  
                  // Strategy 4: User interaction fallback
                  console.log('👆 User interaction may be required');
                  reject(mutedError);
                });
              });
            };
            
            video.onerror = (e) => {
              clearTimeout(timeout);
              console.error('❌ Video error during metadata load:', e);
              reject(e);
            };
          });
        };
        
        // Execute the metadata wait strategy
        await waitForMetadata();
        
        // Strategy 5: Verify video is actually playing
        const verifyPlayback = () => {
          setTimeout(() => {
            console.log('🔍 Verifying video playback...');
            console.log('📊 Video verification state:', {
              readyState: video.readyState,
              videoWidth: video.videoWidth,
              videoHeight: video.videoHeight,
              paused: video.paused,
              currentTime: video.currentTime,
              srcObject: video.srcObject !== null
            });
            
            if (video.readyState === 0 || video.videoWidth === 0) {
              console.error('❌ Video verification failed - stream not working');
              
              // Strategy 6: Restart with basic constraints
              console.log('🔄 Attempting stream restart...');
              restartCameraWithBasicConstraints();
            } else {
              console.log('✅ Video verification passed');
              setCameraActive(true);
              addProctorLog(`Camera monitoring started (config ${configUsed})`, 'success');
              
              // Start backend camera analysis
              startCameraAnalysis();
              
              simulateAIDetection('camera');
            }
          }, 1000);
        };
        
        verifyPlayback();
        
      } catch (setupError) {
        console.error('❌ Video setup failed:', setupError);
        throw setupError;
      }
    } else {
      throw new Error('Video element not available');
    }
    
  } catch (error) {
    console.error('❌ Camera access error:', error);
    
    let errorMessage = 'Camera access failed';
    let logMessage = 'Camera monitoring failed';
    
    if (error.name === 'NotAllowedError') {
      errorMessage = 'Camera permission denied by user';
      logMessage = 'User denied camera permission - please allow camera access';
    } else if (error.name === 'NotFoundError') {
      errorMessage = 'No camera device found';
      logMessage = 'No camera device available - please connect a camera';
    } else if (error.name === 'NotReadableError') {
      errorMessage = 'Camera is already in use';
      logMessage = 'Camera already in use - close other apps using camera';
    } else if (error.name === 'OverconstrainedError') {
      errorMessage = 'Camera constraints not supported';
      logMessage = 'Camera does not support required settings';
    } else if (error.name === 'TypeError') {
      errorMessage = 'Camera API not available';
      logMessage = 'Camera not supported in this browser';
    }
    
    setError(errorMessage);
    addProctorLog(logMessage, 'error');
    setCameraActive(false);
  }
};

// Fallback strategy: restart camera with basic constraints
const restartCameraWithBasicConstraints = async () => {
  try {
    console.log('🔄 Restarting camera with basic constraints...');
    
    // Stop current stream
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    
    // Get basic stream
    const basicStream = await navigator.mediaDevices.getUserMedia({ 
      video: true, 
      audio: false 
    });
    
    console.log('✅ Basic stream obtained');
    
    // Update stream reference
    streamRef.current = basicStream;
    
    // Update video element
    if (videoRef.current) {
      videoRef.current.srcObject = basicStream;
      
      // Force play
      videoRef.current.play().then(() => {
        console.log('✅ Basic stream playing successfully');
        setCameraActive(true);
        addProctorLog('Camera restarted with basic constraints', 'success');
        startCameraAnalysis();
      }).catch(playError => {
        console.error('❌ Basic stream play failed:', playError);
        addProctorLog('Camera restart failed - please check browser permissions', 'error');
      });
    }
    
  } catch (restartError) {
    console.error('❌ Camera restart failed:', restartError);
    addProctorLog('Camera restart failed - please refresh the page and try again', 'error');
  }
};

// Please replace the corrupted startCameraMonitoring function in SkillAnalysis.js with this enhanced version
