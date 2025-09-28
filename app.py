import streamlit as st

from pokemon_analyzer import analyze_complete_team

def main():
    # Page config
    st.set_page_config(
        page_title="Pokemon Team Analyzer",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🔥 Pokemon Team Analyzer")
    st.markdown("**Analyze your Pokemon team's weaknesses and get AI-powered strategic recommendations!**")
    st.markdown("---")
    
    # Sidebar for team input
    with st.sidebar:
        st.header("🎮 Enter Your Team")
        st.markdown("Enter up to 6 Pokemon names:")
         
        pokemon_inputs = []
        for i in range(6):
            pokemon = st.text_input(
                f"Pokemon {i+1}:",
                key=f"pokemon_{i}",
                placeholder=f"e.g., Charizard"
           )
            if pokemon.strip():
                pokemon_inputs.append(pokemon.strip())
        
        # Analysis button
        analyze_button = st.button("🔍 Analyze Team", type="primary", use_container_width=True)        
        # Instructions
        st.markdown("---")
        st.markdown("### 💡 Tips:")
        st.markdown("• Enter Pokemon names in English")
        st.markdown("• Spelling matters (e.g., 'Charizard')")
        st.markdown("• Minimum 1 Pokemon required")
    
    # Main content area
    if analyze_button:
        if len(pokemon_inputs) == 0:
            st.error("⚠️ Please enter at least 1 Pokemon!")
            return
        
        with st.spinner("🔍 Analyzing your team..."):
            # Run analysis
            result = analyze_complete_team(pokemon_inputs)
        
        if not result["success"]:
            st.error(f"❌ Analysis failed: {result['error']}")
            return
        
        # Display results
        display_results(result, pokemon_inputs)
    
    else:
        # Welcome message
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown("### 👈 Enter your Pokemon team in the sidebar to get started!")
            st.markdown("This tool will analyze:")
            st.markdown("• **Type effectiveness** and team weaknesses")
            st.markdown("• **Critical vulnerabilities** (4x damage)")
            st.markdown("• **AI-powered recommendations** for improvement")
            st.markdown("• **Strategic notes** for competitive play")

def display_results(result, pokemon_inputs):
    """Display the complete analysis results"""
    
    team_data = result["team_data"]
    weakness_analysis = result["weakness_analysis"]
    ai_recommendations = result["ai_recommendations"]
    
    # Team Summary Section
    st.header("📊 Team Summary")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Team:")
        for pokemon in team_data["team_members"]:
            types_badges = ""
            for ptype in pokemon["types"]:
                types_badges += f"`{ptype.title()}` "
            
            # Display Pokemon with image if available
            col_img, col_info = st.columns([1, 4])
            with col_img:
                if pokemon["sprite"]:
                    st.image(pokemon["sprite"], width=80)
            with col_info:
                st.markdown(f"**{pokemon['name']}** {types_badges}")
    
    with col2:
        st.metric("Team Size", f"{team_data['success_count']}/6")
        st.metric("Type Coverage", f"{team_data['type_coverage']} types")
        st.metric("Critical Weaknesses", len(weakness_analysis["critical_weaknesses"]))
        st.metric("Major Weaknesses", len(weakness_analysis["major_weaknesses"]))
    
    # Failed Pokemon (if any)
    if team_data["failed_pokemon"]:
        st.warning(f"⚠️ Could not find: {', '.join(team_data['failed_pokemon'])}")
    
    st.markdown("---")
    
    # Weakness Analysis Section
    st.header("🛡️ Weakness Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Critical Weaknesses
        if weakness_analysis["critical_weaknesses"]:
            st.subheader("🚨 Critical Weaknesses (4x damage)")
            for weakness in weakness_analysis["critical_weaknesses"][:3]:
                with st.expander(f"💀 {weakness['type'].upper()} Type"):
                    st.error(f"**{', '.join(weakness['critical_pokemon'])}** take 4x damage!")
        
        # Major Weaknesses  
        if weakness_analysis["major_weaknesses"]:
            st.subheader("⚠️ Major Weaknesses (2+ vulnerable)")
            for weakness in weakness_analysis["major_weaknesses"][:5]:
                with st.expander(f"🔥 {weakness['type'].upper()} Type"):
                    st.warning(f"Threatens: **{', '.join(weakness['vulnerable_pokemon'])}**")
    
    with col2:
        # Immunities
        if weakness_analysis["immunities"]:
            st.subheader("✅ Immunities (0x damage)")
            for immunity in weakness_analysis["immunities"][:3]:
                with st.expander(f"🛡️ {immunity['type'].upper()} Type"):
                    st.success(f"Immune: **{', '.join(immunity['immune_pokemon'])}**")
        
        # Resistances
        strong_resistances = [r for r in weakness_analysis["resistances"] 
                            if len(r["resistant_pokemon"]) >= 2]
        if strong_resistances:
            st.subheader("💪 Strong Resistances")
            for resistance in strong_resistances[:5]:
                with st.expander(f"🔒 {resistance['type'].upper()} Type"):
                    st.info(f"Resists: **{', '.join(resistance['resistant_pokemon'])}**")
    
    st.markdown("---")
    
    # AI Recommendations Section
    st.header("🤖 AI Strategic Recommendations")
    st.markdown(ai_recommendations)
    
    st.markdown("---")
    st.markdown("*Analysis powered by PokeAPI and Gemini AI*")

if __name__ == "__main__":
    main()
