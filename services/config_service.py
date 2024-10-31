from models.models import Configuration, db
def sanitize_keywords(keywords):
    # Split by comma, strip spaces, convert to lowercase, and rejoin with comma
    return ",".join(word.strip().lower() for word in keywords.split(",") if word.strip())

def create_configuration(data):
    # Set default values for missing fields
    selected_sites = data.getlist('sites')
    city = data.get('city', "Bucuresti")
    rooms = int(data.get('rooms') or 1)
    compartment = data.get('compartment', "All")
    min_price = int(data.get('min_price') or 500)
    max_price = int(data.get('max_price') or 3000)
    min_square_meters = int(data.get('min_square_meters') or 20)
    max_square_meters = int(data.get('max_square_meters') or 100)
    min_year_built = int(data.get('min_year_built') or 2000)
    exclude_words = sanitize_keywords(data.get('exclude_words', ""))
    include_words = sanitize_keywords(data.get('include_words', ""))

    # Create a new Configuration object
    config = Configuration(
        city=city,
        rooms=rooms,
        compartment=compartment,
        min_price=min_price,
        max_price=max_price,
        min_square_meters=min_square_meters,
        max_square_meters=max_square_meters,
        min_year_built=min_year_built,
        exclude_words=exclude_words,
        include_words=include_words,
        selected_sites=selected_sites

    )

    # Save to the database
    db.session.add(config)
    db.session.commit()
    return config
