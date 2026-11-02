// provino <lista> <cartella> <colonne> <larghezza_cella> <ritaglio_alto 0-1> <ritaglio_altezza 0-1> <out.jpg> [etichette]
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let nomi = try! String(contentsOfFile: a[1], encoding: .utf8).split(separator: "\n").map(String.init)
let dir = a[2], col = Int(a[3])!, cw = Int(a[4])!, top = Double(a[5])!, hh = Double(a[6])!, out = a[7]
let etichette = a.count > 8 ? a[8].split(separator: "|").map(String.init) : []
func carica(_ p: String) -> CGImage {
    let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil)!
    return CGImageSourceCreateImageAtIndex(s, 0, nil)!
}
let primo = carica(dir + "/" + nomi[0])
let ch = Int(Double(cw) * Double(primo.height) * hh / Double(primo.width))
let pad = 6, righe = (nomi.count + col - 1) / col
let W = col * cw + (col + 1) * pad, H = righe * ch + (righe + 1) * pad
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
ctx.setFillColor(CGColor(gray: 0.08, alpha: 1)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
ctx.interpolationQuality = .high
let font = CTFontCreateWithName("Helvetica-Bold" as CFString, CGFloat(cw) / 7, nil)
for (i, n) in nomi.enumerated() {
    let img = carica(dir + "/" + n)
    let cy = Int(Double(img.height) * top), chh = Int(Double(img.height) * hh)
    let crop = img.cropping(to: CGRect(x: 0, y: cy, width: img.width, height: chh))!
    let r = i / col, c = i % col
    let x = pad + c * (cw + pad), y = H - (pad + (r + 1) * ch + r * pad)
    ctx.draw(crop, in: CGRect(x: x, y: y, width: cw, height: ch))
    let testo = i < etichette.count ? etichette[i] : "\(i + 1)"
    let att = NSAttributedString(string: testo, attributes: [kCTFontAttributeName as NSAttributedString.Key: font,
        kCTForegroundColorAttributeName as NSAttributedString.Key: CGColor(red: 1, green: 0.85, blue: 0.1, alpha: 1),
        kCTStrokeColorAttributeName as NSAttributedString.Key: CGColor(gray: 0, alpha: 1),
        kCTStrokeWidthAttributeName as NSAttributedString.Key: -4.0])
    let line = CTLineCreateWithAttributedString(att)
    ctx.textPosition = CGPoint(x: x + 8, y: y + ch - Int(CGFloat(cw) / 7) - 4)
    CTLineDraw(line, ctx)
}
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, ctx.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.9] as CFDictionary)
CGImageDestinationFinalize(d)
print("provino \(W)x\(H)")
