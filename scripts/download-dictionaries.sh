#!/bin/bash

# XBook Dictionary Download Script
# Downloads open-source dictionaries and vocabulary data

set -e

echo "📚 XBook Dictionary Download Tool"
echo "=================================="
echo ""

# Create directories
DICT_DIR="$(pwd)/data/dictionaries"
mkdir -p "$DICT_DIR"/{jmdict,jlpt,kanjidic,english,tatoeba}

echo "📁 Created dictionary directories"
echo ""

# ============================================
# Japanese Resources
# ============================================

echo "🇯🇵 Downloading Japanese Resources..."
echo ""

# 1. JMdict (JSON format - ~200MB)
if [ ! -f "$DICT_DIR/jmdict/jmdict-eng.json" ]; then
    echo "📥 Downloading JMdict (JSON)..."
    cd "$DICT_DIR/jmdict"

    # Get latest release from jmdict-simplified
    JMDICT_URL="https://github.com/scriptin/jmdict-simplified/releases/latest/download/jmdict-eng-common.json"
    wget -q --show-progress "$JMDICT_URL" -O jmdict-eng-common.json || curl -L "$JMDICT_URL" -o jmdict-eng-common.json

    # Also get full version (larger)
    JMDICT_FULL_URL="https://github.com/scriptin/jmdict-simplified/releases/latest/download/jmdict-eng.json"
    wget -q --show-progress "$JMDICT_FULL_URL" -O jmdict-eng.json || curl -L "$JMDICT_FULL_URL" -o jmdict-eng.json

    cd - > /dev/null
    echo "✅ JMdict downloaded"
else
    echo "✓ JMdict already exists"
fi

echo ""

# 2. JLPT Vocabulary
if [ ! -d "$DICT_DIR/jlpt/jlpt-vocab" ]; then
    echo "📥 Downloading JLPT Vocabulary..."
    cd "$DICT_DIR/jlpt"

    # Try SSH first, fallback to HTTPS
    git clone --depth 1 git@github.com:stephenmk/jlpt-vocab.git 2>/dev/null || \
    git clone --depth 1 https://github.com/stephenmk/jlpt-vocab.git

    cd - > /dev/null
    echo "✅ JLPT vocabulary downloaded"
else
    echo "✓ JLPT vocabulary already exists"
fi

echo ""

# 3. KANJIDIC
if [ ! -f "$DICT_DIR/kanjidic/kanjidic.json" ]; then
    echo "📥 Downloading KANJIDIC..."
    cd "$DICT_DIR/kanjidic"

    # Download from jmdict-simplified
    KANJIDIC_URL="https://github.com/scriptin/jmdict-simplified/releases/latest/download/kanjidic.json"
    wget -q --show-progress "$KANJIDIC_URL" -O kanjidic.json || curl -L "$KANJIDIC_URL" -o kanjidic.json

    cd - > /dev/null
    echo "✅ KANJIDIC downloaded"
else
    echo "✓ KANJIDIC already exists"
fi

echo ""

# ============================================
# English Resources
# ============================================

echo "🇬🇧 Downloading English Resources..."
echo ""

# 1. COCA Top 5000
if [ ! -d "$DICT_DIR/english/COCA-WordFrequency" ]; then
    echo "📥 Downloading COCA Top 5000..."
    cd "$DICT_DIR/english"

    # Try SSH first, fallback to HTTPS
    git clone --depth 1 git@github.com:brucewlee/COCA-WordFrequency.git 2>/dev/null || \
    git clone --depth 1 https://github.com/brucewlee/COCA-WordFrequency.git

    cd - > /dev/null
    echo "✅ COCA frequency list downloaded"
else
    echo "✓ COCA frequency list already exists"
fi

echo ""

# 2. Create API config for Free Dictionary API
echo "📝 Creating English Dictionary API config..."
cat > "$DICT_DIR/english/api-config.json" << 'EOF'
{
    "name": "Free Dictionary API",
    "url": "https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
    "free": true,
    "no_api_key": true,
    "rate_limit": "unlimited",
    "data_source": "Wiktionary",
    "usage": "curl https://api.dictionaryapi.dev/api/v2/entries/en/hello"
}
EOF
echo "✅ API config created"

echo ""

# ============================================
# Optional: Tatoeba Sentences
# ============================================

read -p "📥 Download Tatoeba sentence database? (~500MB) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Downloading Tatoeba sentences..."
    cd "$DICT_DIR/tatoeba"

    # Download Japanese sentences
    wget -q --show-progress https://downloads.tatoeba.org/exports/sentences.tar.bz2
    tar -xjf sentences.tar.bz2
    rm sentences.tar.bz2

    # Download links (translations)
    wget -q --show-progress https://downloads.tatoeba.org/exports/links.tar.bz2
    tar -xjf links.tar.bz2
    rm links.tar.bz2

    cd - > /dev/null
    echo "✅ Tatoeba downloaded"
else
    echo "⏭️  Skipping Tatoeba (can download later)"
fi

echo ""

# ============================================
# Summary
# ============================================

echo "=================================="
echo "📊 Download Summary"
echo "=================================="
echo ""

echo "Japanese:"
ls -lh "$DICT_DIR/jmdict"/*.json 2>/dev/null | awk '{print "  - " $9 ": " $5}'
ls -d "$DICT_DIR/jlpt"/* 2>/dev/null | xargs basename | sed 's/^/  - /'
ls -lh "$DICT_DIR/kanjidic"/*.json 2>/dev/null | awk '{print "  - " $9 ": " $5}'

echo ""
echo "English:"
ls -d "$DICT_DIR/english"/* 2>/dev/null | xargs basename | sed 's/^/  - /'

echo ""
echo "=================================="
echo "✅ All dictionaries downloaded!"
echo "=================================="
echo ""

echo "Next steps:"
echo "1. Run import script: ./scripts/import-dictionaries.sh"
echo "2. Verify data: docker compose exec postgres psql -U xbook_admin -d xbook -c '\dt'"
echo "3. Test lookup: curl http://localhost:8000/api/v1/dictionary/lookup?word=日本語"
echo ""

echo "📖 See docs/DICTIONARY_RESOURCES.md for details"
