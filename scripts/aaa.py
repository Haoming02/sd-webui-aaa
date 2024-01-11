from modules import script_callbacks
import gradio as gr
import numpy as np
import cv2


def check_alpha(img) -> bool:
    return img.shape[-1] == 4 and (img[:, :, 3] < 255).any()

def process_mask(bg: str, fg: str, tc: float, lt: float, ht: float):
    if (bg is None) or (fg is None):
        return [None, None]

    fg_img = cv2.imread(fg, cv2.IMREAD_UNCHANGED)

    if not check_alpha(fg_img):
        print("Foreground Image contains no transparency...")
        return [None, None]

    bg_img = cv2.imread(bg, cv2.IMREAD_UNCHANGED)

    if (bg_img.shape[0] != fg_img.shape[0]) or (bg_img.shape[1] != fg_img.shape[1]):
        print('Currently, only images with the same size are supported...')
        return [None, None]

    mask = fg_img[:, :, 3]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edge = cv2.Canny(mask, lt, ht)
    dilate = cv2.dilate(edge, kernel, iterations=tc)

    background = bg_img[:, :, :3].astype(float)
    foreground = fg_img[:, :, :3].astype(float)

    if check_alpha(bg_img):
        bg_alpha = bg_img[:, :, 3].astype(float) / 255.0
        bg_alpha = cv2.merge([bg_alpha] * 3)
    else:
        bg_alpha = np.ones_like(background)

    alpha = mask.astype(float) / 255.0
    alpha = cv2.merge([alpha] * 3)

    background = cv2.multiply(np.maximum(0.0, bg_alpha - alpha), background)
    foreground = cv2.multiply(alpha, foreground)

    blended = cv2.cvtColor(
        cv2.add(foreground, background).astype("uint8"),
        cv2.COLOR_BGR2RGB
    )

    final = cv2.merge((
        blended,
        (np.maximum(alpha[:, :, 0], bg_alpha[:, :, 0]) * 255.0).astype("uint8")
    ))

    return [
        final,
        dilate.astype("uint8"),
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
                    label="Mask Thickness", minimum=5, maximum=50, step=5, value=15
                )

                low_t = gr.Slider(
                    label="Low Threshold", minimum=0, maximum=255, step=1, value=0
                )

                high_t = gr.Slider(
                    label="High Threshold", minimum=0, maximum=255, step=1, value=100
                )

            with gr.Column():
                proc_btn = gr.Button("Process Mask", variant="primary")
                send_btn = gr.Button("Send to Inpaint", variant="primary")

        proc_btn.click(
            process_mask,
            inputs=[background, foreground, thicc, low_t, high_t],
            outputs=[img, mask],
        )

        send_btn.click(
            None, None, None,
            _js="() => { aaa_sendImage2InpaintUpload(); }"
        )

    return [(aaa_UI, "AAA", "sd-webui-aaa")]


script_callbacks.on_ui_tabs(aaa_ui)
