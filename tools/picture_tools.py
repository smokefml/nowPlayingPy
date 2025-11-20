from wand.image import Image

def verify_image(img_pth: str) -> bool:
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
    except:
        return False
