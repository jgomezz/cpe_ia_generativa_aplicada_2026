## Pasos para crear un Space en Hugging Face, para procesar modelos de generacion de imagenes : Z-Image-Turbo

### Crear en Hugging Face un SPACE : generate-image


### Crear archivo requirements.txt
```txt

git+https://github.com/huggingface/diffusers
torch
transformers>=4.57.1
accelerate
sentencepiece
ftfy
spaces
```

### Crear archivo app.py

```py
import torch
import gradio as gr
import spaces
from diffusers import ZImagePipeline

pipe = ZImagePipeline.from_pretrained(
    "Tongyi-MAI/Z-Image-Turbo",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=False,
)
pipe.to("cuda")


@spaces.GPU(duration=20)
def generar(prompt, negative_prompt, steps, seed, width, height):
    imagen = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=int(height),
        width=int(width),
        num_inference_steps=int(steps),
        guidance_scale=0.0,
        generator=torch.Generator("cuda").manual_seed(int(seed)),
    ).images[0]
    return imagen


demo = gr.Interface(
    fn=generar,
    inputs=[
        gr.Textbox(label="Prompt", value="un gato caminando por la tarde cerca de la playa"),
        gr.Textbox(label="Prompt negativo", value=""),
        gr.Slider(1, 16, value=9, step=1, label="Steps"),
        gr.Number(value=42, label="Seed"),
        gr.Slider(512, 1536, value=1024, step=64, label="Ancho"),
        gr.Slider(512, 1536, value=1024, step=64, label="Alto"),
    ],
    outputs=gr.Image(label="Resultado"),
    title="Z-Image Turbo",
)

demo.launch()


```