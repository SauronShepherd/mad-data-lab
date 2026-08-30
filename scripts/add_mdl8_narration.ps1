$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$text = @"
MAD DATA LAB is a collection of data investigations. Every case can require a different analytical path.
Dashboards tell us what the number is. MAD DATA LAB asks why it changed.
Here, Genie acts as the data scientist. It forms competing explanations from curated evidence and makes an initial prediction.
Instead of waiting for another question, Genie chooses the next analytical experiment. Component decomposition shows that version two explains most of the anomaly.
Version two is the strongest lead, so Genie compares its source snapshots: twenty-three modified records, two removed records, and five added records. The net source impact is minus five point nine million euros.
There is a real data-quality warning, but Genie checks magnitude instead of declaring it the cause. The impact is not additive and is insufficient as the primary explanation.
The conclusion is auditable down to changed records, calculation lineage, snapshots, and source.
The formula is ruled out. Version two source changes reconcile to the deviation, and the evidence supports the primary explanation.
We did not ask for an answer. We ran an investigation. That is Genie at the core.
"@
$wav = 'release-report/MDL-8/mdl8-narration.wav'
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('Microsoft Zira Desktop')
$synth.Rate = -2
$synth.Volume = 90
$synth.SetOutputToWaveFile($wav)
$synth.Speak($text)
$synth.Dispose()
ffmpeg -y -i 'release-report/MDL-8/MDL-8-demo.mp4' -i $wav -filter_complex "[1:a]volume=1.0[narr];[0:a]volume=0.24[music];[music][narr]amix=inputs=2:duration=first:dropout_transition=2[a]" -map 0:v:0 -map '[a]' -c:v copy -c:a aac -b:a 160k -shortest 'release-report/MDL-8/MDL-8-demo-narrated.mp4'
ffprobe -v error -show_entries format=duration:stream=width,height,codec_name -of json 'release-report/MDL-8/MDL-8-demo-narrated.mp4' | Set-Content 'release-report/MDL-8/demo-video-narrated-verification.json'
Get-Content 'release-report/MDL-8/demo-video-narrated-verification.json'
