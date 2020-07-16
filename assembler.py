import click


@click.command()
@click.option(
    "--filename", help="Name of the .asm file to be converted to machine code."
)
@click.option("--destination", default="./", help="Path to destination")
def main(filename: str, destination: str):
    """An assembler for converting assembly code to HACK machine code."""
    if not filename:
        print("You must enter a filename.")
    print(filename, destination)


if __name__ == "__main__":
    main()
