from genealogy import app

if __name__ == "__main__":
    app.run(debug=True)


@app.template_filter()
def datedisplay(value, format='%d %B, %Y (%a)'):
    """Convert a datetime to a different format."""
    if value is None:
        return None
    return value.strftime(format)


app.jinja_env.filters['datedisplay'] = datedisplay
