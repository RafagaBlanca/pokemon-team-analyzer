import requests
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import openai
from google import genai
from google.genai import types

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

client = genai.Client()


# Pokemon Type Effectiveness Chart
TYPE_EFFECTIVENESS = {
    "normal": {
        "super_effective": [],
        "not_very_effective": ["rock", "steel"],
        "no_effect": ["ghost"],
    },
    "fire": {
        "super_effective": ["grass", "ice", "bug", "steel"],
        "not_very_effective": ["fire", "water", "rock", "dragon"],
        "no_effect": [],
    },
    "water": {
        "super_effective": ["fire", "ground", "rock"],
        "not_very_effective": ["water", "grass", "dragon"],
        "no_effect": [],
    },
    "electric": {
        "super_effective": ["water", "flying"],
        "not_very_effective": ["electric", "grass", "dragon"],
        "no_effect": ["ground"],
    },
    "grass": {
        "super_effective": ["water", "ground", "rock"],
        "not_very_effective": [
            "fire",
            "grass",
            "poison",
            "flying",
            "bug",
            "dragon",
            "steel",
        ],
        "no_effect": [],
    },
    "ice": {
        "super_effective": ["grass", "ground", "flying", "dragon"],
        "not_very_effective": ["fire", "water", "ice", "steel"],
        "no_effect": [],
    },
    "fighting": {
        "super_effective": ["normal", "ice", "rock", "dark", "steel"],
        "not_very_effective": ["poison", "flying", "psychic", "bug", "fairy"],
        "no_effect": ["ghost"],
    },
    "poison": {
        "super_effective": ["grass", "fairy"],
        "not_very_effective": ["poison", "ground", "rock", "ghost"],
        "no_effect": ["steel"],
    },
    "ground": {
        "super_effective": ["fire", "electric", "poison", "rock", "steel"],
        "not_very_effective": ["grass", "bug"],
        "no_effect": ["flying"],
    },
    "flying": {
        "super_effective": ["electric", "grass", "fighting"],
        "not_very_effective": ["electric", "rock", "steel"],
        "no_effect": [],
    },
    "psychic": {
        "super_effective": ["fighting", "poison"],
        "not_very_effective": ["psychic", "steel"],
        "no_effect": ["dark"],
    },
    "bug": {
        "super_effective": ["grass", "psychic", "dark"],
        "not_very_effective": [
            "fire",
            "fighting",
            "poison",
            "flying",
            "ghost",
            "steel",
            "fairy",
        ],
        "no_effect": [],
    },
    "rock": {
        "super_effective": ["fire", "ice", "flying", "bug"],
        "not_very_effective": ["fighting", "ground", "steel"],
        "no_effect": [],
    },
    "ghost": {
        "super_effective": ["psychic", "ghost"],
        "not_very_effective": ["dark"],
        "no_effect": ["normal"],
    },
    "dragon": {
        "super_effective": ["dragon"],
        "not_very_effective": ["steel"],
        "no_effect": ["fairy"],
    },
    "dark": {
        "super_effective": ["fighting", "psychic"],
        "not_very_effective": ["fighting", "dark", "fairy"],
        "no_effect": [],
    },
    "steel": {
        "super_effective": ["ice", "rock", "fairy"],
        "not_very_effective": ["fire", "water", "electric", "steel"],
        "no_effect": [],
    },
    "fairy": {
        "super_effective": ["fighting", "dragon", "dark"],
        "not_very_effective": ["fire", "poison", "steel"],
        "no_effect": [],
    },
}


def get_pokemon_data(name: str) -> Optional[Dict]:

    name = name.lower()

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    try:

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            pokemon_info = {
                "name": data["name"].title(),
                "id": data["id"],
                "types": [type_info["type"]["name"] for type_info in data["types"]],
                "sprite": data["sprites"]["front_default"],
            }

            return pokemon_info

        else:

            print(f"Pokemon {name} not found")
            return None
    except requests.exceptions.RequestException as e:

        print(f"Error connecting to PokeApi: {e}")
        return None

    except KeyError as e:
        print(f"Error parsign Pokemon data: {e}")
        return None


def get_team_data(pokemon_list: List[str]) -> Dict:

    if len(pokemon_list) > 6:
        print("Error: Pokemon teams should have maximum 6 members")
        return None

    team_data = {
        "team_members": [],
        "all_types": [],
        "success_count": 0,
        "failed_pokemon": [],
    }

    print(f"Analyzing team of {len(pokemon_list)} Pokemon...")

    for i, pokemon in enumerate(pokemon_list, 1):
        print(f"{i}.- Fetching data of {pokemon}...")

        pokemon_data = get_pokemon_data(pokemon)

        if pokemon_data:
            team_data["team_members"].append(pokemon_data)
            team_data["all_types"].extend(pokemon_data["types"])
            team_data["success_count"] += 1

            print(f"{pokemon_data['name']} data obtained!")
        else:
            team_data["failed_pokemon"].append(pokemon)
            print(f"{pokemon} data not found!")

        team_data["unique_types"] = list(set(team_data["all_types"]))
        team_data["type_coverage"] = len(team_data["unique_types"])

    return team_data


def calculate_damage_multiplier(
    attacking_type: str, defending_types: List[str]
) -> float:

    if attacking_type not in TYPE_EFFECTIVENESS:
        return 1.0

    multiplier = 1.0
    attack_data = TYPE_EFFECTIVENESS[attacking_type]

    for defending_type in defending_types:
        if defending_type in attack_data["no_effect"]:
            multiplier *= 0
        elif defending_type in attack_data["super_effective"]:
            multiplier *= 2
        elif defending_type in attack_data["not_very_effective"]:
            multiplier *= 0.5

    return multiplier




def display_team_summary(team_data: Dict) -> None:
    print("\n" + "=" * 50)
    print("TEAM ANALYSIS SUMMARY")
    print("=" * 50)

    if team_data["team_members"]:
        for pokemon in team_data["team_members"]:
            types_str = " | ".join(pokemon["types"])
            print(f" {pokemon['name']} ({types_str})")

    if team_data["failed_pokemon"]:
        print(f"Failed to load {len(team_data['failed_pokemon'])} Pokemon: ")

        for pokemon in team_data["failed_pokemon"]:
            print(f"{pokemon} \n")

    print(f"Type Coverage: {team_data['type_coverage']} unique types")
    print(f"Types: {', '.join(team_data['unique_types'])}")

    print("\n" + "=" * 50)




def get_ai_team_recommendations(team_data: Dict, weakness_analysis: Dict) -> Optional[str]:

    # Step 1: Prepare team information for the prompt
    team_summary = []
    for pokemon in team_data["team_members"]:
        types_str = "/".join(pokemon["types"])
        team_summary.append(f"{pokemon['name']} ({types_str})")

    # Step 2: Prepare weakness information
    critical_weaknesses = []
    for weakness in weakness_analysis["critical_weaknesses"][:3]:
        critical_weaknesses.append(
            f"{weakness['type']} (4x damage to {', '.join(weakness['critical_pokemon'])})"
        )

    major_weaknesses = []
    for weakness in weakness_analysis["major_weaknesses"][:3]:
        major_weaknesses.append(
            f"{weakness['type']} (threatens {', '.join(weakness['vulnerable_pokemon'])})"
        )

    immunities = []
    for immunity in weakness_analysis["immunities"][:3]:
        immunities.append(
            f"{immunity['type']} (immune: {', '.join(immunity['immune_pokemon'])})"
        )

    prompt = f"""You are an expert competitive Pokemon analyst. Analyze this team and provide strategic recommendations as well as recommended items for each Pokemon.

CURRENT TEAM:
{chr(10).join([f"• {pokemon}" for pokemon in team_summary])}

CRITICAL WEAKNESSES (4x damage):
{chr(10).join([f"• {weakness}" for weakness in critical_weaknesses]) if critical_weaknesses else "• None"}

MAJOR WEAKNESSES (multiple vulnerable Pokemon):
{chr(10).join([f"• {weakness}" for weakness in major_weaknesses]) if major_weaknesses else "• None"}

Provide strategic analysis in this format:

## TEAM EVALUATION
[2-3 sentences about overall balance and playstyle]

## TOP 3 THREATS  
1. [Type] - [Why it's dangerous for this specific team]
2. [Type] - [Why it's dangerous for this specific team]
3. [Type] - [Why it's dangerous for this specific team]

## POKEMON RECOMMENDATIONS
1. **[Name] ([Type])** - [Why it solves key weaknesses]
2. **[Name] ([Type])** - [Why it improves team balance]  
3. **[Name] ([Type])** - [Alternative option with different strategy]

## STRATEGIC NOTES
[2-3 tactical tips for using this team effectively]

Be specific to this composition. Focus on competitive viability."""

    try:
        # Step 4: Call Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are an expert competitive Pokemon analyst with deep knowledge of type matchups, meta strategies, and team building."
            ),
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f"❌ Error getting AI recommendations: {str(e)}\n\nPlease check your API key in the .env file."


def analyze_team_weaknesses(team_data: Dict) -> Dict:
    all_types = [
        "normal",
        "fire",
        "water",
        "electric",
        "grass",
        "ice",
        "fighting",
        "poison",
        "ground",
        "flying",
        "psychic",
        "bug",
        "rock",
        "ghost",
        "dragon",
        "dark",
        "steel",
        "fairy",
    ]

    weakness_analysis = {
        "critical_weaknesses": [],  # Types that deal 4x+ damage to someone
        "major_weaknesses": [],  # Types that deal 2x damage to multiple members
        "minor_weaknesses": [],  # Types that deal 2x damage to few members
        "resistances": [],  # Types we deal 0.5x or less damage to
        "immunities": [],  # Types that deal no damage to us (0x)
        "team_coverage": {},  # How vulnerable each Pokemon is
        "type_threat_level": {},  # How dangerous each type is for the team
    }

    for attacking_type in all_types:
        vulnerable_pokemon = []
        critical_pokemon = []
        resistant_pokemon = []
        immune_pokemon = []

        for pokemon in team_data["team_members"]:
            multiplier = calculate_damage_multiplier(attacking_type, pokemon["types"])

            if multiplier >= 4.0:
                critical_pokemon.append(pokemon["name"])
                vulnerable_pokemon.append(pokemon["name"])
            elif multiplier >= 2.0:
                vulnerable_pokemon.append(pokemon["name"])
            elif multiplier == 0.0:
                immune_pokemon.append(pokemon["name"])
            elif multiplier <= 0.5:
                resistant_pokemon.append(pokemon["name"])

        threat_info = {
            "type": attacking_type,
            "vulnerable_count": len(vulnerable_pokemon),
            "critical_count": len(critical_pokemon),
            "vulnerable_pokemon": vulnerable_pokemon,
            "critical_pokemon": critical_pokemon,
            "resistant_pokemon": resistant_pokemon,
            "immune_pokemon": immune_pokemon,
        }

        weakness_analysis["type_threat_level"][attacking_type] = threat_info

        if critical_pokemon:
            weakness_analysis["critical_weaknesses"].append(threat_info)
        elif len(vulnerable_pokemon) >= 2:
            weakness_analysis["major_weaknesses"].append(threat_info)
        elif len(vulnerable_pokemon) >= 1:
            weakness_analysis["minor_weaknesses"].append(threat_info)

        if resistant_pokemon or immune_pokemon:
            weakness_analysis["resistances"].append(threat_info)

        if immune_pokemon:
            weakness_analysis["immunities"].append(threat_info)

    weakness_analysis["critical_weaknesses"].sort(
        key=lambda x: x["critical_count"], reverse=True
    )
    weakness_analysis["major_weaknesses"].sort(
        key=lambda x: x["vulnerable_count"], reverse=True
    )

    return weakness_analysis


def display_weakness_analysis(weakness_analysis: Dict) -> None:
    """
    Displays a clear report of team weaknesses
    """

    print("\n" + "=" * 60)
    print("🛡️  TEAM WEAKNESS ANALYSIS")
    print("=" * 60)

    # Critical weaknesses (4x damage)
    if weakness_analysis["critical_weaknesses"]:
        print("\n🚨 CRITICAL WEAKNESSES (4x+ damage):")
        for weakness in weakness_analysis["critical_weaknesses"][:3]:  # Top 3
            critical_str = ", ".join(weakness["critical_pokemon"])
            print(f"   💀 {weakness['type'].upper()}: {critical_str} take 4x damage!")

    # Major weaknesses (multiple Pokemon affected)
    if weakness_analysis["major_weaknesses"]:
        print(f"\n⚠️  MAJOR WEAKNESSES (2+ team members vulnerable):")
        for weakness in weakness_analysis["major_weaknesses"][:3]:  # Top 3
            vulnerable_str = ", ".join(weakness["vulnerable_pokemon"])
            print(f"   🔥 {weakness['type'].upper()}: {vulnerable_str}")

    # Team strengths
    if weakness_analysis["immunities"]:
        print(f"\n✅ IMMUNITIES (0x damage):")
        for immunity in weakness_analysis["immunities"][:3]:  # Top 3
            immune_str = ", ".join(immunity["immune_pokemon"])
            print(f"   🛡️  {immunity['type'].upper()}: {immune_str}")

    # Main resistances
    strong_resistances = [
        r for r in weakness_analysis["resistances"] if len(r["resistant_pokemon"]) >= 2
    ]
    if strong_resistances:
        print(f"\n💪 STRONG RESISTANCES (2+ team members resist):")
        for resistance in strong_resistances[:3]:  # Top 3
            resistant_str = ", ".join(resistance["resistant_pokemon"])
            print(f"   🔒 {resistance['type'].upper()}: {resistant_str}")

    print("\n" + "=" * 60)


def analyze_complete_team(pokemon_list: List[str]) -> Dict:
    """
    Complete team analysis: data + weaknesses + AI recommendations

    Args:
        pokemon_list: List of Pokemon names

    Returns:
        Dictionary with complete analysis
    """

    print("🔍 Starting complete team analysis...")

    # Step 1: Get team data
    team_data = get_team_data(pokemon_list)

    if team_data["success_count"] == 0:
        return {"success": False, "error": "No valid Pokemon found in the team"}

    # Step 2: Analyze weaknesses
    print("⚡ Calculating type effectiveness...")
    weakness_analysis = analyze_team_weaknesses(team_data)

    # Step 3: Get AI recommendations
    print("🤖 Getting AI recommendations...")
    ai_recommendations = get_ai_team_recommendations(team_data, weakness_analysis)

    # Step 4: Compile complete result
    complete_analysis = {
        "success": True,
        "team_data": team_data,
        "weakness_analysis": weakness_analysis,
        "ai_recommendations": ai_recommendations,
        "summary": {
            "team_size": team_data["success_count"],
            "type_coverage": team_data["type_coverage"],
            "critical_weaknesses_count": len(weakness_analysis["critical_weaknesses"]),
            "major_weaknesses_count": len(weakness_analysis["major_weaknesses"]),
        },
    }

    print("✅ Complete analysis finished!")
    return complete_analysis


def test_pokemon_api():
    """Function to test that everything works"""

    print("🧪 TESTING COMPLETE TEAM ANALYSIS WITH AI")
    print("-" * 60)

    test_team = ["Charizard", "Blastoise", "Venusaur", "Pikachu", "Snorlax", "Alakazam"]

    # Complete analysis
    result = analyze_complete_team(test_team)

    if result["success"]:
        # Show summary
        display_team_summary(result["team_data"])
        display_weakness_analysis(result["weakness_analysis"])

        # Show AI recommendations
        print("\n" + "=" * 60)
        print("🤖 AI STRATEGIC RECOMMENDATIONS")
        print("=" * 60)
        print(result["ai_recommendations"])
        print("=" * 60)

    else:
        print(f"❌ Analysis failed: {result['error']}")


if __name__ == "__main__":
    test_pokemon_api()
