from genealogy import app

if __name__ == "__main__":
    app.run(debug=True)


@app.template_filter()
# def datetimefilter(value, format='%Y/%m/%d %H:%M'):
def datedisplay(value, format='%d %B, %Y'):
    """Convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datedisplay'] = datedisplay
