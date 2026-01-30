#!/bin/bash
# Install Quick Capture Tools (qn + qc)

echo "🚀 Installing Quick Capture Tools..."

# Install qn (Quick Notes)
mkdir -p ~/bin
cp /home/zous/clawd/nightly-projects/quick-capture/qn ~/bin/qn
chmod +x ~/bin/qn

# Install qc (Quick Capture)
cp /home/zous/clawd/nightly-projects/quick-capture/qc ~/bin/qc
chmod +x ~/bin/qc

# Add to PATH if not already
if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
fi

echo ""
echo "✅ Installed tools:"
echo "   📝 qn - Quick Notes (with tags & search)"
echo "   📦 qc - Quick Capture (tasks, ideas, bugs)"
echo ""
echo "Usage:"
echo "   qn \"Buy milk #shopping\"      # Quick note with tags"
echo "   qn --search \"AI\"             # Search notes"
echo "   qn --today                    # View today's notes"
echo "   qn --tags                     # List all tags"
echo ""
echo "   qc \"great idea #idea\"        # Quick capture"
echo "   qc -l                         # List all captures"
echo "   qc --export                   # Export to memory"
echo ""
echo "📁 Tools location: ~/bin/"
