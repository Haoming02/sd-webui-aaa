function aaa_sendImage2InpaintUpload() {
    const img = gradioApp().getElementById('aaa_img').querySelector('img');
    const mask = gradioApp().getElementById('aaa_mask').querySelector('img');

    if (img === null || mask === null)
        return;

    const imageInputs = gradioApp().getElementById('img2img_inpaint_upload_tab').querySelectorAll("input[type='file']");
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;

    ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);

    canvas.toBlob((blob) => {
        const file = new File(([blob]), "img.png");
        aaa_SetImage(imageInputs[0], file);
    });

    ctx.drawImage(mask, 0, 0, mask.naturalWidth, mask.naturalHeight);

    canvas.toBlob((blob) => {
        const file = new File(([blob]), "mask.png");
        aaa_SetImage(imageInputs[1], file);
    });

    switch_to_img2img_tab(4);
}

function aaa_SetImage(imageInput, file) {

    const dt = new DataTransfer();
    dt.items.add(file);
    const list = dt.files;

    imageInput.files = list;

    const event = new Event('change', {
        'bubbles': true,
        "composed": true
    });

    imageInput.dispatchEvent(event);

}
