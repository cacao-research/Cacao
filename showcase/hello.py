# Hello World — showcase demo
import cacao as c

c.config(title="Hello Cacao", branding=True)

c.title("Hello, Cacao!")
c.text("The simplest Python web framework")
c.spacer()

with c.card("Getting Started"):
    c.code("""import cacao as c

c.title("Hello, Cacao!")
c.text("Build web apps in pure Python")

with c.row():
    c.metric("Lines of Code", "4")
    c.metric("Dependencies", "0")
    c.metric("Setup Time", "10s")
""", language="python")

c.spacer()

with c.row():
    c.metric("Lines of Code", "4")
    c.metric("Dependencies", "0")
    c.metric("Setup Time", "10s")
