import warnings
from wand.image import Image
from wand.exceptions import OptionWarning

def verify_image(img_pth: str) -> bool:
    """
    Verifica que la imagen en path es una imagen y se asegura de que sea cuadrada
    Devuelve True si termina correctamente, pero si falla, devuelve False
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", OptionWarning)
        try:
            img = Image(filename=img_pth)
            w = img.width
            h = img.height

            if w == h:
                return True

            size = max(w,h)

            img.trim(fuzz=(img.quantum_range * 0.15))

            bg_img = img.clone()
            bg_img.resize(size,size,filter='lanczos',blur=1)
            bg_img.extent(width=size,height=size,gravity='center')
            bg_img.blur(radius=0, sigma=20.0)

            bg_img.composite(image=img,operator='over',gravity='center')

            bg_img.save(filename=img_pth)

            return True
        
        except Exception as e:
            # print(f"Error procesando imagen: {e}")
            return False
