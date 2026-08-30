$ErrorActionPreference = 'Stop'
$outDir = 'release-report/MDL-8'
$list = Join-Path $outDir 'demo-video-input.txt'
$items = @(
  @('desktop-02-case-board.png', 8),
  @('desktop-03-briefing.png', 10),
  @('desktop-04-investigation.png', 16),
  @('desktop-05-experiment-1.png', 28),
  @('desktop-06-experiment-2.png', 29),
  @('desktop-06-experiment-3.png', 21),
  @('desktop-06-experiment-4.png', 20),
  @('desktop-06-experiment-5.png', 20),
  @('desktop-10-verdict.png', 12)
)
$lines = [System.Collections.Generic.List[string]]::new()
foreach ($item in $items) {
  $lines.Add("file 'screenshots/$($item[0])'")
  $lines.Add("duration $($item[1])")
}
$lines.Add("file 'screenshots/$($items[-1][0])'")
[IO.File]::WriteAllLines($list, $lines)
ffmpeg -y -f concat -safe 0 -i $list -stream_loop -1 -i 'dist/audio/mad_data_lab_curiosity.mp3' -t 164 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#08111d,format=yuv420p" -r 30 -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 128k -shortest "$outDir/MDL-8-demo.mp4"
$probe = ffprobe -v error -show_entries format=duration:stream=width,height,codec_name -of json "$outDir/MDL-8-demo.mp4" | ConvertFrom-Json
$probe | ConvertTo-Json -Depth 5 | Set-Content "$outDir/MDL-8-demo-video-verification.json"
Get-Content "$outDir/MDL-8-demo-video-verification.json"
