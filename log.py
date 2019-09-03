from setuptools import setup
setup()
import clipboard

text = clipboard.paste()
print(text)
