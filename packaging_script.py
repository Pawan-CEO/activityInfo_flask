from tamo import Taco

taco = Taco(
    connector_file='main.py',
    dest_dir='.',
    name='Shaktiman WDC',
    version='1.0',
)

taco.generate_taco()
