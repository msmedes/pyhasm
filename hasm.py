import os
import click

from hasm.assembler import Assembler


@click.command()
@click.option("-f", help="Name of the .asm file to be converted to machine code.")
def main(f: str):
    """An assembler for converting assembly code to HACK machine code."""
    if not f:
        print("You must enter a filepath.")
        raise ValueError
    assembler = Assembler(f)
    assembler.assemble()
    output_name = f"{os.path.splitext(f)[0]}.hack"
    with open(output_name, "w") as f:
        f.writelines("\n".join(assembler.buffer))


if __name__ == "__main__":
    main()
