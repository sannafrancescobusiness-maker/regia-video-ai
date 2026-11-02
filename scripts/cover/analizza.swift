// Analizza i fotogrammi delle clip in camera: qualità del volto (Vision), occhi, bocca, sorriso (CoreImage).
// uso: analizza <video> <clip.json> <passo_s> <cartella_out>
import Foundation
import AVFoundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let video = URL(fileURLWithPath: a[1])
let clips = try! JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: a[2]))) as! [[String: Any]]
let passo = Double(a[3])!
let out = a[4]
try? FileManager.default.createDirectory(atPath: out + "/mini", withIntermediateDirectories: true)

let asset = AVURLAsset(url: video)
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
let ci = CIContext()
let det = CIDetector(ofType: CIDetectorTypeFace, context: ci, options: [CIDetectorAccuracy: CIDetectorAccuracyHigh])!

func box(_ p: [CGPoint]) -> CGRect {
    let xs = p.map { $0.x }, ys = p.map { $0.y }
    return CGRect(x: xs.min()!, y: ys.min()!, width: xs.max()! - xs.min()!, height: ys.max()! - ys.min()!)
}
func salvaMini(_ img: CGImage, _ path: String) {
    let w = 360, h = Int(Double(img.height) * 360.0 / Double(img.width))
    let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.interpolationQuality = .high
    ctx.draw(img, in: CGRect(x: 0, y: 0, width: w, height: h))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.85] as CFDictionary)
    CGImageDestinationFinalize(d)
}

var tempi: [(Double, Double, String)] = []
for c in clips {
    let ms = c["ms"] as! Double, dur = c["dur"] as! Double, st = c["start"] as! Double, id = c["id"] as! String
    var t = 0.08
    while t < dur - 0.08 { tempi.append((ms + t, st + t, id)); t += passo }
}
var righe = ["clip,t_girato,t_finale,qualita,yaw,roll,pitch,occhioS,occhioD,bocca,sorriso,chiusoS,chiusoD,largh,cx,cy"]
for (i, (tg, tf, id)) in tempi.enumerated() {
    guard let img = try? gen.copyCGImage(at: CMTime(seconds: tg, preferredTimescale: 600), actualTime: nil) else { continue }
    let h = VNImageRequestHandler(cgImage: img, options: [:])
    let lm = VNDetectFaceLandmarksRequest()
    let q = VNDetectFaceCaptureQualityRequest()
    try? h.perform([lm, q])
    guard let f = (lm.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { continue }
    let qual = (q.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width })?.faceCaptureQuality ?? -1
    var eS = -1.0, eD = -1.0, bo = -1.0
    if let L = f.landmarks {
        if let e = L.leftEye?.normalizedPoints, e.count > 2 { let b = box(e); eS = Double(b.height / b.width) }
        if let e = L.rightEye?.normalizedPoints, e.count > 2 { let b = box(e); eD = Double(b.height / b.width) }
        if let il = L.innerLips?.normalizedPoints, let ol = L.outerLips?.normalizedPoints, il.count > 2, ol.count > 2 {
            bo = Double(box(il).height / box(ol).width)
        }
    }
    var sor = 0, cS = 0, cD = 0
    if let ff = det.features(in: CIImage(cgImage: img), options: [CIDetectorSmile: true, CIDetectorEyeBlink: true]).first as? CIFaceFeature {
        sor = ff.hasSmile ? 1 : 0; cS = ff.leftEyeClosed ? 1 : 0; cD = ff.rightEyeClosed ? 1 : 0
    }
    let bb = f.boundingBox
    let nome = String(format: "%@_%07.2f", id, tg)
    salvaMini(img, "\(out)/mini/\(nome).jpg")
    righe.append(String(format: "%@,%.3f,%.3f,%.4f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%d,%d,%d,%.3f,%.3f,%.3f", id, tg, tf, qual,
                        f.yaw?.doubleValue ?? 0, f.roll?.doubleValue ?? 0, f.pitch?.doubleValue ?? 0, eS, eD, bo, sor, cS, cD,
                        bb.width, bb.midX, bb.midY))
    if i % 40 == 0 { print("fotogramma \(i + 1)/\(tempi.count) progress \(Int(100.0 * Double(i + 1) / Double(tempi.count)))%"); fflush(stdout) }
}
try! righe.joined(separator: "\n").write(toFile: out + "/punteggi.csv", atomically: true, encoding: .utf8)
print("fatto: \(righe.count - 1) fotogrammi con volto su \(tempi.count)")
