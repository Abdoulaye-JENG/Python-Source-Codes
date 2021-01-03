import random
import string

def generate_random_string(size=15, allowed_characters = None):
    chars = string.ascii_letters + string.digits + string.punctuation
    allowed_characters = chars if allowed_characters is None else allowed_characters
    return ''.join(random.SystemRandom().choice(allowed_characters) for _ in range(size+1)) 


if __name__ == "__main__":
    print(generate_random_string())