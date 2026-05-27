import SwiftUI
import AVFoundation

/// SwiftUI wrapper around an AVFoundation camera preview layer.
///
/// Privacy model:
/// - The camera starts only after iOS permission is granted.
/// - This preview does not record video.
/// - This preview does not upload frames.
/// - Future AI analysis should be triggered only by explicit user action.
struct CameraPreviewView: UIViewRepresentable {
    @ObservedObject var cameraManager: CameraManager

    func makeUIView(context: Context) -> UIView {
        let view = UIView(frame: UIScreen.main.bounds)

        cameraManager.previewLayer.frame = view.bounds
        cameraManager.previewLayer.videoGravity = .resizeAspectFill
        view.layer.addSublayer(cameraManager.previewLayer)

        cameraManager.startSession()

        return view
    }

    func updateUIView(_ uiView: UIView, context: Context) {
        cameraManager.previewLayer.frame = uiView.bounds
    }
}

/// Manages camera permission, device input and session lifecycle.
final class CameraManager: ObservableObject {
    @Published var isPermissionGranted = false

    let session = AVCaptureSession()
    let previewLayer: AVCaptureVideoPreviewLayer

    private let sessionQueue = DispatchQueue(label: "huai.roadcam.session", qos: .userInitiated)
    private var isConfigured = false

    init() {
        self.previewLayer = AVCaptureVideoPreviewLayer(session: self.session)
        checkPermission()
    }

    private func checkPermission() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            isPermissionGranted = true
            setupCameraIfNeeded()

        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .video) { [weak self] granted in
                DispatchQueue.main.async {
                    self?.isPermissionGranted = granted
                    if granted {
                        self?.setupCameraIfNeeded()
                    }
                }
            }

        case .denied, .restricted:
            isPermissionGranted = false

        @unknown default:
            isPermissionGranted = false
        }
    }

    private func setupCameraIfNeeded() {
        guard !isConfigured else { return }

        sessionQueue.async { [weak self] in
            guard let self else { return }

            guard let videoDevice = AVCaptureDevice.default(
                .builtInWideAngleCamera,
                for: .video,
                position: .back
            ) else {
                return
            }

            do {
                let videoDeviceInput = try AVCaptureDeviceInput(device: videoDevice)

                self.session.beginConfiguration()

                if self.session.canSetSessionPreset(.hd1920x1080) {
                    self.session.sessionPreset = .hd1920x1080
                }

                if self.session.canAddInput(videoDeviceInput) {
                    self.session.addInput(videoDeviceInput)
                }

                self.session.commitConfiguration()
                self.isConfigured = true
            } catch {
                print("Camera configuration error: \(error.localizedDescription)")
            }
        }
    }

    func startSession() {
        guard isPermissionGranted else { return }

        sessionQueue.async { [weak self] in
            guard let self, !self.session.isRunning else { return }
            self.session.startRunning()
        }
    }

    func stopSession() {
        sessionQueue.async { [weak self] in
            guard let self, self.session.isRunning else { return }
            self.session.stopRunning()
        }
    }
}

struct ContentView: View {
    @StateObject private var cameraManager = CameraManager()

    var body: some View {
        ZStack {
            if cameraManager.isPermissionGranted {
                CameraPreviewView(cameraManager: cameraManager)
                    .ignoresSafeArea()
                    .onDisappear {
                        cameraManager.stopSession()
                    }

                VStack {
                    HStack {
                        Text("ROAD CAM MODE")
                            .font(.caption)
                            .bold()
                            .padding(6)
                            .background(Color.red)
                            .foregroundColor(.white)
                            .cornerRadius(4)

                        Spacer()
                    }
                    .padding(.top, 50)
                    .padding(.horizontal)

                    Spacer()

                    Text("System gotowy do analizy potoku wideo")
                        .font(.footnote)
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.black.opacity(0.6))
                        .cornerRadius(8)
                        .padding(.bottom, 40)
                }
            } else {
                VStack(spacing: 12) {
                    Image(systemName: "camera.badge.ellipsis")
                        .font(.largeTitle)
                        .padding()

                    Text("Aplikacja wymaga uprawnień do kamery.")
                        .font(.headline)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal)

                    Text("Podgląd nie nagrywa i nie wysyła obrazu automatycznie.")
                        .font(.footnote)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal)
                }
            }
        }
    }
}
