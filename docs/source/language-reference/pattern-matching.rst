Pattern matching
----------------

Use pattern matching to promote an object to its class from one of its
traits. Pattern matching can match object contents or value as
well.

.. warning::

   Pattern matching is only partly implemented.

Below is the contents of ``src/main.mys`` found in the
`pattern_matching example`_.

.. code-block:: python

   @trait
   class Base:
       pass

   class Foo(Base):
       a: i64
       b: string

   class Bar(Base):
       pass

   class Fie(Base):
       pass

   def traits(base: Base):
       # Foo() and Bar() just means these classes with any state. No
       # instance is created, just the type is checked.
       match base:
           case Foo(a=1) as foo:
               print(f"Trait foo with a=1 and b=\"{foo.b}\".")
           case Foo(a=2, b="ho"):
               print("Trait foo with a=2 and b=\"ho\".")
           case Foo():
               print("Trait foo.")
           case Bar():
               print("Trait bar.")
           case _:
               print(f"Other trait: {base}")

   def numbers(value: i64):
       match value:
           case 0:
               print("Zero integer.")
           case 5:
               print("Five integer.")

   def strings(value: string):
       match value:
           case "foo":
               print("String foo.")
           case _:
               print(f"Other string: {value}")

   def main():
       traits(Foo(1, "hi"))
       traits(Foo(2, "ho"))
       traits(Foo(3, ""))
       traits(Bar())
       traits(Fie())
       numbers(0)
       numbers(1)
       numbers(5)
       strings("foo")
       strings("bar")

Build and run.

.. code-block:: text

   $ mys run
   Trait foo with a=1 and b="hi".
   Trait foo with a=2 and b="ho".
   Trait foo.
   Trait bar.
   Other trait: Fie()
   Zero integer.
   Five integer.
   String foo.
   Other string: bar

.. _pattern_matching example: https://github.com/mys-lang/mys/tree/main/examples/pattern_matching
