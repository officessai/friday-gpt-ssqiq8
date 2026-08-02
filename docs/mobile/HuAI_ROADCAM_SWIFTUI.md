# HuAI RoadCam Preview v0.1

HuAI RoadCam Preview is a native iOS prototype for a camera-preview module built with SwiftUI and AVFoundation.

## Purpose

This module provides a safe camera preview baseline for future Road Cam / HuAI / CPOC Vision Mode experiments.

It is a preview-only prototype:

- no video recording by default
- no automatic upload of frames
- no continuous AI stream
- no hidden background analysis
- camera access only after iOS permission is granted

## Files

```text
/ios/HuAIRoadCam/CameraPreviewView.swift
```

## Camera Mode

The prototype currently uses the back camera:

```swift
position: .back
```

For a front-camera prototype, change it to:

```swift
position: .front
```

## Required iOS Permission

Add this key to the app `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Aplikacja używa kamery do podglądu obrazu i analizy wideo po zgodzie użytkownika.</string>
```

Without this permission text, iOS will block camera access.

## Privacy Baseline

RoadCam must follow this rule:

> The camera may preview. AI may analyze only after explicit user action.

Future AI analysis should use one of these modes:

1. manual snapshot analysis
2. frame every X seconds after user opt-in
3. local-only pre-processing before network calls

Do not ship automatic continuous streaming as a default behavior.

## Future Roadmap

- Add Start / Stop camera controls
- Add Take Snapshot button
- Add Analyze Snapshot button
- Add `AVCaptureVideoDataOutput` for controlled frame capture
- Add a visible privacy notice before camera activation
- Add local frame redaction if people/faces are visible
- Keep all API keys server-side only

## Status

Prototype / documentation baseline.

Not production-ready until integrated into a real Xcode project and tested on device.
