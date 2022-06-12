import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ImageField
from PIL import Image


def compressImage(
    uploadedImage: ImageField,
    quality: int = 50,
    lossless: bool = False
) -> InMemoryUploadedFile:
    """
    lossless
        If present and true, instructs the WebP writer to use lossless compression.

    quality
        Integer, 1-100, Defaults to 80. For lossy, 0 gives the smallest size and 100 the largest. For lossless, this parameter is the amount of effort put into the compression: 0 is the fastest, but gives larger files compared to the slowest, but best, 100.
    """

    imageTemporary = Image.open(uploadedImage)

    outputIoStream = BytesIO()
    imageTemporary.save(outputIoStream,
                        format='webp',
                        quality=quality,
                        lossless=lossless)
    outputIoStream.seek(0)

    uploadedImage = InMemoryUploadedFile(
        outputIoStream, 'ImageField',
        "%s.webp" % uploadedImage.name.split('.')[0], 'image/webp',
        sys.getsizeof(outputIoStream), None)

    return uploadedImage
