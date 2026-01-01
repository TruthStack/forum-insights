import streamlit as st
import json
import base64
import os
import sys

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
try:
    from modules.incident_ingestion.main import poll_forums
    from modules.log_parser.main import parse_log
    from modules.prompt_builder.main import build_prompt
    from modules.gemini_explainer.main import explain_incident
    from modules.historical_storage.main import store_incident, query_incidents
    from modules.trend_aggregator.main import aggregate_trends
    from modules.notification_dispatcher.main import dispatch
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please make sure all module directories exist with main.py files")

# Page config
st.set_page_config(
    page_title="Forum Insights: AI TL;DR Bot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        color: #1E40AF;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem !important;
        color: #374151;
        margin-top: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F3F4F6;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">🤖 Forum Insights: AI-Powered TL;DR Bot</h1>', unsafe_allow_html=True)
st.markdown("""
<p style="font-size: 1.1rem; color: #6B7280;">
Automatically summarize long forum threads, detect trends, and get proactive alerts.
Built for the <strong>Foru.ms x v0 Hackathon</strong>.
</p>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/forum--v1.png", width=80)
    st.title("⚙️ Settings")
    
    st.subheader("API Keys")
    forums_key = st.text_input("Foru.ms API Key", type="password", value="demo-key")
    gemini_key = st.text_input("Gemini API Key", type="password", value="demo-key")
    
    st.subheader("Alert Settings")
    enable_slack = st.checkbox("Enable Slack Alerts", value=True)
    enable_email = st.checkbox("Enable Email Alerts", value=False)
    
    st.divider()
    
    st.caption("""
    **How it works:**
    1. Paste a thread URL
    2. AI summarizes content
    3. Trends are analyzed
    4. Alerts are sent (if enabled)
    """)

# Main content
st.markdown('<h2 class="sub-header">🔗 Enter Thread Details</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    thread_url = st.text_input(
        "Foru.ms Thread URL or ID",
        placeholder="https://foru.ms/thread/12345 or just 12345",
        value="78945-software-update-broke-my-plugin"
    )

with col2:
    analyze_button = st.button("🚀 Analyze Thread", type="primary", use_container_width=True)

# Initialize session state for results
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

if analyze_button and thread_url:
    with st.spinner("🔄 Fetching and analyzing thread..."):
        # Extract thread ID
        thread_id = thread_url.split("/")[-1] if "/" in thread_url else thread_url
        
        # Step 1: Fetch posts from Foru.ms
        st.info(f"📥 Fetching thread: {thread_id}")
        posts = poll_forums(thread_id, forums_key)
        
        # Display posts preview
        with st.expander(f"📄 View {len(posts)} Thread Posts"):
            for i, post in enumerate(posts, 1):
                st.markdown(f"**Post #{i} by {post['user']}**")
                st.write(post['message'])
                st.caption(f"Likes: {post['likes']} | {post['timestamp']}")
                st.divider()
        
        # Step 2: Parse logs
        st.info("🔍 Parsing and sanitizing posts...")
        parsed_logs = []
        for post in posts:
            parsed = parse_log(post)
            parsed_logs.append(parsed)
        
        # Step 3: Build prompt and generate TL;DR
        st.info("🤖 Generating AI summary with Gemini...")
        combined_messages = " ".join([p.get("message", "") for p in parsed_logs])
        prompt_data = {"parsed_fields": {"message": combined_messages}}
        built_prompt = build_prompt(prompt_data)
        summary = explain_incident(built_prompt)
        
        # Display TL;DR
        st.markdown('<h2 class="sub-header">📋 AI-Generated TL;DR</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Urgency", summary.get("urgency", "medium").upper())
        with col2:
            st.metric("Sentiment", summary.get("sentiment", "neutral").capitalize())
        with col3:
            st.metric("Confidence", f"{summary.get('confidence', 0.85)*100:.0f}%")
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"**🧐 What happened:**\n{summary.get('what_happened', 'No summary generated')}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("**🔍 Root causes:**")
            for cause in summary.get("root_cause", ["Not specified"]):
                st.markdown(f"• {cause}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("**🚀 Recommended actions:**")
            for action in summary.get("remediation", ["Monitor thread"]):
                st.markdown(f"• {action}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Step 4: Store and analyze trends
        st.markdown('<h2 class="sub-header">📈 Trend Analysis</h2>', unsafe_allow_html=True)
        
        for log in parsed_logs:
            store_incident(log)
        
        trends = aggregate_trends({"incidents": parsed_logs})
        
        # Display trend metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Posts", trends["total_incidents"])
        with col2:
            st.metric("Avg Toxicity", f"{trends['aggregates'].get('avg_toxicity', 0)*100:.0f}%")
        with col3:
            sentiment = trends['aggregates'].get('dominant_sentiment', 'neutral')
            st.metric("Dominant Sentiment", sentiment.capitalize())
        with col4:
            error_type = trends['aggregates'].get('common_error_type', 'discussion')
            st.metric("Main Topic", error_type.capitalize())
        
        # Trend chart
        if 'sentiment_distribution' in trends['aggregates']:
            chart_data = trends['aggregates']['sentiment_distribution']
            st.bar_chart(chart_data)
        
        # Display insights
        if trends.get('insights'):
            st.markdown("**💡 Key Insights:**")
            for insight in trends['insights']:
                st.markdown(f"• {insight}")
        
        # Step 5: Send alerts
        st.markdown('<h2 class="sub-header">📢 Alert System</h2>', unsafe_allow_html=True)
        
        alert_method = "both" if enable_slack and enable_email else "slack" if enable_slack else "email" if enable_email else None
        
        if alert_method:
            st.info(f"Sending {alert_method} alert...")
            alert_result = dispatch(summary, alert_method)
            
            if alert_result.get('status') == 'sent':
                st.success(f"✅ Alert sent successfully via {alert_method}")
            elif alert_result.get('status') == 'sent_multiple':
                st.success("✅ Alerts sent to both Slack and Email")
            else:
                st.warning(f"⚠️ Alert status: {alert_result.get('status')}")
        else:
            st.warning("⚠️ No alert methods enabled in settings")
        
        # Step 6: Historical context
        st.markdown('<h2 class="sub-header">🕐 Historical Context</h2>', unsafe_allow_html=True)
        
        similar_threads = query_incidents({"service": "forum"})
        
        if similar_threads:
            st.info(f"📚 Found {len(similar_threads)} similar historical threads")
            
            for i, thread in enumerate(similar_threads[:3], 1):
                with st.expander(f"Similar thread #{i}"):
                    st.write(f"**Message:** {thread.get('message', 'No message')[:200]}...")
                    if 'timestamp' in thread:
                        st.caption(f"Stored at: {thread['timestamp']}")
        else:
            st.info("📚 No similar historical threads found")
        
        # Store results in session state
        st.session_state.analysis_results = {
            "summary": summary,
            "trends": trends,
            "posts_count": len(posts),
            "thread_id": thread_id
        }
        
        # Success celebration
        st.balloons()
        st.success("🎉 Analysis complete! All modules executed successfully.")

# Display previous results if available
elif st.session_state.analysis_results:
    st.markdown("---")
    st.markdown("### 📊 Previous Analysis Results")
    
    results = st.session_state.analysis_results
    st.write(f"**Thread ID:** {results['thread_id']}")
    st.write(f"**Posts analyzed:** {results['posts_count']}")
    st.write(f"**Summary generated:** {results['summary'].get('what_happened', '')[:100]}...")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🔧 Built With:**")
    st.markdown("- Foru.ms API")
    st.markdown("- Gemini AI")
    st.markdown("- Python/Streamlit")
with col2:
    st.markdown("**🏆 Hackathon:**")
    st.markdown("Foru.ms x v0")
    st.markdown("Theme: *We built the engine*")
    st.markdown("*You build the car!*")
with col3:
    st.markdown("**🔗 Links:**")
    st.markdown("[GitHub Repository](https://github.com/TruthStack/forum-insights)")
    st.markdown("[Live Demo](https://forum-insights-tldr-bot.vercel.app)")
    st.markdown("[Devpost Submission](https://devpost.com)")

st.caption("Forum Insights TL;DR Bot | Winner-Level Submission for Foru.ms x v0 Hackathon")
