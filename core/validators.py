from django.core.exceptions import ValidationError
import os

def validate_file_size(value):
    limit = 50 * 1024 * 1024 # 50 MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 50 MB.')

def validate_image_size(value):
    limit = 5 * 1024 * 1024 # 5 MB
    if value.size > limit:
        raise ValidationError('Image too large. Size should not exceed 5 MB.')

def validate_audio_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.wav', '.m4a']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed: .mp3, .wav, .m4a')
