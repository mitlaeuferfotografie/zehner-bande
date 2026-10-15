"""Erzeugt die Zahlen-Ansage public/audio/<stimme>/1.mp3 … 100.mp3 und prüft jede Datei mit Vosk.

Voraussetzungen (einmalig):
  pip install piper-tts numpy vosk    (vosk braucht evtl. zusätzlich: pip install srt)
  ffmpeg im PATH
  Piper-Stimme laden (nicht ins Repo legen), für Thorsten seit 15.10.2026 das bessere „high“-Modell:
    https://huggingface.co/rhasspy/piper-voices/tree/main/de/de_DE/thorsten/high
    (de_DE-thorsten-high.onnx und de_DE-thorsten-high.onnx.json in denselben Ordner)
  Vosk-Modell entpackt (vosk-model-small-de-0.15, siehe public/vosk/LIESMICH.txt)

Aufruf:
  python werkzeuge/stimmen_erzeugen.py --stimme thorsten --onnx pfad/de_DE-thorsten-high.onnx --vosk pfad/vosk-model-small-de-0.15
  --ziel ordner   schreibt die Dateien zum Anhören erst woandershin (Standard: public/audio/<stimme>)
  --s-stimmhaft   macht das S am Wortanfang weich wie in „Sonne“ (sechs-, sieben-, sechzig, siebzig …),
                  mit s_stimmhaft.py und den freigegebenen Werten Summen 0.55, Zischen 0.25. Für Thorsten nötig,
                  weil er jedes S am Wortanfang scharf spricht (die 6 klang wie „Sex“).
Eigene Aufnahmen (Stimme der Lehrkraft) brauchen dieses Skript nicht – siehe CLAUDE.md, Abschnitt „Eigene Stimme“.
"""
import argparse, json, os, subprocess, wave

ONES = ['null', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']
OC = ['', 'ein', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']
TEENS = {10: 'zehn', 11: 'elf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn', 16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn'}
TENS = ['', 'zehn', 'zwanzig', 'dreißig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig']


def zahlwort(n):  # identisch mit zahlwort() in src/App.jsx
    if n == 100: return 'hundert'
    if n < 10: return ONES[n]
    if n < 20: return TEENS[n]
    z, e = divmod(n, 10)
    return f'{OC[e]}und{TENS[z]}' if e else TENS[z]


# 0,35 s Stille vorne (sonst schneiden Tablets den Wortanfang ab), 0,3 s hinten, Lautstärke angleichen
AF = ('silenceremove=start_periods=1:start_threshold=-50dB,areverse,'
      'silenceremove=start_periods=1:start_threshold=-50dB,areverse,'
      'adelay=350,apad=pad_dur=0.3,highpass=f=70,loudnorm=I=-16:TP=-1.5')


def to_mp3(wav, mp3):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-af', AF, '-ar', '24000', '-ac', '1', '-b:a', '48k', mp3], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stimme', required=True)
    ap.add_argument('--onnx', required=True)
    ap.add_argument('--vosk', required=True)
    ap.add_argument('--tempo', type=float, default=1.35, help='length_scale: größer = langsamer')
    ap.add_argument('--ziel', help='Ausgabeordner (Standard: public/audio/<stimme>)')
    ap.add_argument('--s-stimmhaft', action='store_true', help='S am Wortanfang weich machen (s_stimmhaft.py)')
    a = ap.parse_args()
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    from vosk import Model, KaldiRecognizer, SetLogLevel
    SetLogLevel(-1)
    voice = PiperVoice.load(a.onnx)
    model = Model(a.vosk)
    grammar = json.dumps([zahlwort(n) for n in range(1, 101)] + ['[unk]'], ensure_ascii=False)
    if a.s_stimmhaft:
        from s_stimmhaft import stimmhaft  # liegt im selben Ordner

    def erkannt(mp3):
        pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', mp3, '-ar', '16000', '-ac', '1', '-f', 's16le', '-'], capture_output=True).stdout + b'\0' * 32000
        r = KaldiRecognizer(model, 16000, grammar); r.AcceptWaveform(pcm)
        return json.loads(r.FinalResult())['text'].replace(' ', '').replace('[unk]', '')

    out = a.ziel or os.path.join('public', 'audio', a.stimme)
    os.makedirs(out, exist_ok=True)
    # Wenn eine Datei nicht verständlich ist: mit anderen Einstellungen neu versuchen
    varianten = [(a.tempo, 0.35, 0.35), (1.6, 0.3, 0.3), (1.3, 0.5, 0.5), (1.5, 0.2, 0.2), (1.7, 0.4, 0.3), (1.4, 0.6, 0.6)] * 3
    for n in range(1, 101):
        wort, ziel = zahlwort(n), os.path.join(out, f'{n}.mp3')
        weich = a.s_stimmhaft and wort.startswith('s')
        ok = False
        for ls, ns, nw in varianten:
            if weich:
                stimmhaft(voice, wort, ziel, tempo=ls)  # Summen 0.55, Zischen 0.25 (freigegeben)
            else:
                with wave.open('_tmp.wav', 'wb') as w:
                    voice.synthesize_wav(wort + '.', w, syn_config=SynthesisConfig(length_scale=ls, noise_scale=ns, noise_w_scale=nw))
                to_mp3('_tmp.wav', ziel)
            if erkannt(ziel) == wort:
                ok = True; break
        print(n, wort, ('weiches S, ' if weich else '') + ('ok' if ok else 'UNDEUTLICH – bitte anhören'), flush=True)
    if os.path.exists('_tmp.wav'):
        os.remove('_tmp.wav')


if __name__ == '__main__':
    main()
