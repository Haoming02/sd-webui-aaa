from modules import script_callbacks
import gradio as gr
import numpy as np
from PIL import Image
import cv2


def check_alpha(img:np.array) -> bool:
    return img.shape[-1] == 4 and (img[:, :, 3] < 255).any()

def preprocess_foreground(fg_img:Image, rotation:float, scale:float):
    if not check_alpha(np.asarray(fg_img)):
        print("Foreground Image contains no transparency...")
        return None

    w, h = fg_img.size
    w = int(float(w) * scale)
    h = int(float(h) * scale)

    return fg_img.resize((w, h), resample=Image.BILINEAR).rotate(rotation, resample=Image.BILINEAR, expand=True)

def process_mask(bg: str, fg: str, tc: float, lt: float, ht: float, x:float, y:float, r:float, s:float):
    if (bg is None) or (fg is None):
        return [None, None]

    fg_img = preprocess_foreground(Image.open(fg), r, s)
    if fg_img is None:
        return [None, None]

    bg_img = Image.open(bg)

    width, height = bg_img.size
    new_fg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    new_fg.paste(fg_img, (x, y), fg_img)

    mask = np.asarray(new_fg)[:, :, 3]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edge = cv2.Canny(mask, lt, ht)
    dilate = cv2.dilate(edge, kernel, iterations=tc)

    bg_img.paste(new_fg, (0, 0), new_fg)

    return [
        bg_img,
        dilate.astype("uint8")
    ]


def aaa_ui():

    with gr.Blocks() as aaa_UI:
        with gr.Row():
            background = gr.Image(
                image_mode="RGBA",
                sources="upload",
                type="filepath",
                label="Background Image",
                show_download_button=False,
                interactive=True,
                height=250
            )

            foreground = gr.Image(
                image_mode="RGBA",
                sources="upload",
                type="filepath",
                label="Foreground Image",
                show_download_button=False,
                interactive=True,
                height=250
            )

            img = gr.Image(
                image_mode="RGBA",
                label="Blended Image",
                elem_id="aaa_img",
                interactive=False,
                height=250,
            )

            mask = gr.Image(
                image_mode="L",
                label="Mask",
                elem_id="aaa_mask",
                interactive=False,
                height=250
            )

        with gr.Row():
            with gr.Column():
                thicc = gr.Slider(
                    label="Mask Thickness", minimum=5, maximum=50, step=5, value=10
                )

                low_t = gr.Slider(
                    label="Low Threshold", minimum=0, maximum=255, step=1, value=0
                )

                high_t = gr.Slider(
                    label="High Threshold", minimum=0, maximum=255, step=1, value=100
                )

            with gr.Column():
                offset_x = gr.Slider(
                    label="X Offset", minimum=-2048, maximum=2048, step=1, value=0
                )

                offset_y = gr.Slider(
                    label="Y Offset", minimum=-2048, maximum=2048, step=1, value=0
                )

                with gr.Row():
                    offset_r = gr.Slider(
                        label="Rotation", minimum=-180, maximum=180, step=1, value=0
                    )

                    offset_s = gr.Slider(
                        label="Scale", minimum=0.0, maximum=2.0, step=0.1, value=1.0
                    )

        with gr.Row():
            proc_btn = gr.Button("Process Mask", variant="primary")
            send_btn = gr.Button("Send to Inpaint", variant="primary")

        proc_btn.click(
            process_mask,
            inputs=[background, foreground, thicc, low_t, high_t, offset_x, offset_y, offset_r, offset_s],
            outputs=[img, mask],
        )

        send_btn.click(
            None, None, None,
            _js="() => { aaa_sendImage2InpaintUpload(); }"
        )

    return [(aaa_UI, "AAA", "sd-webui-aaa")]


script_callbacks.on_ui_tabs(aaa_ui)
