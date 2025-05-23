import cv2
from PIL import Image
import scratchattach as sa
from scratchattach import Encoding
cloud = sa.get_tw_cloud("1169610073") #replace with your project id
client = cloud.requests()

def get_image_colors_from_pil(pil_img):
    width, height = 40, 40  # Width first!
    pil_img = pil_img.resize((width, height)).convert("RGB")

    # Fast pixel access using getdata()
    pixels = pil_img.getdata()
    hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels]

    return hex_colors

def capture_and_get_colors(cap):
    ret, frame = cap.read()
    if not ret:
        return []
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)
    return get_image_colors_from_pil(pil_img)

def chat(to_host_):
    return Encoding.decode(int(to_host_)) #will decode an encoded text


# Example usage
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tempchat = ""
    try:
        while True:
            hex_colors = capture_and_get_colors(cap)
            to_host = cloud.get_var("TO_HOST")
            if to_host!= None:
                if chat(to_host) != tempchat:
                    hex_colors.append(chat(to_host))
                    tempchat=chat(to_host)
            client.send(hex_colors)

    finally:
        cap.release()

