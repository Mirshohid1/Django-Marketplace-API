from pathlib import Path
from uuid import uuid4


def base_upload_path(instance, filename, dir_name):
    ext = Path(filename).suffix

    return f"{dir_name}/" f"{instance.id}/" f"{uuid4().hex}{ext}"


def product_image_upload_path(instance, filename):
    return base_upload_path(instance, filename, "products")


def product_variant_upload_path(instance, filename):
    return base_upload_path(instance, filename, "product_variants")
