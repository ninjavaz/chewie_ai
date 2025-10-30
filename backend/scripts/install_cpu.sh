#!/bin/bash
# Install dependencies with CPU-only PyTorch to save disk space

set -e

echo "🧹 Cleaning old venv..."
rm -rf venv

echo "🐍 Creating new virtual environment with Python 3.11..."
~/.pyenv/versions/3.11.9/bin/python -m venv venv

echo "✅ Activating venv..."
source venv/bin/activate

echo "📦 Installing PyTorch CPU-only (saves ~3 GB)..."
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo "📦 Installing other dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "💾 Disk space saved: ~3 GB (CPU-only vs CUDA)"
echo ""
echo "🚀 To activate venv:"
echo "  source venv/bin/activate"
echo ""
echo "🧪 To test:"
echo "  python -c 'import sentence_transformers; print(\"✅ Works!\")'"
echo ""
