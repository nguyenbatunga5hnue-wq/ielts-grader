#!/usr/bin/env bash
# Cài môi trường phân tích bài nói. Chỉ cần PyPI + GitHub (KHÔNG cần huggingface).
# Dùng: bash setup.sh [MODELS_DIR]   (mặc định ~/.cache/ielts-speech-models)
set -e
M="${1:-$HOME/.cache/ielts-speech-models}"; mkdir -p "$M"
command -v ffmpeg >/dev/null || { echo "Cần ffmpeg (apt-get install -y ffmpeg)"; exit 1; }
pip install -q sherpa-onnx cmudict soundfile scipy editdistance numpy torch resampy tqdm munkres regex pyyaml
pip install -q --no-deps allosaurus panphon
# panphon cần unicodecsv (không build được trên py3.13) -> shim bằng csv chuẩn
python3 -c "import unicodecsv" 2>/dev/null || echo "from csv import *" > "$(python3 -c 'import site;print(site.getsitepackages()[0])')/unicodecsv.py"
R=https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models
cd "$M"
[ -f silero_vad.onnx ] || curl -sSL -O $R/silero_vad.onnx
for m in sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8 sherpa-onnx-whisper-base.en; do
  [ -d $m ] || { curl -sSL -O $R/$m.tar.bz2 && tar xjf $m.tar.bz2 && rm $m.tar.bz2; }
done
python3 -c "from allosaurus.app import read_recognizer" 2>/dev/null
python3 -m allosaurus.bin.list_model 2>/dev/null | grep -q eng2102 || python3 -m allosaurus.bin.download_model -m eng2102
echo "OK. Models ở $M  (export SPEECH_MODELS=$M)"
