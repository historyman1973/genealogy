from genealogy import app

if __name__ == "__main__":
    app.run(debug=True)


@app.template_filter()
def datedisplay(value, format='%d %B, %Y (%a)'):
    """Convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datedisplay'] = datedisplay
