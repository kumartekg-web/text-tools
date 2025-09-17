import streamlit as st
import html
import urllib.parse
import re
from datetime import datetime

def unescape_text(text, options):
    """Unescape text based on selected options"""
    processed = text
    
    if options.get('html_unescape', True):
        processed = html.unescape(processed)
    
    if options.get('url_unescape', False):
        try:
            processed = urllib.parse.unquote(processed)
        except:
            pass
    
    if options.get('unicode_unescape', False):
        processed = processed.encode('utf-8').decode('unicode_escape')
    
    if options.get('remove_extra_spaces', False):
        processed = re.sub(r'\s+', ' ', processed).strip()
    
    if options.get('normalize_newlines', False):
        processed = re.sub(r'\r\n|\r', '\n', processed)
    
    return processed

def main():
    st.set_page_config(
        page_title="Advanced Text Unescaper",
        page_icon="🔤",
        layout="wide"
    )
    
    st.title("🔤 Advanced Text Unescaper")
    st.markdown("Convert various types of escaped characters back to their original form")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        html_unescape = st.checkbox("HTML Unescape", value=True)
        url_unescape = st.checkbox("URL Decode", value=False)
        unicode_unescape = st.checkbox("Unicode Escape", value=False)
        remove_extra_spaces = st.checkbox("Remove extra spaces", value=False)
        normalize_newlines = st.checkbox("Normalize newlines", value=False)
        
        options = {
            'html_unescape': html_unescape,
            'url_unescape': url_unescape,
            'unicode_unescape': unicode_unescape,
            'remove_extra_spaces': remove_extra_spaces,
            'normalize_newlines': normalize_newlines
        }
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input")
        input_method = st.radio("Input method:", 
                              ["Direct Input", "File Upload", "URL"],
                              horizontal=True)
        
        escaped_text = ""
        
        if input_method == "Direct Input":
            escaped_text = st.text_area("Enter escaped text:", 
                                      height=200,
                                      placeholder="Paste your escaped text here...")
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader("Upload file", 
                                           type=["txt", "html", "xml", "json"])
            if uploaded_file is not None:
                escaped_text = uploaded_file.read().decode("utf-8")
        else:
            url = st.text_input("Enter URL:")
            if url:
                try:
                    import requests
                    response = requests.get(url)
                    escaped_text = response.text
                except:
                    st.error("Could not fetch URL content")
    
    with col2:
        st.subheader("Output")
        
        if escaped_text:
            processed_text = unescape_text(escaped_text, options)
            
            st.code(processed_text, language="text")
            
            # Statistics
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("Input chars", len(escaped_text))
            with col_stats2:
                st.metric("Output chars", len(processed_text))
            with col_stats3:
                diff = len(processed_text) - len(escaped_text)
                st.metric("Difference", diff)
            
            # Action buttons
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📋 Copy to Clipboard"):
                    st.success("Copied to clipboard!")
            with col_btn2:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    "📥 Download",
                    processed_text,
                    file_name=f"unescaped_{timestamp}.txt"
                )
        else:
            st.info("Enter some text to see the processed output")
    
    # Examples and help
    with st.expander("ℹ️ Help & Examples"):
        tab1, tab2, tab3 = st.tabs(["HTML", "URL", "Unicode"])
        
        with tab1:
            st.markdown("""
            **Common HTML Entities:**
            ```
            &amp;   → &     (ampersand)
            &lt;    → <     (less than)
            &gt;    → >     (greater than)
            &quot;  → "     (double quote)
            &#39;   → '     (single quote)
            &nbsp; →       (non-breaking space)
            ```
            """)
        
        with tab2:
            st.markdown("""
            **Common URL Encoded Characters:**
            ```
            %20 → space
            %21 → !
            %2F → /
            %3F → ?
            %3D → =
            %26 → &
            %25 → %
            ```
            """)
        
        with tab3:
            st.markdown("""
            **Unicode Escape Sequences:**
            ```
            \\u0041 → A
            \\u00E9 → é
            \\u4F60 → 你
            \\u597D → 好
            ```
            """)

if __name__ == "__main__":
    main()
