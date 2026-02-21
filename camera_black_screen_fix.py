#!/usr/bin/env python3
"""
Camera Black Screen Diagnostic Tool
"""

import requests
import json

def camera_diagnostic():
    """Comprehensive camera diagnostic test"""
    print("📷 CAMERA BLACK SCREEN DIAGNOSTIC")
    print("=" * 60)
    
    print("\n🔍 COMMON CAUSES OF BLACK CAMERA SCREEN:")
    print("-" * 50)
    
    causes = [
        {
            "issue": "Browser Permission Denied",
            "symptoms": "Black screen, no error, camera LED off",
            "solution": "Click camera icon in address bar, allow permissions",
            "console": "NotAllowedError: Permission denied"
        },
        {
            "issue": "Camera Already in Use",
            "symptoms": "Black screen, camera LED on (another app using it)",
            "solution": "Close other apps using camera (Zoom, Teams, etc.)",
            "console": "NotReadableError: Device in use"
        },
        {
            "issue": "HTTPS Required",
            "symptoms": "Black screen on production, works on localhost",
            "solution": "Use HTTPS in production environment",
            "console": "TypeError: getUserMedia is not secure"
        },
        {
            "issue": "No Camera Device",
            "symptoms": "Black screen, no camera detected",
            "solution": "Connect camera or check device manager",
            "console": "NotFoundError: No device found"
        },
        {
            "issue": "Video Element Not Playing",
            "symptoms": "Stream obtained but video not displaying",
            "solution": "Video element needs user interaction to play",
            "console": "No error, but video.readyState < 2"
        },
        {
            "issue": "Browser Compatibility",
            "symptoms": "Black screen in older browsers",
            "solution": "Update browser or use Chrome/Firefox",
            "console": "TypeError: getUserMedia not defined"
        }
    ]
    
    for i, cause in enumerate(causes, 1):
        print(f"\n{i}. {cause['issue']}")
        print(f"   Symptoms: {cause['symptoms']}")
        print(f"   Solution: {cause['solution']}")
        print(f"   Console: {cause['console']}")
    
    print("\n🛠️ STEP-BY-STEP TROUBLESHOOTING:")
    print("-" * 50)
    
    steps = [
        "1. Open browser developer tools (F12)",
        "2. Go to Console tab",
        "3. Click 'Enable AI Proctor' in your app",
        "4. Click 'Test Camera' button",
        "5. Watch console messages carefully",
        "6. Look for any red error messages",
        "7. Check if camera LED turns on",
        "8. Verify browser permission requests"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🌐 BROWSER-SPECIFIC SOLUTIONS:")
    print("-" * 50)
    
    browsers = {
        "Chrome": [
            "Settings > Privacy > Camera > Allow",
            "Click camera icon in address bar",
            "Clear cache and restart browser"
        ],
        "Firefox": [
            "Options > Privacy & Security > Camera",
            "Check about:config for media permissions",
            "Reset camera permissions in settings"
        ],
        "Edge": [
            "Settings > Privacy > Camera > Allow",
            "Check site permissions",
            "Clear browsing data"
        ],
        "Safari": [
            "Preferences > Websites > Camera > Allow",
            "Safari > Settings > Camera",
            "Reset Safari if needed"
        ]
    }
    
    for browser, solutions in browsers.items():
        print(f"\n📱 {browser}:")
        for solution in solutions:
            print(f"   • {solution}")
    
    print("\n🧪 ADVANCED DEBUGGING:")
    print("-" * 50)
    
    print("Run these commands in browser console:")
    print("\n// Check camera permissions:")
    print("navigator.permissions.query({name: 'camera'})")
    print("\n// List all devices:")
    print("navigator.mediaDevices.enumerateDevices()")
    print("\n// Test camera directly:")
    print("navigator.mediaDevices.getUserMedia({video: true})")
    print("\n// Check current stream:")
    print("stream.getVideoTracks()[0].getSettings()")
    
    print("\n🔧 QUICK FIXES TO TRY:")
    print("-" * 50)
    
    quick_fixes = [
        "Refresh the page and try again",
        "Close other tabs using camera",
        "Restart the browser completely",
        "Try a different browser",
        "Check if camera works in other apps",
        "Update browser to latest version",
        "Disable browser extensions",
        "Check system camera settings",
        "Restart computer if needed"
    ]
    
    for i, fix in enumerate(quick_fixes, 1):
        print(f"{i}. {fix}")
    
    print("\n✅ SUCCESS INDICATORS:")
    print("-" * 50)
    
    success_indicators = [
        "Camera LED turns on",
        "Console shows 'Video playing successfully'",
        "Video dimensions appear in console",
        "Camera feed shows your face",
        "Recording indicator appears",
        "No error messages in console"
    ]
    
    for indicator in success_indicators:
        print(f"   ✅ {indicator}")
    
    print("\n🎯 NEXT STEPS:")
    print("-" * 50)
    print("1. Try the enhanced camera function with multiple configs")
    print("2. Check console for detailed logging")
    print("3. Verify camera permissions in browser settings")
    print("4. Test with different browsers if needed")
    print("5. Contact support if issue persists")

if __name__ == "__main__":
    camera_diagnostic()
