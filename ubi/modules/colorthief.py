# import cv2
import os
import asyncio
import math
from PIL import Image
from telethon import events
from telethon.tl.types import MessageMediaPhoto , MessageMediaDocument, DocumentAttributeAnimated
from ubi import u 
from colorthief import ColorThief

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


@u.on(events.NewMessage(pattern=r"\.palette"))  # pylint: disable=E0602
async def _(event):
    # if forwarded message
    out = event.message.out
    if event.fwd_from:
        return
    if event.reply_to_msg_id :
        # edits own message if outgoing , responds with new if not 
        if out : await event.edit("Downloading...")
        else : msg = await event.respond("Downloading...")
        # populates reply message object 
        target = await event.get_reply_message()
        # if media is photo 
        if isinstance(target.media , MessageMediaPhoto):
            try : 
                # downloads media
                await u.download_media(target,'domcol.jpg')

                # steal the colors off the image
                if out : await event.edit("Yoinking dominant color ...")
                else : await msg.edit("Yoinking dominant color ...")
                color_thief  = ColorThief('domcol.jpg')
                dominant_color = color_thief.get_color(quality=1)

                # generate image with palette 
                if out : await event.edit("Generating palette ...")
                else : await msg.edit("Generating palette ...")
                palette = color_thief.get_palette(color_count=12)
                original_image = Image.open('domcol.jpg')

                # get original width and height 
                ow = original_image.width
                oh = original_image.height

                # create a new image with the dominant color 
                img = Image.new("RGB", (ow+400, oh+400), dominant_color)

                # paste the original image on top of the new image
                img.paste(original_image, (200, 200))

                for index,color in enumerate(palette):
                    palette_image = Image.new("RGB", (40, 40), color)
                    img.paste(palette_image, (120, 200+index*40))

                if out : await event.edit("Uploading ...")
                else : await msg.edit("Uploading ...")

                img.save("domicol.jpg")
                # clean command message
                if out : await event.delete()
                else : await msg.delete()

                # close the original image
                original_image.close()

                # convert palette to hex 
                dom_hex = rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])
                palette_hex = []
                for color in palette :
                    palette_hex.append(rgb2hex(color[0], color[1], color[2]))
                # remove quotes 
                palette_hex = str(palette_hex)[1:-1].replace('\'','')
                # send pallette and domcol image
                await u.send_message(
                    event.chat_id, 
                    file="domicol.jpg",
                    message=f"**Dominant Color:** {dom_hex}\n\n**Palette:**  {palette_hex}")
                # cleanup residual files  
                os.remove('domcol.jpg')
                os.remove('domicol.jpg')

            except Exception as e:
                # On exception log error 
                await event.edit(str(e))

        elif isinstance(target.media , MessageMediaDocument):

            mimetype = target.media.document.mime_type
            size = target.media.document.size
            isanimated = DocumentAttributeAnimated() in target.media.document.attributes

            print(target)
            print('\n\n')
            print(target.media)
            print('\n\n')
            print(mimetype)
            print(target.media.document.attributes)
            print('\n\n')
            print(size)
            print(isanimated)
            # is an animated gif 
            if isanimated and mimetype == "video/mp4" and size < 5000000:
                # temp disable gif handling because of cv2 big 
                if out : await event.edit("Unsupported file type")
                else : await msg.edit("Unsupported file type")
                return
                # downloads media
                await u.download_media(target,'domcol.mp4')
                vidcap = cv2.VideoCapture('domcol.mp4')
                success,image = vidcap.read()
                count = 0
                while success:
                    cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
                    success,image = vidcap.read()
                    print('Read a new frame: ', success)
                    count += 1
                f0 = Image.open('frame0.jpg')
                color_thief  = ColorThief('frame0.jpg')
                dominant_color = color_thief.get_color(quality=1)
                print(f0.width)
                print(f0.height)
                grid_width = int(math.sqrt(count))
                grid_height = math.ceil(count/grid_width)
                print(f"gridwidth : {grid_width}")
                print(f"gridheight : {grid_height}")

                p_grid_width = f0.width*grid_width
                p_grid_height = f0.height*grid_height
                print(f"p_gridwidth : {p_grid_width}")
                print(f"p_gridheight : {p_grid_height}")
                canvas = Image.new("RGB", (p_grid_width, p_grid_height), dominant_color)
                ycount = 1
                for i in range(0,count):
                    img = Image.open(f"frame{i}.jpg")
                    print(f"\nframe {i}")

                    ycoord = math.ceil(i/grid_width) * f0.height
                    xcoord = (ycount * f0.width) - f0.width
                    print(f"ycoord {ycoord}")
                    print(f"xcoord {xcoord}")
                    canvas.paste(img, (xcoord, ycoord))
                    if not ycount >= grid_width:
                        ycount = ycount + 1
                    else:
                        ycount =  1
                    img.close()
                canvas.save("cvas.jpg")
                print('Finished!')
                # cleanup 
                f0.close()
                for i in range (0,count):
                    os.remove(f"frame{i}.jpg")

                # steal the colors off the image
                if out : await event.edit("Yoinking dominant color ...")
                else : await msg.edit("Yoinking dominant color ...")
                color_thief  = ColorThief('cvas.jpg')
                dominant_color = color_thief.get_color(quality=1)

                # generate image with palette 
                if out : await event.edit("Generating palette ...")
                else : await msg.edit("Generating palette ...")
                palette = color_thief.get_palette(color_count=12)
                original_image = Image.open('cvas.jpg')

                # get original width and height 
                ow = original_image.width
                oh = original_image.height

                # create a new image with the dominant color 
                img = Image.new("RGB", (ow+400, oh+400), dominant_color)

                # paste the original image on top of the new image
                img.paste(original_image, (200, 200))

                for index,color in enumerate(palette):
                    palette_image = Image.new("RGB", (40, 40), color)
                    img.paste(palette_image, (120, 200+index*40))

                if out : await event.edit("Uploading ...")
                else : await msg.edit("Uploading ...")

                img.save("domicol2.jpg")
                # clean command message
                if out : await event.delete()
                else : await msg.delete()

                # close the original image
                original_image.close()

                # convert palette to hex 
                dom_hex = rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])
                palette_hex = []
                for color in palette :
                    palette_hex.append(rgb2hex(color[0], color[1], color[2]))
                # remove quotes 
                palette_hex = str(palette_hex)[1:-1].replace('\'','')
                # send pallette and domcol image
                await u.send_message(
                    event.chat_id, 
                    file="domicol2.jpg",
                    message=f"**Dominant Color:** {dom_hex}\n\n**Palette:**  {palette_hex}")
                # cleanup residual files  
                vidcap.release()
                os.remove('domcol.mp4')
                os.remove('cvas.jpg')
                os.remove('domicol2.jpg')

            else : 
                if out : await event.edit("Unsupported file type")
                else : await msg.edit("Unsupported file type")
        else:
            # media isnt a photo type 
            if out : 
                await event.edit("**Ignoring ... **")
                await asyncio.sleep(5)
                await event.delete()
            else : 
                await msg.edit("**Ignoring ... **")
                await asyncio.sleep(5)
                await msg.delete()
