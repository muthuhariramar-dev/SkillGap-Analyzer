# 🔍 Camera Black Screen Debug Guide

## 🎯 **Problem Identified**
Camera stream is obtained but video appears black/empty despite no console errors.

## 🔧 **Debugging Steps**

### **Step 1: Test with Direct HTML Page**
1. Open `camera_debug.html` in your browser
2. Click "Start Camera" button
3. Allow camera permissions
4. Check if video appears in the debug page
5. Click "Test Stream" to analyze quality

### **Step 2: Check Browser Console**
Look for these specific messages:
```
✅ Camera API supported
✅ Camera stream obtained
✅ Video source set
✅ Video metadata loaded
✅ Video playing successfully
```

### **Step 3: Analyze Debug Information**
Check these values in the debug page:
- **Video Ready State:** Should be 4 (HAVE_ENOUGH_DATA)
- **Video Width:** Should be > 0 (e.g., 640, 320)
- **Video Height:** Should be > 0 (e.g., 480, 240)
- **Stream Active:** Should be true
- **Stream Tracks:** Should be 1

### **Step 4: Test Stream Quality**
Click "Test Stream" button and check:
- **Average brightness:** Should be > 20
- **Non-black pixels:** Should be > 10%

## 🚨 **Common Issues & Solutions**

### **Issue 1: Camera Permission**
**Symptoms:**
- Permission denied error
- No camera indicator in browser

**Solution:**
1. Click camera icon in address bar
2. Select "Allow" for camera access
3. Refresh the page
4. Try again

### **Issue 2: Camera in Use**
**Symptoms:**
- "Camera in use" error
- Black screen with camera LED on

**Solution:**
1. Close other apps using camera (Zoom, Teams, etc.)
2. Close other browser tabs with camera
3. Restart browser
4. Try again

### **Issue 3: Browser Compatibility**
**Symptoms:**
- Camera API not supported error
- Video element not working

**Solution:**
1. Try Chrome or Firefox
2. Update browser to latest version
3. Try HTTPS instead of HTTP
4. Use localhost instead of IP

### **Issue 4: Hardware Issues**
**Symptoms:**
- No camera found error
- Camera not working in any app

**Solution:**
1. Check camera is connected
2. Test camera in other apps
3. Restart computer
4. Try different camera

## 🛠️ **Advanced Debugging**

### **Check Network Conditions:**
```javascript
// In browser console
navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    const videoDevices = devices.filter(d => d.kind === 'videoinput');
    console.log('Video devices:', videoDevices);
  });
```

### **Test Different Configurations:**
```javascript
// Try basic constraints
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => console.log('Basic config works'))
  .catch(err => console.log('Basic config failed:', err));

// Try specific constraints
navigator.mediaDevices.getUserMedia({ 
  video: { width: 640, height: 480 } 
})
  .then(stream => console.log('Specific config works'))
  .catch(err => console.log('Specific config failed:', err));
```

### **Check Video Element State:**
```javascript
// In browser console
const video = document.querySelector('video');
console.log('Video state:', {
  readyState: video.readyState,
  videoWidth: video.videoWidth,
  videoHeight: video.videoHeight,
  paused: video.paused,
  currentTime: video.currentTime,
  srcObject: video.srcObject
});
```

## 🎯 **React-Specific Issues**

### **Issue: srcObject Not Working**
**Problem:** React may interfere with video element

**Solution:**
```javascript
// Use ref instead of state
const videoRef = useRef(null);

// Set srcObject directly
videoRef.current.srcObject = stream;

// Don't use setState for video
```

### **Issue: useEffect Timing**
**Problem:** Video element not ready when stream is set

**Solution:**
```javascript
// Wait for video element to be ready
useEffect(() => {
  if (videoRef.current && stream) {
    videoRef.current.srcObject = stream;
  }
}, [stream]);
```

### **Issue: Cleanup Problems**
**Problem:** Stream not properly cleaned up

**Solution:**
```javascript
useEffect(() => {
  return () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
  };
}, []);
```

## 📊 **Expected Results**

### **Working Camera Should Show:**
- ✅ Live video feed in debug page
- ✅ Video dimensions > 0
- ✅ Average brightness > 20
- ✅ Non-black pixels > 10%
- ✅ No error messages
- ✅ Ready state = 4

### **Failing Camera Will Show:**
- ❌ Black screen
- ❌ Video dimensions = 0
- ❌ Average brightness < 10
- ❌ Non-black pixels < 5%
- ❌ Error messages in console

## 🚀 **Next Steps**

### **If Debug Page Works:**
- Camera and browser are working
- Issue is in React implementation
- Check useEffect timing and refs

### **If Debug Page Fails:**
- Browser or camera issue
- Fix permissions/hardware first
- Then test React implementation

### **If Both Work:**
- Check backend integration
- Verify frame capture
- Test AI analysis

## 🎉 **Success Criteria**

Camera is working when:
1. Debug page shows live video
2. React app shows live video
3. Frame capture works
4. Backend analysis receives frames
5. AI alerts are generated

**Use the debug page to isolate the issue and fix systematically!** 🔧
