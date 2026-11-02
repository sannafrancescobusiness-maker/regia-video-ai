// estrai <video> <cartella> <tempo:nome> ...  → JPEG alla risoluzione piena, specchiati come nel video (HDR → SDR).
import Foundation
import AVFoundation
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let gen = AVAssetImageGenerator(asset: AVURLAsset(url: URL(fileURLWithPath: a[1])))
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
gen.dynamicRangePolicy = .forceSDR
for arg in a[3...] {
    let p = arg.split(separator: ":"), t = Double(p[0])!, nome = String(p[1])
    let img = try! gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil)
    let ctx = CGContext(data: nil, width: img.width, height: img.height, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.translateBy(x: CGFloat(img.width), y: 0); ctx.scaleBy(x: -1, y: 1)   // specchio orizzontale
    ctx.draw(img, in: CGRect(x: 0, y: 0, width: img.width, height: img.height))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: "\(a[2])/\(nome).jpg") as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.95] as CFDictionary)
    CGImageDestinationFinalize(d)
    print("\(nome).jpg \(img.width)x\(img.height)")
}
