import os
import time
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
from streamlit_tags import st_tags_sidebar


if 'counter' not in st.session_state: 
    st.session_state.counter = 0

if 'image_labels' not in st.session_state:
    st.session_state.image_labels = []

if 'crop_button' not in st.session_state:
    st.session_state.crop_button = False

def saving_increment(label, name, img):
    ## Incrementa o contador para obter a próxima foto
    st.session_state.image_labels.append(label)
    img.save(f'images/{label}/{name}')
    st.session_state.counter += 1

def saving_increment_crop(label, name, img):
    ## Incrementa o contador para obter a próxima foto
    st.session_state.image_labels.append(label)
    img.save(f'images/{label}/{name}')
    st.session_state.counter += 1
    st.session_state.crop_button = False

def main():
    st.set_page_config(initial_sidebar_state="expanded")
    st.title("Image to be labeled")
    st.sidebar.title('Image Uploader')

    uploaded_files = st.sidebar.file_uploader("Choose images", accept_multiple_files=True)
    labels = st_tags_sidebar(
        label='# Enter the labels :',
        text='Press enter to add more')
    
    if not uploaded_files or not labels:
        st.warning("Please upload images and enter labels.")
        return

    images = []
    progress_text = "Labeling progress."
    if uploaded_files and labels:

        # Dividir as etiquetas
        labels = [label.strip() for label in labels]
        
        for path in [labels[i] for i in range(len(labels))]:
            try:
                os.mkdir(f'images/')
            except:
                pass
            try:
                os.mkdir(f'images/{path}')
            except:
                pass

        for uploaded_file in uploaded_files:
            images.append(uploaded_file)

        crop_button = st.button('Crop image')
        
        if crop_button:
            st.session_state.crop_button = True

        if st.session_state.crop_button:
            try:
                img = Image.open(images[st.session_state.counter])
                realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
                if not realtime_update:
                    st.write("Double click to save crop")
                # Get a cropped image from the frontend
                cropped_img = st_cropper(img, realtime_update=realtime_update, box_color='yellow')
                
                st.write("Preview")
                _ = cropped_img.thumbnail((500,500))
                st.image(cropped_img)

                st.subheader('Choose a label for the image')
                label = st.radio(f"label:",[labels[i] for i in range(len(labels))])

                st.button(f"Next image", on_click=saving_increment_crop, args=[label, images[st.session_state.counter].name, cropped_img])
                
                st.progress((st.session_state.counter/len(images)), text=progress_text)
           
            except:
                st.success("All images have been labeled successfully!")
                st.balloons()
        else:
            try:
                img = Image.open(images[st.session_state.counter])
                st.image(img, caption=f"Image {st.session_state.counter+1}")

                st.subheader('Choose a label for the image')
                label = st.radio(f"label:",[labels[i] for i in range(len(labels))])

                st.button(f"Next image", on_click=saving_increment, args=[label, images[st.session_state.counter].name, img])
                st.progress((st.session_state.counter/len(images)), text=progress_text)

            except:
                st.success("All images have been labeled successfully!")
                st.balloons()

if __name__ == "__main__":
    main()
