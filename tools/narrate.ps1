Add-Type -AssemblyName System.Speech
$hortaRoot = Split-Path -Parent $PSScriptRoot
$hortaSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$hortaSynth.SelectVoice('Microsoft Maria Desktop')
$hortaSynth.Rate = 0
$hortaSynth.Volume = 95
$hortaScenes = @(
 'Já imaginou colher o tempero do almoço a poucos passos da sua cozinha?',
 'Você pode começar com um vaso, a planta certa e um lugar com luz adequada.',
 'O Horta Infinita reúne guias em PDF para aprender sobre plantio, rega e cuidados.',
 'Comece pelo Essencial e avance no seu ritmo.',
 'Escolha seu acesso a partir de sete reais e noventa centavos.'
)
for ($hortaIndex=0; $hortaIndex -lt $hortaScenes.Count; $hortaIndex++) {
 $hortaWav = Join-Path $hortaRoot ('video\voz-{0}.wav' -f $hortaIndex)
 $hortaSynth.SetOutputToWaveFile($hortaWav)
 $hortaSynth.Speak($hortaScenes[$hortaIndex])
 $hortaSynth.SetOutputToNull()
}
$hortaSynth.Dispose()
Write-Output 'Cinco trechos de narração pt-BR gerados.'
