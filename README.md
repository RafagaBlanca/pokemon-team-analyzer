# 🔥 Pokemon Team Analyzer

An AI-powered Pokemon team analysis tool that provides instant weakness analysis and strategic recommendations for competitive play.


## 🎯 Overview

This tool automates the tedious process of analyzing Pokemon team compositions, calculating type effectiveness, and researching strategic improvements. What traditionally takes 15-20 minutes of manual analysis is now completed in under 30 seconds with deeper insights than manual methods.

### ✨ Key Features

- **⚡ Instant Team Analysis**: Enter 1-6 Pokemon and get comprehensive weakness analysis
- **🧠 AI Strategic Recommendations**: Get expert-level strategic advice powered by Gemini AI
- **🎯 Type Effectiveness Engine**: Precise damage multiplier calculations for all 18 Pokemon types
- **🛡️ Weakness Identification**: Automatically detect critical 4x weaknesses and major threats
- **💪 Resistance Analysis**: Identify team strengths and defensive capabilities
- **🎮 Competitive Focus**: Strategic recommendations tailored for competitive play
- **🖼️ Visual Interface**: Clean Streamlit UI with Pokemon sprites and organized results

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini AI API key (free at [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd pokemon-team-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Usage

### Basic Usage

1. **Enter Your Team**: In the sidebar, input 1-6 Pokemon names (e.g., "Charizard", "Blastoise")
2. **Click Analyze**: Hit the "🔍 Analyze Team" button
3. **Review Results**: Get instant analysis including:
   - Team summary with type coverage
   - Critical weaknesses (4x damage vulnerabilities)
   - Major weaknesses (types threatening multiple Pokemon)
   - Immunities and resistances
   - AI-powered strategic recommendations

### Example Teams to Try

**Classic Kanto Starter Team**:
- Charizard, Blastoise, Venusaur, Pikachu, Snorlax, Alakazam

**Balanced Competitive Team**:
- Garchomp, Rotom-Wash, Ferrothorn, Latios, Scizor, Heatran

**Monotype Challenge**:
- Charizard, Arcanine, Rapidash, Ninetales, Flareon, Magmortar

### Tips for Best Results

- ✅ Use exact Pokemon names (case doesn't matter)
- ✅ English names only (e.g., "Charizard" not "Dracaufeu")
- ✅ Hyphenated forms work (e.g., "Rotom-Wash")
- ✅ Minimum 1 Pokemon required for analysis

## 🏗️ Project Structure

```
pokemon-team-analyzer/
├── app.py                 # Streamlit UI application
├── pokemon_analyzer.py    # Core analysis logic
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🔧 Technical Details

### Core Components

1. **PokeAPI Integration**: Fetches Pokemon data including types, sprites, and stats
2. **Type Effectiveness Engine**: 18x18 matrix calculating precise damage multipliers
3. **Weakness Analysis**: Identifies critical vulnerabilities and team strengths
4. **AI Strategic Layer**: Gemini AI provides expert-level competitive recommendations

### Dependencies

- `streamlit`: Web UI framework
- `requests`: API calls to PokeAPI
- `python-dotenv`: Environment variable management
- `google-generativeai`: Gemini AI integration

## 🚨 Troubleshooting

### Common Issues

**"Pokemon not found" error**:
- Check spelling of Pokemon names
- Use English names only
- Some regional forms may not be recognized

**AI recommendations not loading**:
- Verify your Gemini API key is correct in `.env`
- Check internet connection
- Ensure API key has sufficient quota

**App not starting**:
- Confirm Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that port 8501 is available

### Getting Help

If you encounter issues:
1. Check the console output for specific error messages
2. Verify your `.env` file is properly configured
3. Ensure all Pokemon names are spelled correctly

## 🔑 API Keys Setup

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

**Note**: The Gemini API has a generous free tier suitable for testing and light usage.

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Vercel (Recommended)
1. Push code to GitHub
2. Connect repository to Vercel
3. Add `GEMINI_API_KEY` to environment variables
4. Deploy automatically

### Other Platforms
- **Railway**: Simple drag-and-drop deployment
- **Render**: Python app deployment
- **Heroku**: Traditional cloud deployment

## 🎯 Use Cases

- **Competitive Players**: Analyze team compositions for tournaments
- **Casual Players**: Learn about type effectiveness and team building
- **Content Creators**: Quick analysis for team showcases
- **Pokemon Enthusiasts**: Explore strategic depth of team combinations

## 🔄 Future Enhancements

- [ ] Meta tier integration
- [ ] Team comparison features
- [ ] Batch team analysis

## 📄 License

This project is for educational and personal use. Pokemon names and data are property of Nintendo/Game Freak/Creatures Inc.

---

**Built with ❤️ for the Pokemon competitive community**

*If you find this tool helpful, consider sharing it with fellow trainers!* 🎮