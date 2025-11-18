---

<p align="center">
    <img width="1080" height="720" src="https://files.catbox.moe/eiew9b.png">
</p>

<h1 align="center">
    MakersBNB
</h1>

<p align="center">
    AirBNB clone made with Flask and Basecoat UI.
</p>

---
## Contributors
- [Milo Tek](https://github.com/pixeljammed)
- [Tom Peace](https://github.com/thomaspeace)
- [Ryan Osmaston](https://github.com/Ryasmaston)
- [Vincent Adeola](https://github.com/dir-V)
- [Josh Hil](https://github.com/JoshHil97)
- [Daniel Pascaru](https://github.com/harpleen)


## Setup

```shell
# Set up the virtual environment
; python -m venv makersbnb-venv

# Activate the virtual environment
; source makersbnb-venv/bin/activate 

# Install dependencies
(makersbnb-venv); pip install -r requirements.txt

# Install the virtual browser we will use for testing
(makersbnb-venv); playwright install
# If you have problems with the above, contact your coach

# Create a test and development database
(makersbnb-venv); createdb MAKERSBNB
(makersbnb-venv); createdb MAKERSBNB_TEST

# Open lib/database_connection.py and change the database names
(makersbnb-venv); open lib/database_connection.py

# Run the tests (with extra logging)
(makersbnb-venv); pytest -sv

# Run the app
(makersbnb-venv); python app.py

# Now visit http://localhost:5001/index in your browser
```
