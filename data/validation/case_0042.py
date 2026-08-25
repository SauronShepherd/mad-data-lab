from data.generation import generate_case

def validate():
    return generate_case().content_hash

if __name__ == '__main__': print(validate())
