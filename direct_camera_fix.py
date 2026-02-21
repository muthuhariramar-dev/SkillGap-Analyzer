#!/usr/bin/env python3
"""
Direct Camera Fix Test
"""

import requests
import json

def direct_camera_fix():
    """Direct solution for black camera issue"""
    print("📷 DIRECT CAMERA FIX TEST")
    print("=" * 50)
    
    print("\n🔍 ROOT CAUSE ANALYSIS:")
    print("-" * 30)
    
    print("The issue is likely one of these:")
    print("1. Browser blocking camera (most common)")
    print("2. Camera permissions not granted properly")
    print("3. Video element not displaying stream")
    print("4. Stream obtained but no actual video data")
    print("5. Camera hardware/driver issues")
    
    print("\n🛠️ IMMEDIATE FIXES TO TRY:")
    print("-" * 30)
    
    fixes = [
        {
            "fix": "Refresh Page Completely",
            "steps": [
                "1. Close browser tab",
                "2. Open new tab",
                "3. Go to localhost:3000",
                "4. Try proctor mode again"
            ]
        },
        {
            "fix": "Check Browser Camera Permissions",
            "steps": [
                "1. Click camera icon in address bar",
                "2. Select 'Allow' for camera",
                "3. Refresh page",
                "4. Try camera again"
            ]
        },
        {
            "fix": "Try Different Browser",
            "steps": [
                "1. Close current browser",
                "2. Open Chrome (latest version)",
                "3. Go to localhost:3000",
                "4. Test camera in proctor mode"
            ]
        },
        {
            "fix": "Check System Camera",
            "steps": [
                "1. Open Windows Camera app",
                "2. Verify camera works there",
                "3. Close Windows Camera",
                "4. Try proctor mode again"
            ]
        },
        {
            "fix": "Clear Browser Data",
            "steps": [
                "1. Clear browser cache and cookies",
                "2. Restart browser",
                "3. Go to localhost:3000",
                "4. Test camera again"
            ]
        }
    ]
    
    for i, fix in enumerate(fixes, 1):
        print(f"\n{i}. {fix['fix']}")
        for step in fix['steps']:
            print(f"   {step}")
    
    print("\n🎯 SPECIFIC BROWSER FIXES:")
    print("-" * 30)
    
    browsers = {
        "Chrome": [
            "1. Go to chrome://settings/content/camera",
            "2. Ensure camera is allowed",
            "3. Clear site data for localhost",
            "4. Restart Chrome"
        ],
        "Firefox": [
            "1. Go to about:preferences#privacy",
            "2. Check camera permissions",
            "3. Clear cache for localhost",
            "4. Restart Firefox"
        ],
        "Edge": [
            "1. Go to edge://settings/content/camera",
            "2. Allow camera access",
            "3. Clear browsing data",
            "4. Restart Edge"
        ]
    }
    
    for browser, steps in browsers.items():
        print(f"\n📱 {browser}:")
        for step in steps:
            print(f"   {step}")
    
    print("\n🔧 TECHNICAL SOLUTION:")
    print("-" * 30)
    
    print("The issue is likely video element not displaying the stream.")
    print("Let's add a direct video element test:")
    
    print("\n// Test in browser console:")
    print("// 1. Check if stream exists")
    print("navigator.mediaDevices.getUserMedia({video: true})")
    print("  .then(stream => {")
    print("    console.log('Stream:', stream);")
    print("    console.log('Video tracks:', stream.getVideoTracks());")
    print("  })")
    print("  .catch(err => console.error('Error:', err));")
    
    print("\n// 2. Test video element directly")
    print("const video = document.createElement('video');")
    print("video.autoplay = true;")
    print("video.muted = true;")
    print("navigator.mediaDevices.getUserMedia({video: true})")
    print("  .then(stream => {")
    print("    video.srcObject = stream;")
    print("    document.body.appendChild(video);")
    print("    console.log('Video element test:', video);")
    print("  });")
    
    print("\n🎯 QUICK TEST:")
    print("-" * 30)
    
    print("1. Open browser console (F12)")
    print("2. Paste this code and press Enter:")
    print("""
navigator.mediaDevices.getUserMedia({video: true})
  .then(stream => {
    console.log('✅ Stream obtained:', stream);
    const video = document.createElement('video');
    video.srcObject = stream;
    video.autoplay = true;
    video.muted = true;
    video.style.width = '320px';
    video.style.height = '240px';
    video.style.border = '2px solid red';
    document.body.appendChild(video);
    console.log('✅ Video element added to page');
  })
  .catch(err => console.error('❌ Error:', err));
    """)
    
    print("3. If you see a red-bordered video, camera works")
    print("4. If you get an error, that's the problem to fix")
    
    print("\n🚀 FINAL SOLUTION:")
    print("-" * 30)
    print("If the test above works, the issue is in the React component.")
    print("If the test fails, the issue is browser/system permissions.")
    
    print("\n✅ WORKING CAMERA SHOULD SHOW:")
    print("• Live video feed in red-bordered box")
    print("• Console shows '✅ Stream obtained'")
    print("• Console shows '✅ Video element added'")
    print("• No permission errors in console")
    
    print("\n❌ NOT WORKING SHOWS:")
    print("• Permission denied error")
    print("• No video element appears")
    print("• Black screen in test video")
    print("• Camera LED stays off")

if __name__ == "__main__":
    direct_camera_fix()
