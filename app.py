import io
from PIL import Image
from rembg import remove
import streamlit as st

st.set_page_config(
    page_title="Image Background Remover",
    layout="centered"
)

st.title("Image Background Remover")
st.write("Upload an image to automatically isolate the foreground subject and download a transparent PNG.")

uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Image**")
        st.image(input_image, use_container_width=True)
        
    with col2:
        st.markdown("**Processed Output**")
        with st.spinner("Removing background..."):
            # Convert image to bytes for processing
            img_byte_arr = io.BytesIO()
            input_image.save(img_byte_arr, format=input_image.format or 'PNG')
            input_bytes = img_byte_arr.getvalue()
            
            # Remove background
            output_bytes = remove(input_bytes)
            output_image = Image.open(io.BytesIO(output_bytes))
            
            st.image(output_image, use_container_width=True)
            
    # Prepare download buffer
    buffer = io.BytesIO()
    output_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    st.markdown("---")
    st.download_button(
        label="Download Transparent PNG",
        data=buffer,
        file_name="background_removed.png",
        mime="image/png"
    )
