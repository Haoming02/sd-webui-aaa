# SD Webui Add Anything Anywhere
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), 
which automatically generates a mask for Inpainting, from the edges of a specified image.

## But Why?
When you remove the background of a subject and place it on another image, 
the edge of the subject may still contain some blending artifacts or inconsistency.
This can easily be sovlved by doing an Inpaint pass. 
However, manually drawing a mask around the edge can be a chore.
Therefore, use this Extension to automatically generate one for you!

## Settings
- **Background:** Background to place the subject on
- **Foreground:** The subject to place. Requires transparency / alpha channel
- **Mask Thickness:** The thickness of the generated mask. Adjust this based on the image resolution
- **Low/High Threshold:** Parameters for the Canny edge detection

## Example

<p align="center">
<img src="samples/01.jpg"><br>
<b>1.</b> A photo of a man
</p>

<p align="center">
<img src="samples/02.png"><br>
<b>2.</b> Remove background using <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg">rembg</a>
</p>

<p align="center">
<img src="samples/03.jpg"><br>
<b>3.</b> A photo of a background
</p>

<p align="center">
<img src="samples/04.jpg"><br>
<b>4.</b> Place subject onto the background<br>
Notice the grey outline around the subject
</p>

<p align="center">
<img src="samples/05.png"><br>
<b>5.</b> Generate a mask automatically<br>
<code>(Thickness = 10)</code>
</p>

<p align="center">
<img src="samples/06.jpg"><br>
<b>6.</b> Inpaint!
</p>

## Limitation
Right now, this can only handle images with the exact same resolution...

> Meaning, if you want to place a small object onto a large background, 
you need to create a big empty image with the object pre-placed first.

## ToDo
- [ ] Make it actually **anywhere**...

<hr>

<sup>*Yeah, the Extension name is wack. Suggestion is open :P*</sup>
