import base64
import io
import requests
import streamlit as st
import PIL
import helper
import setting

def main():
    """
    Main function for the Streamlit app.
    """
    setting.configure_page()

    # Creating sidebar
    with st.sidebar:
        st.header("Drawing Configuration")     # Adding header to sidebar
        # Adding file uploader to sidebar for selecting images
        source_img = st.sidebar.file_uploader(
    "Choose a DWG or image file...",
    type=("dwg", "jpg", "jpeg", "png")
)
        # Model Options
        confidence = setting.get_model_confidence()

        # Multiselect for selecting labels
        available_labels = ['Column', 'Curtain Wall', 'Dimension', 'Door', 'Railing', 'Sliding Door', 'Stair Case', 'Wall', 'Window']
        selected_labels = setting.select_labels(available_labels)

    # Creating main page heading
    st.title("Floor Plan Object Detection using YOLOv8")

    # Creating two columns on the main page
    col1, col2 = st.columns([1, 3])

    # Adding image to the first column if image is uploaded
    with col1:
        if source_img:
            file_extension = source_img.name.split(".")[-1].lower()

            if file_extension == "dwg":
                st.info(
                    "DWG file uploaded. It will be converted and detected by the backend."
                )
                uploaded_image = source_img

            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(
                    uploaded_image,
                    caption="Uploaded Image",
                    use_column_width=True,
                )

        else:
            uploaded_image = None
            st.warning("Please upload a DWG or image file.")


    if st.sidebar.button("Detect Objects"):
        if uploaded_image is None:
            st.warning(
                "Please upload a valid image before detecting objects."
            )
        else:
            files = {
                "file": (
                    source_img.name,
                    source_img.getvalue(),
                    source_img.type or "application/octet-stream",
                )
            }

            data = {
                "confidence": confidence,
                "labels": ",".join(selected_labels),
            }
            try:
                with st.spinner(
                    "DWG를 변환하고 객체를 탐지하는 중입니다..."
                ):
                    response = requests.post(
                        "http://127.0.0.1:8000/detect",
                        files=files,
                        data=data,
                        timeout=120,
                    )

                response.raise_for_status()
                api_result = response.json()

            except requests.exceptions.ConnectionError:
                st.error(
                    "Backend 서버에 연결할 수 없습니다. "
                    "uvicorn 서버가 실행 중인지 확인하세요."
                )
                st.stop()

            except requests.exceptions.Timeout:
                st.error(
                    "처리 시간이 너무 오래 걸렸습니다. "
                    "도면 크기를 줄이거나 다시 시도하세요."
                )
                st.stop()

            except requests.exceptions.HTTPError:
                try:
                    error_message = response.json().get(
                        "detail",
                        "Backend 처리 중 오류가 발생했습니다.",
                    )
                except ValueError:
                    error_message = (
                        "Backend 처리 중 오류가 발생했습니다."
                    )

                st.error(error_message)
                st.stop()

            except requests.exceptions.RequestException as error:
                st.error(f"요청 중 오류가 발생했습니다: {error}")
                st.stop()

            object_counts = api_result["counts"]

            image_bytes = base64.b64decode(
                api_result["annotated_image"]
            )
            res_plotted = PIL.Image.open(
                io.BytesIO(image_bytes)
            )

            with col2:
                st.image(
                    res_plotted,
                    caption="Detected Floor Plan",
                    use_column_width=True,
                )

                st.write("\n\nDetected Objects and their Counts:")
                for label, count in object_counts.items():
                    st.write(f"{label}: {count}")

                csv_file = helper.generate_csv(object_counts)
                st.download_button(
                    label="Download CSV",
                    data=csv_file,
                    file_name="detected_objects.csv",
                    mime="text/csv",
                )

if __name__ == "__main__":
    main()
